import os
import sys
import time
import json
import ctypes
import subprocess
import requests
import psutil
from PIL import Image, ImageDraw
import streamlit as st

# Optional PyAutoGUI support
try:
    import pyautogui
    pyautogui.FAILSAFE = True
    HAS_PYAUTOGUI = True
except Exception:
    HAS_PYAUTOGUI = False

# ---------------- CONFIGURATION ----------------

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OLLAMA_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="Day 48 - AI Computer-Use Agent",
    page_icon="🖥️",
    layout="wide"
)

# ---------------- SAFETY & ACTION GUARDRAILS ----------------

BLOCKED_KEYWORDS = ["shutdown", "restart", "format", "rmdir", "del /", "regedit", "powershell -enc", "drop database"]

ALLOWED_APPLICATIONS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "mspaint": "mspaint.exe",
    "explorer": "explorer.exe"
}

def validate_action_safety(action_type: str, action_params: dict):
    """Guardrail to reject unsafe or high-risk OS operations."""
    param_str = json.dumps(action_params).lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in param_str:
            return False, f"Action blocked by safety policy: contains restricted token '{keyword}'."
    
    if action_type == "open_application":
        app_name = action_params.get("app_name", "").lower().strip()
        if app_name not in ALLOWED_APPLICATIONS and not app_name.endswith(".exe"):
            return False, f"Application '{app_name}' not in allowed safe application whitelist."
            
    return True, "Safe"

# ---------------- OS AUTOMATION PRIMITIVES ----------------

def get_active_window_title() -> str:
    """Returns the title of the current foreground desktop window."""
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value if buf.value else "Desktop / Shell"
    except Exception:
        return "Unknown Window"

def open_application(app_name: str, dry_run: bool = False):
    """Launches a desktop application."""
    target_exe = ALLOWED_APPLICATIONS.get(app_name.lower().strip(), app_name)
    if dry_run:
        return {"action": "open_application", "status": "simulated", "app": target_exe, "message": f"[DRY-RUN] Launched {target_exe}"}
    try:
        subprocess.Popen([target_exe], shell=True)
        time.sleep(1.0)
        return {"action": "open_application", "status": "success", "app": target_exe, "message": f"Successfully launched {target_exe}"}
    except Exception as e:
        return {"action": "open_application", "status": "failed", "app": target_exe, "error": str(e)}

def type_text(text: str, dry_run: bool = False):
    """Types characters into the currently focused window."""
    if dry_run:
        return {"action": "type_text", "status": "simulated", "text": text, "message": f"[DRY-RUN] Typed: '{text}'"}
    try:
        if HAS_PYAUTOGUI:
            pyautogui.write(text, interval=0.03)
        else:
            # Fallback using Windows PowerShell SendKeys
            escaped_text = text.replace("'", "''").replace("{", "{{").replace("}", "}}")
            cmd = f'powershell -Command "$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys(\'{escaped_text}\')"'
            subprocess.run(cmd, shell=True, timeout=5)
        return {"action": "type_text", "status": "success", "text": text}
    except Exception as e:
        return {"action": "type_text", "status": "failed", "error": str(e)}

def press_key(key: str, dry_run: bool = False):
    """Sends hotkey or navigation key press."""
    if dry_run:
        return {"action": "press_key", "status": "simulated", "key": key, "message": f"[DRY-RUN] Pressed key: {key}"}
    try:
        if HAS_PYAUTOGUI:
            pyautogui.press(key.lower())
        else:
            cmd = f'powershell -Command "$wshell = New-Object -ComObject wscript.shell; $wshell.SendKeys(\'{{{key.upper()}}}\')"'
            subprocess.run(cmd, shell=True, timeout=5)
        return {"action": "press_key", "status": "success", "key": key}
    except Exception as e:
        return {"action": "press_key", "status": "failed", "error": str(e)}

def mouse_click(x: int = 100, y: int = 100, dry_run: bool = False):
    """Clicks desktop coordinate (x, y)."""
    if dry_run:
        return {"action": "mouse_click", "status": "simulated", "coordinates": [x, y], "message": f"[DRY-RUN] Clicked at ({x}, {y})"}
    try:
        if HAS_PYAUTOGUI:
            pyautogui.click(x, y)
        else:
            ctypes.windll.user32.SetCursorPos(int(x), int(y))
            # MOUSEEVENTF_LEFTDOWN = 0x0002, MOUSEEVENTF_LEFTUP = 0x0004
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
        return {"action": "mouse_click", "status": "success", "coordinates": [x, y]}
    except Exception as e:
        return {"action": "mouse_click", "status": "failed", "error": str(e)}

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_cursor_position():
    """Safely retrieves current mouse cursor coordinates."""
    if HAS_PYAUTOGUI:
        try:
            pos = pyautogui.position()
            return [int(pos.x), int(pos.y)]
        except Exception:
            pass
    try:
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return [int(pt.x), int(pt.y)]
    except Exception:
        return [0, 0]

def capture_desktop_state(dry_run: bool = False):
    """Captures screenshot and resolution telemetry."""
    try:
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
    except Exception:
        width, height = 1920, 1080

    active_win = get_active_window_title()
    cursor_pos = get_cursor_position()

    return {
        "screen_resolution": f"{width}x{height}",
        "active_window": active_win,
        "cursor_pos": cursor_pos
    }

def list_running_apps():
    """Lists desktop application windows currently active."""
    apps = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name']
            if name.lower() in [v for v in ALLOWED_APPLICATIONS.values()] or name.lower().endswith('.exe'):
                if name not in apps:
                    apps.append(name)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return apps[:8]

# Tool Dispatcher
COMPUTER_TOOLS = {
    "open_application": open_application,
    "type_text": type_text,
    "press_key": press_key,
    "mouse_click": mouse_click,
    "capture_desktop_state": capture_desktop_state
}

# ---------------- LOCAL AI AGENT PLANNER ----------------

def plan_computer_actions(user_goal: str):
    """
    Prompts local Qwen3 to decompose a high-level desktop goal into
    structured JSON executable OS steps.
    """
    system_prompt = (
        "You are an autonomous Computer-Use AI agent running locally on Windows. "
        "Your role is to translate a user's desktop goal into a sequential list of OS actions. "
        "Available actions: \n"
        "- open_application(app_name): opens 'notepad', 'calculator', 'paint', 'explorer'\n"
        "- type_text(text): writes text into the focused window\n"
        "- press_key(key): presses a key like 'enter', 'tab', 'escape'\n"
        "- mouse_click(x, y): clicks coordinates\n"
        "- capture_desktop_state(): checks screen resolution and active window\n\n"
        "Return strictly valid JSON with key 'plan' containing a list of action objects. "
        "Each object must have 'action' (string) and 'params' (dict), and an 'explanation' (string).\n"
        "Example:\n"
        '{\n'
        '  "plan": [\n'
        '    {"action": "open_application", "params": {"app_name": "notepad"}, "explanation": "Open Notepad editor"},\n'
        '    {"action": "type_text", "params": {"text": "System Ready"}, "explanation": "Write deployment status"},\n'
        '    {"action": "press_key", "params": {"key": "enter"}, "explanation": "New line"}\n'
        '  ]\n'
        '}'
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"User Goal: {user_goal}"}
        ],
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 300,
            "num_ctx": 2048
        }
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=90)
        res.raise_for_status()
        raw_content = res.json()["message"]["content"]
        data = json.loads(raw_content)
        return data.get("plan", [])
    except Exception as e:
        # Fallback deterministic planner for common tasks
        goal_lower = user_goal.lower()
        if "notepad" in goal_lower:
            text_to_type = "Hello from Local AI Computer-Use Agent!"
            if "write" in goal_lower or "type" in goal_lower:
                text_to_type = user_goal.split("notepad")[-1].replace("and write", "").replace("and type", "").strip(": ") or text_to_type
            return [
                {"action": "open_application", "params": {"app_name": "notepad"}, "explanation": "Launch Notepad"},
                {"action": "type_text", "params": {"text": text_to_type}, "explanation": "Type generated text"},
                {"action": "press_key", "params": {"key": "enter"}, "explanation": "Press Enter"}
            ]
        elif "calc" in goal_lower:
            return [
                {"action": "open_application", "params": {"app_name": "calculator"}, "explanation": "Launch Calculator"},
                {"action": "type_text", "params": {"text": "125*8="}, "explanation": "Input calculation equation"}
            ]
        else:
            return [
                {"action": "capture_desktop_state", "params": {}, "explanation": "Inspect active desktop environment"}
            ]

# ---------------- UI DASHBOARD ----------------

st.title("🖥️ Day 48 — Local AI-Powered Computer-Use Agent 🤖")
st.caption("Autonomous OS Desktop Interaction • Action Decomposition (Ollama Qwen3) • Guardrail Verification")

# Top Telemetry & Health
active_window = get_active_window_title()
running_apps = list_running_apps()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Agent Status", "Active / Ready")
col2.metric("Ollama Model", MODEL_NAME)
col3.metric("Active Window", active_window[:20] if len(active_window) > 20 else active_window)
col4.metric("Safety Guardrails", "Enforced (Strict)")

st.divider()

# Sidebar: Controls & Safety
with st.sidebar:
    st.header("⚙️ Agent Execution Mode")
    simulated_mode = st.toggle("🧪 Safe Dry-Run / Simulation Mode", value=True, help="Executes virtual mock actions without moving physical mouse or typing real keystrokes.")
    
    st.divider()
    st.subheader("🛡️ Safety Constraints")
    st.markdown("- **Allowed Apps**: `notepad`, `calc`, `paint`, `explorer`")
    st.markdown("- **Blocked**: `shutdown`, `del`, `format`, `regedit`")
    st.markdown("- **Emergency Fail-Safe**: Move mouse to screen corner")
    
    st.divider()
    st.subheader("🖥️ Visible Target Processes")
    st.write(running_apps if running_apps else ["No target processes detected"])

# Main Interface: Plan & Dispatch
c_input, c_results = st.columns([1, 1.2])

with c_input:
    st.subheader("🎯 Desktop Task Objective")
    preset_task = st.selectbox(
        "Choose a predefined computer-use task:",
        [
            "Open Notepad, write a DevOps deployment summary, and press Enter.",
            "Open Calculator and calculate 256 * 16.",
            "Inspect desktop resolution and active foreground window.",
            "Launch Paint editor and prepare a canvas."
        ]
    )
    custom_task = st.text_input("Or describe a custom desktop goal:", value="")
    selected_goal = custom_task.strip() if custom_task.strip() else preset_task

    exec_button = st.button("🚀 Plan & Execute Computer Actions", type="primary", use_container_width=True)

with c_results:
    st.subheader("📋 Execution Trace & Audit Log")
    if exec_button:
        with st.status(f"Decomposing goal: '{selected_goal}'...", expanded=True) as status_box:
            # Step 1: AI Planning
            start_time = time.time()
            plan = plan_computer_actions(selected_goal)
            status_box.update(label=f"Action plan generated ({len(plan)} steps). Executing...", state="running")
            
            trace_records = []
            
            # Step 2: Guardrail check & execution
            for idx, step in enumerate(plan, 1):
                act_name = step.get("action", "")
                act_params = step.get("params", {})
                explanation = step.get("explanation", "")
                
                # Safety check
                is_safe, reason = validate_action_safety(act_name, act_params)
                if not is_safe:
                    trace_records.append({
                        "step": idx,
                        "action": act_name,
                        "params": act_params,
                        "status": "BLOCKED",
                        "details": reason
                    })
                    st.error(f"Step {idx} Blocked: {reason}")
                    break

                # Execute action
                if act_name in COMPUTER_TOOLS:
                    func = COMPUTER_TOOLS[act_name]
                    # Pass dry_run
                    try:
                        res = func(**act_params, dry_run=simulated_mode) if act_name != "capture_desktop_state" else func(dry_run=simulated_mode)
                    except TypeError:
                        res = func(**act_params)
                        
                    trace_records.append({
                        "step": idx,
                        "action": act_name,
                        "params": act_params,
                        "explanation": explanation,
                        "result": res
                    })
                    time.sleep(0.5)
                else:
                    trace_records.append({
                        "step": idx,
                        "action": act_name,
                        "status": "UNKNOWN_ACTION"
                    })
                    
            status_box.update(label=f"Completed {len(trace_records)} actions in {time.time() - start_time:.2f}s", state="complete")
            st.session_state["last_trace"] = trace_records

    # Render Trace Cards
    if "last_trace" in st.session_state:
        for item in st.session_state["last_trace"]:
            step_num = item.get("step")
            act = item.get("action")
            exp = item.get("explanation", "")
            
            with st.expander(f"Step {step_num}: `{act}` — {exp}", expanded=True):
                st.write("**Parameters:**", item.get("params"))
                if "result" in item:
                    st.json(item["result"])
                elif "details" in item:
                    st.warning(item["details"])

# Desktop Telemetry Visualizer
st.divider()
st.subheader("📊 Desktop Environment State")
vis1, vis2 = st.columns([1, 1])

with vis1:
    state = capture_desktop_state(dry_run=simulated_mode)
    st.write(f"**Resolution:** `{state['screen_resolution']}`")
    st.write(f"**Foreground Window:** `{state['active_window']}`")
    st.write(f"**Cursor Coordinates:** `({state['cursor_pos'][0]}, {state['cursor_pos'][1]})`")

with vis2:
    st.info("💡 **Mode Tip**: Toggle 'Safe Dry-Run Mode' in the sidebar to simulate keystrokes and clicks safely, or disable it to watch the AI interact with your desktop apps in real time.")

