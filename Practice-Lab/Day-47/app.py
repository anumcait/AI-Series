import os
import json
import socket
import tempfile
import psutil
import requests
import numpy as np
import sounddevice as sd
import soundfile as sf
import streamlit as st

# Windows SAPI COM for offline TTS
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
DEFAULT_TIMEOUT = 180

st.set_page_config(
    page_title="Day 47 - Voice-Controlled DevOps Assistant",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- LOCAL STT ENGINE ----------------

@st.cache_resource
def load_whisper():
    return WhisperModel("base", device="cpu", compute_type="int8")

def normalize_spoken_devops_terms(text: str) -> str:
    """Corrects common Whisper phonetic mishearings for DevOps names."""
    corrections = {
        "all in the": "ollama",
        "o llama": "ollama",
        "olama": "ollama",
        "dr": "docker",
        "ps util": "psutil",
        "gin x": "nginx",
        "engine x": "nginx"
    }
    normalized = text
    for wrong, right in corrections.items():
        if wrong in normalized.lower():
            # Case-insensitive replacement
            idx = normalized.lower().find(wrong)
            normalized = normalized[:idx] + right + normalized[idx + len(wrong):]
    return normalized

def transcribe_audio_array(audio_np):
    if audio_np is None or len(audio_np) == 0:
        return "", ""
    model = load_whisper()
    segments, info = model.transcribe(audio_np, beam_size=1, vad_filter=True)
    raw_text = " ".join(seg.text.strip() for seg in segments).strip()
    clean_text = normalize_spoken_devops_terms(raw_text)
    return clean_text, info.language

# ---------------- OFFLINE TTS & SIMULATION ----------------

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
        return len([d for d in devices if d.get("max_input_channels", 0) > 0]) > 0
    except Exception:
        return False

def record_audio():
    st.info(f"Listening for {RECORD_SECONDS} seconds. Speak your DevOps command now!")
    audio = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()

# ---------------- DEVOPS TOOLS ----------------

def get_system_health():
    """Gathers real-time CPU, RAM, and Disk metrics."""
    cpu_percent = psutil.cpu_percent(interval=0.2)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/') if os.name != 'nt' else psutil.disk_usage('C:\\')
    return {
        "status": "warning" if cpu_percent > 85 or memory.percent > 90 else "healthy",
        "cpu_usage_percent": cpu_percent,
        "memory_used_percent": memory.percent,
        "memory_available_gb": round(memory.available / (1024 ** 3), 2),
        "disk_used_percent": disk.percent,
        "disk_free_gb": round(disk.free / (1024 ** 3), 2)
    }

def check_process_status(process_name: str):
    """Checks if a given process or service is running."""
    matches = []
    target = process_name.lower().strip()
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            p_name = proc.info.get('name', '') or ''
            if target in p_name.lower():
                matches.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return {
        "query": process_name,
        "is_running": len(matches) > 0,
        "instance_count": len(matches),
        "matching_processes": matches[:5]
    }

def check_port_reachability(host: str, port: int):
    """Tests TCP socket connection to a host and port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect((host, int(port)))
        s.close()
        return {"host": host, "port": port, "reachable": True, "message": "Connection successful"}
    except Exception as e:
        return {"host": host, "port": port, "reachable": False, "error": str(e)}

def inspect_recent_incident_logs(filter_level: str = "ERROR"):
    """Returns sample mock incident logs for diagnostics."""
    logs = [
        {"timestamp": "2026-11-10T11:30:15", "level": "WARNING", "service": "auth-api", "msg": "High response latency (450ms)"},
        {"timestamp": "2026-11-10T11:32:40", "level": "ERROR", "service": "db-worker", "msg": "Database connection pool exhausted"},
        {"timestamp": "2026-11-10T11:35:10", "level": "INFO", "service": "ingress", "msg": "Health check 200 OK from 10.0.1.25"}
    ]
    if filter_level:
        logs = [log for log in logs if log["level"].upper() == filter_level.upper()]
    return {"filter": filter_level, "log_count": len(logs), "logs": logs}

AVAILABLE_TOOLS = {
    "get_system_health": get_system_health,
    "check_process_status": check_process_status,
    "check_port_reachability": check_port_reachability,
    "inspect_recent_incident_logs": inspect_recent_incident_logs
}

DEVOPS_TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_system_health",
            "description": "Returns live server CPU, Memory, and Disk usage metrics.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_process_status",
            "description": "Checks if a service or process is currently active on the host.",
            "parameters": {
                "type": "object",
                "properties": {
                    "process_name": {"type": "string", "description": "Name of the process, e.g. python, ollama, chrome, docker"}
                },
                "required": ["process_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_port_reachability",
            "description": "Checks if a TCP port on a target host is reachable.",
            "parameters": {
                "type": "object",
                "properties": {
                    "host": {"type": "string", "description": "Hostname or IP address, e.g. localhost or 127.0.0.1"},
                    "port": {"type": "integer", "description": "Port number, e.g. 11434, 8501, 80"}
                },
                "required": ["host", "port"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "inspect_recent_incident_logs",
            "description": "Inspects recent operational error and warning logs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter_level": {"type": "string", "description": "Log level: ERROR, WARNING, or INFO", "default": "ERROR"}
                }
            }
        }
    }
]

# ---------------- LOCAL AI DEVOPS AGENT LOOP ----------------

def fallback_keyword_diagnosis(user_command: str):
    """Fallback diagnostic executor when Ollama is overloaded or times out."""
    cmd_lower = user_command.lower()
    executed_tools = []
    
    if any(k in cmd_lower for k in ["cpu", "memory", "ram", "disk", "health"]):
        res = get_system_health()
        executed_tools.append({"tool": "get_system_health", "arguments": {}, "result": res})
        ans = f"System CPU is at {res['cpu_usage_percent']}%, Memory is at {res['memory_used_percent']}%, and you have {res['disk_free_gb']} GB free disk space."
        return ans, executed_tools

    if any(k in cmd_lower for k in ["process", "running", "service", "ollama", "docker", "python"]):
        target = "ollama" if "ollama" in cmd_lower else ("docker" if "docker" in cmd_lower else "python")
        res = check_process_status(target)
        executed_tools.append({"tool": "check_process_status", "arguments": {"process_name": target}, "result": res})
        if res["is_running"]:
            ans = f"The {target} process is currently running with {res['instance_count']} active instances."
        else:
            ans = f"The {target} process does not appear to be running on this system."
        return ans, executed_tools

    if "port" in cmd_lower or "connection" in cmd_lower:
        port = 11434 if "11434" in cmd_lower else (8501 if "8501" in cmd_lower else 80)
        res = check_port_reachability("localhost", port)
        executed_tools.append({"tool": "check_port_reachability", "arguments": {"host": "localhost", "port": port}, "result": res})
        state = "reachable" if res["reachable"] else "unreachable"
        ans = f"Port {port} on localhost is currently {state}."
        return ans, executed_tools

    if "log" in cmd_lower or "incident" in cmd_lower or "error" in cmd_lower:
        res = inspect_recent_incident_logs("ERROR")
        executed_tools.append({"tool": "inspect_recent_incident_logs", "arguments": {"filter_level": "ERROR"}, "result": res})
        ans = f"Found {res['log_count']} recent error logs, including database connection pool issues."
        return ans, executed_tools

    return "DevOps query processed, but no specific action was required.", executed_tools

def execute_voice_devops_loop(user_voice_command, messages, model_name=MODEL_NAME, timeout_sec=DEFAULT_TIMEOUT):
    """
    Executes Tool-Calling loop with local Qwen3:
    1. Keeps payload lean (capped context) to protect host under high RAM/CPU load.
    2. Constrains token generation (num_predict) for ultra-fast latency.
    3. Handles timeouts gracefully with automated deterministic diagnostic fallback.
    """
    # Build lean message history: system prompt + last 2 turns to prevent RAM thrashing
    lean_messages = [messages[0]]  # system prompt
    recent_turns = [m for m in messages[1:] if m.get("role") in ["user", "assistant"]][-4:]
    lean_messages.extend(recent_turns)
    lean_messages.append({"role": "user", "content": user_voice_command})
    
    payload = {
        "model": model_name,
        "messages": lean_messages,
        "tools": DEVOPS_TOOL_DEFINITIONS,
        "stream": False,
        "options": {
            "num_predict": 128,  # Limit generation for fast voice responses
            "temperature": 0.2,
            "num_ctx": 2048      # Capped context prevents out-of-memory paging
        }
    }

    executed_tool_details = []

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=timeout_sec)
        res.raise_for_status()
        message_data = res.json()["message"]

        # Check for tool calls
        if "tool_calls" in message_data and message_data["tool_calls"]:
            lean_messages.append(message_data)
            
            for tool_call in message_data["tool_calls"]:
                func_name = tool_call["function"]["name"]
                func_args = tool_call["function"].get("arguments", {})
                if isinstance(func_args, str):
                    try:
                        func_args = json.loads(func_args)
                    except Exception:
                        func_args = {}

                if func_name in AVAILABLE_TOOLS:
                    tool_func = AVAILABLE_TOOLS[func_name]
                    observation = tool_func(**func_args)
                    executed_tool_details.append({
                        "tool": func_name,
                        "arguments": func_args,
                        "result": observation
                    })

                    lean_messages.append({
                        "role": "tool",
                        "content": json.dumps(observation)
                    })

            # Final voice synthesis generation pass
            second_payload = {
                "model": model_name,
                "messages": lean_messages,
                "stream": False,
                "options": {
                    "num_predict": 128,
                    "temperature": 0.2
                }
            }
            res2 = requests.post(OLLAMA_URL, json=second_payload, timeout=timeout_sec)
            res2.raise_for_status()
            final_answer = res2.json()["message"]["content"]
        else:
            final_answer = message_data.get("content", "Command acknowledged.")

    except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
        # Graceful fallback: System is under heavy RAM/CPU pressure (>90%)
        fallback_ans, fallback_tools = fallback_keyword_diagnosis(user_voice_command)
        final_answer = f"[High Load Fallback] {fallback_ans}"
        executed_tool_details = fallback_tools

    messages.append({"role": "user", "content": user_voice_command})
    messages.append({"role": "assistant", "content": final_answer})
    return final_answer, executed_tool_details

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an AI-powered voice DevOps assistant. "
                "Use tools to inspect system metrics, check processes, test ports, or read logs. "
                "Always summarize findings clearly, calmly, and concisely in 2 sentences for voice read-out."
            )
        }
    ]

if "last_executed_tools" not in st.session_state:
    st.session_state.last_executed_tools = []

if "last_voice_response" not in st.session_state:
    st.session_state.last_voice_response = ""

if "last_response_audio" not in st.session_state:
    st.session_state.last_response_audio = None

# ---------------- UI DASHBOARD ----------------

st.title("🎙️ Day 47 — Voice-Controlled DevOps Assistant ⚙️")
st.caption("Voice-to-Command (Faster-Whisper) • DevOps Tool Calling (Ollama Qwen3) • Offline Voice Feedback (SAPI5)")

# Top telemetry bar
health_snapshot = get_system_health()
c1, c2, c3, c4 = st.columns(4)

cpu_val = health_snapshot['cpu_usage_percent']
mem_val = health_snapshot['memory_used_percent']

c1.metric(
    "CPU Utilization", 
    f"{cpu_val}%", 
    delta="High Load" if cpu_val > 85 else "Normal",
    delta_color="inverse"
)
c2.metric(
    "Memory Used", 
    f"{mem_val}%", 
    delta="Critically Full" if mem_val > 90 else "Normal",
    delta_color="inverse"
)
c3.metric("Free Disk", f"{health_snapshot['disk_free_gb']} GB")
mic_ok = has_input_audio_device()
c4.metric("Voice Input", "Physical Mic" if mic_ok else "Simulated Audio")

if mem_val > 90 or cpu_val > 85:
    st.warning("⚠️ **Host Resource Alert**: CPU or Memory is above 90%. Ollama responses are automatically optimized with low-context memory caching and fast timeout protection.")

st.divider()

col_chat, col_tools = st.columns([1.1, 1])

with col_tools:
    st.subheader("⚡ Spoken DevOps Controls")
    
    input_mode = st.radio(
        "Audio Source:",
        ["🧪 Test Voice Simulation (No Mic Needed)", "🎤 Physical Microphone"],
        index=0 if not mic_ok else 1
    )

    triggered_audio = None

    if input_mode == "🧪 Test Voice Simulation (No Mic Needed)":
        preset_command = st.selectbox(
            "Select Spoken DevOps Directive:",
            [
                "Is the Ollama service process currently running?",
                "Check server CPU, memory, and disk health.",
                "Test TCP connection to port 11434 on localhost.",
                "Inspect recent error logs for database issues."
            ]
        )
        custom_voice = st.text_input("Or enter custom spoken command:", value="")
        command_text = custom_voice.strip() if custom_voice.strip() else preset_command

        if st.button("▶️ Speak DevOps Command & Execute", type="primary", use_container_width=True):
            with st.spinner(f"Synthesizing voice audio for: '{command_text}'..."):
                triggered_audio = synthesize_test_audio(command_text)
    else:
        if st.button("🎤 Start Speaking Command", type="primary", use_container_width=True):
            try:
                triggered_audio = record_audio()
            except Exception as e:
                st.error(f"Microphone error: {e}. Switch to 'Test Voice Simulation'.")

    # Run pipeline if audio triggered
    if triggered_audio is not None:
        try:
            with st.spinner("Transcribing spoken directive with Whisper..."):
                transcript, lang = transcribe_audio_array(triggered_audio)

            if not transcript:
                st.warning("No spoken command detected. Try again.")
            else:
                with st.spinner(f"Executing DevOps tool loop for: '{transcript}'..."):
                    voice_answer, tool_traces = execute_voice_devops_loop(
                        transcript,
                        st.session_state.messages,
                        model_name=MODEL_NAME
                    )

                st.session_state.last_executed_tools = tool_traces
                st.session_state.last_voice_response = voice_answer

                with st.spinner("Synthesizing voice response audio..."):
                    st.session_state.last_response_audio = text_to_speech_wav(voice_answer)
                st.rerun()

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to local Ollama. Ensure Ollama daemon is active.")
        except Exception as error:
            st.error(f"Voice DevOps error: {error}")

    # Tool Execution Inspection Card
    if st.session_state.last_executed_tools:
        st.divider()
        st.subheader("🛠️ DevOps Tool Invocations")
        for trace in st.session_state.last_executed_tools:
            with st.expander(f"Tool Executed: `{trace['tool']}`", expanded=True):
                st.write("**Arguments:**", trace["arguments"])
                st.json(trace["result"])

    if st.session_state.last_response_audio and os.path.exists(st.session_state.last_response_audio):
        st.divider()
        st.subheader("🔊 Audio Spoken Response")
        st.audio(st.session_state.last_response_audio, format="audio/wav", autoplay=True)

    st.divider()
    if st.button("🗑️ Clear Dialogue & Diagnostics", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are an AI-powered voice DevOps assistant. "
                    "Use tools to inspect system metrics, check processes, test ports, or read logs. "
                    "Always summarize findings clearly, calmly, and concisely in 2 sentences for voice read-out."
                )
            }
        ]
        st.session_state.last_executed_tools = []
        st.session_state.last_voice_response = ""
        st.session_state.last_response_audio = None
        st.rerun()

with col_chat:
    st.subheader("💬 Spoken Dialogue & Agent Trace")
    for msg in st.session_state.messages:
        if msg.get("role") in ["system", "tool"]:
            continue
        with st.chat_message(msg["role"]):
            st.write(msg.get("content", ""))
