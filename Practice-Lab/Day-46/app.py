import os
import tempfile
import requests
import numpy as np
import sounddevice as sd
import soundfile as sf
import streamlit as st

# Windows SAPI COM for robust offline TTS
try:
    import pythoncom
    import win32com.client
    HAS_WIN32COM = True
except ImportError:
    HAS_WIN32COM = False

from faster_whisper import WhisperModel

# ---------------- CONFIGURATION ----------------

MODEL_NAME = "qwen3:4b"
OLLAMA_URL = "http://localhost:11434/api/chat"

SAMPLE_RATE = 16000
RECORD_SECONDS = 5

st.set_page_config(
    page_title="Day 46 - AI Voice Assistant",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- LOAD SPEECH MODEL ----------------

@st.cache_resource
def load_whisper():
    return WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

# ---------------- AUDIO SYNTHESIS & TTS ----------------

def text_to_speech_wav(text):
    """
    Synthesizes speech into a temporary WAV file using native Windows SAPI.
    Works 100% reliably in background threads without blocking.
    """
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path = temp_wav.name
    temp_wav.close()

    if HAS_WIN32COM:
        pythoncom.CoInitialize()
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        stream = win32com.client.Dispatch("SAPI.SpFileStream")
        # 3 = SSFMCreateForWrite
        stream.Open(temp_path, 3, False)
        speaker.AudioOutputStream = stream
        speaker.Speak(text)
        stream.Close()
    else:
        # Fallback if win32com is absent: use pyttsx3
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, temp_path)
        engine.runAndWait()
        engine.stop()

    return temp_path

def synthesize_test_audio(text_prompt):
    """
    Synthesizes speech into a NumPy float32 array for testing
    when no physical microphone is connected.
    """
    wav_path = text_to_speech_wav(text_prompt)
    data, sr = sf.read(wav_path, dtype="float32")
    
    if os.path.exists(wav_path):
        try:
            os.remove(wav_path)
        except Exception:
            pass
        
    if data.ndim > 1:
        data = data.mean(axis=1)
        
    return data.astype(np.float32)

# ---------------- SPEECH TO TEXT ----------------

def has_input_audio_device():
    """Checks if a valid input microphone is available."""
    try:
        devices = sd.query_devices()
        input_devs = [d for d in devices if d.get('max_input_channels', 0) > 0]
        return len(input_devs) > 0
    except Exception:
        return False

def record_audio():
    st.info(f"Listening for {RECORD_SECONDS} seconds. Speak now!")
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    return audio.flatten()

def transcribe_audio_array(audio_np):
    """Transcribes directly from a NumPy float32 array, bypassing PyAV container errors."""
    if audio_np is None or len(audio_np) == 0:
        return "", ""

    model = load_whisper()
    segments, info = model.transcribe(
        audio_np,
        beam_size=1,
        vad_filter=True
    )
    text = " ".join(segment.text.strip() for segment in segments)
    return text.strip(), info.language

# ---------------- LOCAL AI RESPONSE ----------------

def ask_qwen(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )
    response.raise_for_status()
    return response.json()["message"]["content"]

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful voice assistant. "
                "Answer clearly, naturally, and concisely in 2 sentences."
            )
        }
    ]

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "last_response_audio" not in st.session_state:
    st.session_state.last_response_audio = None

# ---------------- DASHBOARD UI ----------------

st.title("🎙️ Day 46 — Local AI Voice Assistant")
st.caption("Speech-to-Text (Faster-Whisper) • Local Reasoning (Qwen3) • Text-to-Speech (SAPI5)")

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("Ollama Model", MODEL_NAME)
with col_m2:
    st.metric("STT Engine", "Faster-Whisper (int8)")
with col_m3:
    mic_ready = has_input_audio_device()
    st.metric("Microphone", "Available" if mic_ready else "Simulated / No Mic")

st.divider()

col_chat, col_controls = st.columns([1.2, 1])

with col_controls:
    st.subheader("⚡ Voice Input Controls")
    
    input_mode = st.radio(
        "Select Audio Source:",
        ["🧪 Test Voice Simulation (No Mic Needed)", "🎤 Physical Microphone"],
        index=0 if not mic_ready else 1
    )
    
    triggered_audio = None
    
    if input_mode == "🧪 Test Voice Simulation (No Mic Needed)":
        st.info("💡 Perfect when running in environments without a physical microphone.")
        preset_prompt = st.selectbox(
            "Choose a spoken test prompt:",
            [
                "What is Docker in one simple sentence?",
                "How is the weather today?",
                "Explain the role of an AI Agent.",
                "How does local Whisper transcribe spoken audio?",
                "Tell me a short fun fact about space."
            ]
        )
        custom_voice = st.text_input("Or enter custom spoken text to test:", value="")
        test_text = custom_voice.strip() if custom_voice.strip() else preset_prompt
        
        if st.button("▶️ Simulate Spoken Audio & Run", type="primary", use_container_width=True):
            with st.spinner(f"Synthesizing spoken audio for: '{test_text}'..."):
                triggered_audio = synthesize_test_audio(test_text)
                
    else:
        st.markdown("*Requires a connected and enabled physical microphone.*")
        if st.button("🎤 Start Speaking (Record)", type="primary", use_container_width=True):
            try:
                triggered_audio = record_audio()
            except Exception as e:
                st.error(f"Microphone device error: {e}. Please switch to 'Test Voice Simulation' above.")

    # Process audio if triggered
    if triggered_audio is not None:
        try:
            with st.spinner("Transcribing speech with Faster-Whisper..."):
                question, language = transcribe_audio_array(triggered_audio)

            if not question:
                st.warning("No speech detected. Please try another sample.")
            else:
                st.session_state.last_question = question
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })

                with st.spinner("Qwen3 is reasoning..."):
                    answer = ask_qwen(st.session_state.messages)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
                st.session_state.last_answer = answer

                with st.spinner("Synthesizing voice response audio..."):
                    audio_out = text_to_speech_wav(answer)
                    st.session_state.last_response_audio = audio_out
                
                st.rerun()

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to Ollama. Make sure Ollama is running.")
        except Exception as error:
            st.error(f"Voice pipeline error: {error}")

    # Replay audio widget
    if st.session_state.last_response_audio and os.path.exists(st.session_state.last_response_audio):
        st.divider()
        st.subheader("🔊 Audio Response")
        st.audio(st.session_state.last_response_audio, format="audio/wav", autoplay=True)

    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful voice assistant. "
                    "Answer clearly, naturally, and concisely in 2 sentences."
                )
            }
        ]
        st.session_state.last_question = ""
        st.session_state.last_answer = ""
        st.session_state.last_response_audio = None
        st.rerun()

with col_chat:
    st.subheader("💬 Active Dialogue")
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
