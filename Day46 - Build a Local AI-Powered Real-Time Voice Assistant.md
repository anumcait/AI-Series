# 🚀 Day 46 — Build a Local AI-Powered Real-Time Voice Assistant 🎙️🤖

## Objective

Build a 100% offline, privacy-first conversational voice assistant application to capture spoken audio, transcribe speech using Faster-Whisper, reason through multi-turn dialogue with local Qwen3, synthesize natural speech output via offline SAPI5, and interact through a Streamlit dashboard.

## Technologies Used

- Python
- Faster-Whisper (CTranslate2 & int8 CPU)
- Ollama – Qwen3
- Windows SAPI5 / pyttsx3 (Offline Text-to-Speech)
- SoundDevice & SoundFile
- Streamlit
- NumPy
- Requests

## Work Completed

1. **Speech Engine Integration**: Configured Faster-Whisper (`base`, `int8` CPU) with Voice Activity Detection (`vad_filter=True`) and connected to local Ollama (`qwen3:4b`) via `/api/chat`.
2. **Dual-Mode Audio Ingestion**: Built microphone recording via `sounddevice` alongside an automated Windows SAPI speech simulation fallback for environments without a physical microphone (`PaErrorCode -9996`).
3. **Buffer Optimization**: Streamed audio directly as NumPy Float32 arrays into Faster-Whisper, eliminating intermediate disk I/O and resolving PyAV container open bugs.
4. **Conversational Voice Prompting**: Configured Qwen3 with an oral-adapted system prompt enforcing concise 2-sentence spoken responses.
5. **Offline Speech Synthesis (TTS)**: Integrated Windows SAPI5 (`SpVoice` & `SpFileStream`) with COM apartment initialization (`pythoncom.CoInitialize()`) and browser audio playback.
6. **Streamlit Dashboard**: Created a split-screen interface featuring live metrics, dialogue history, audio replay, and one-click voice test presets.

## Workflow

Audio Input (Microphone / SAPI Simulation) → Float32 Buffer → Faster-Whisper (STT) → Qwen3 Analysis → SAPI5 Synthesis (TTS) → Browser Audio Playback → Streamlit Dashboard

## File Contents

### `requirements.txt`
```text
streamlit
sounddevice
soundfile
numpy
scipy
faster-whisper
pyttsx3
ollama
plotly
pandas
```

### `app.py`
```python
import os
import tempfile
import requests
import numpy as np
import sounddevice as sd
import soundfile as sf
import streamlit as st

try:
    import pythoncom
    import win32com.client
    HAS_WIN32COM = True
except ImportError:
    HAS_WIN32COM = False

from faster_whisper import WhisperModel

MODEL_NAME = "qwen3:4b"
OLLAMA_URL = "http://localhost:11434/api/chat"
SAMPLE_RATE = 16000
RECORD_SECONDS = 5

st.set_page_config(page_title="Day 46 - AI Voice Assistant", page_icon="🎙️", layout="wide")

@st.cache_resource
def load_whisper():
    return WhisperModel("base", device="cpu", compute_type="int8")

def text_to_speech_wav(text):
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_path = temp_wav.name
    temp_wav.close()

    if HAS_WIN32COM:
        pythoncom.CoInitialize()
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        stream = win32com.client.Dispatch("SAPI.SpFileStream")
        stream.Open(temp_path, 3, False)
        speaker.AudioOutputStream = stream
        speaker.Speak(text)
        stream.Close()
    else:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, temp_path)
        engine.runAndWait()
        engine.stop()

    return temp_path

def synthesize_test_audio(text_prompt):
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

def has_input_audio_device():
    try:
        devices = sd.query_devices()
        return len([d for d in devices if d.get('max_input_channels', 0) > 0]) > 0
    except Exception:
        return False

def record_audio():
    st.info(f"Listening for {RECORD_SECONDS} seconds. Speak now!")
    audio = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()

def transcribe_audio_array(audio_np):
    if audio_np is None or len(audio_np) == 0:
        return "", ""
    model = load_whisper()
    segments, info = model.transcribe(audio_np, beam_size=1, vad_filter=True)
    return " ".join(seg.text.strip() for seg in segments).strip(), info.language

def ask_qwen(messages):
    response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "messages": messages, "stream": False}, timeout=180)
    response.raise_for_status()
    return response.json()["message"]["content"]

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful voice assistant. Answer clearly, naturally, and concisely in 2 sentences."}]
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""
if "last_response_audio" not in st.session_state:
    st.session_state.last_response_audio = None

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
    input_mode = st.radio("Select Audio Source:", ["🧪 Test Voice Simulation (No Mic Needed)", "🎤 Physical Microphone"], index=0 if not mic_ready else 1)
    triggered_audio = None

    if input_mode == "🧪 Test Voice Simulation (No Mic Needed)":
        st.info("💡 Perfect when running in environments without a physical microphone.")
        preset_prompt = st.selectbox("Choose a spoken test prompt:", [
            "What is Docker in one simple sentence?",
            "How is the weather today?",
            "Explain the role of an AI Agent.",
            "How does local Whisper transcribe spoken audio?",
            "Tell me a short fun fact about space."
        ])
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

    if triggered_audio is not None:
        try:
            with st.spinner("Transcribing speech with Faster-Whisper..."):
                question, language = transcribe_audio_array(triggered_audio)

            if not question:
                st.warning("No speech detected. Please try another sample.")
            else:
                st.session_state.last_question = question
                st.session_state.messages.append({"role": "user", "content": question})

                with st.spinner("Qwen3 is reasoning..."):
                    answer = ask_qwen(st.session_state.messages)

                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.session_state.last_answer = answer

                with st.spinner("Synthesizing voice response audio..."):
                    st.session_state.last_response_audio = text_to_speech_wav(answer)
                st.rerun()
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to Ollama. Make sure Ollama is running.")
        except Exception as error:
            st.error(f"Voice pipeline error: {error}")

    if st.session_state.last_response_audio and os.path.exists(st.session_state.last_response_audio):
        st.divider()
        st.subheader("🔊 Audio Response")
        st.audio(st.session_state.last_response_audio, format="audio/wav", autoplay=True)

    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": "You are a helpful voice assistant. Answer clearly, naturally, and concisely in 2 sentences."}]
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
```

## Initial Test & Verification Result

- **Ollama Model**: `qwen3:4b`
- **STT Model**: `faster-whisper (base, int8 CPU)`
- **Sample Rate**: `16,000 Hz`
- **Test Input Query**: `"How is the weather today?"`
- **Synthesized Audio Samples**: `44,523 Float32 frames`
- **STT Transcription Result**: `"How is the weather today?"` (Language: `en`)
- **Qwen3 Response**: `"I don't have access to real-time weather data, but you can check the current conditions using a weather app, website, or by searching 'weather today' on Google."`
- **Response Audio Output**: `422,194 bytes WAV file`
- **Pipeline Status**: Verified end-to-end with 100% offline local execution.

## Important Limitations

- Speech recognition accuracy depends on Whisper model size (`base` prioritizes latency over `large-v3` precision).
- Physical microphone recording requires an active audio input device enabled in the OS.
- Dialogue follows a turn-based request-response flow rather than full-duplex interruption.
- Text-to-speech voice timbre is determined by the installed system SAPI5 voice packages.
- Local Ollama instance must remain active on `http://localhost:11434` with `qwen3:4b`.

## Outcome

Implemented a local real-time AI voice assistant with Faster-Whisper speech-to-text, dual-mode audio capture (physical microphone + offline voice simulation), local Qwen3 conversational dialogue, offline SAPI5 speech synthesis, and an interactive Streamlit dashboard.

### Screenshots

<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/075d6d8a-a864-4882-bf58-511f2abbf529" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/7bb4bc9d-7eee-4c90-af9c-65eea0627fc1" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/24e0fd99-8d9c-4687-abfb-7bb8e6b73ed1" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/e68d6484-99c2-4313-b8f2-289b62f8d4fa" />
