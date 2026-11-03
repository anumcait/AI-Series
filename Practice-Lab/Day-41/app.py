import os
import time
import sqlite3
import threading
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import psutil
import requests
import streamlit as st
import plotly.express as px

from sklearn.ensemble import IsolationForest
from streamlit_autorefresh import st_autorefresh

# ---------------- CONFIGURATION ----------------

DB = "monitoring.db"
INTERVAL = 3
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:4b"

THRESHOLDS = {
    "cpu": 85,
    "memory": 85,
    "disk": 90
}

# ---------------- DATABASE ----------------

def connect_db():
    con = sqlite3.connect(DB, timeout=10)
    con.execute("PRAGMA journal_mode=WAL")
    return con


def initialize_db():
    with connect_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu REAL,
                memory REAL,
                disk REAL,
                net_recv REAL,
                net_sent REAL
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                severity TEXT,
                metric TEXT,
                value REAL,
                reason TEXT
            )
        """)


def get_metrics(limit=200):
    with connect_db() as con:
        return pd.read_sql_query(
            "SELECT * FROM metrics ORDER BY id DESC LIMIT ?",
            con, params=(limit,)
        ).sort_values("id")


def get_alerts(limit=100):
    with connect_db() as con:
        return pd.read_sql_query(
            "SELECT * FROM alerts ORDER BY id DESC LIMIT ?",
            con, params=(limit,)
        )


# ---------------- ANOMALY DETECTION ----------------

def detect_anomalies(current, history):
    findings = []

    # 1. Configurable threshold detection
    for metric, threshold in THRESHOLDS.items():
        value = current[metric]

        if value >= threshold:
            severity = "CRITICAL" if value >= 95 else "WARNING"

            findings.append({
                "severity": severity,
                "metric": metric,
                "value": value,
                "reason": (
                    f"{metric.upper()} utilization is "
                    f"{value:.1f}%, above the {threshold}% threshold."
                )
            })

    # 2. Statistical detection using rolling history
    if len(history) >= 20:
        for metric in ["cpu", "memory", "disk"]:
            values = history[metric].astype(float)

            mean = values.mean()
            std = values.std()

            if std > 0:
                z_score = abs((current[metric] - mean) / std)

                if z_score >= 3:
                    findings.append({
                        "severity": "WARNING",
                        "metric": metric,
                        "value": current[metric],
                        "reason": (
                            f"{metric.upper()} is unusually different "
                            f"from its recent baseline "
                            f"(Z-score: {z_score:.2f})."
                        )
                    })

    # 3. Machine-learning detection using Isolation Forest
    features = ["cpu", "memory", "disk", "net_recv", "net_sent"]

    if len(history) >= 50:
        training = history[features].astype(float).tail(200)
        model = IsolationForest(
            n_estimators=50,
            contamination=0.03,
            random_state=42
        )

        try:
            model.fit(training)
            sample = pd.DataFrame([current])[features]
            prediction = model.predict(sample)[0]

            if prediction == -1:
                findings.append({
                    "severity": "WARNING",
                    "metric": "combined",
                    "value": 0,
                    "reason": (
                        "Isolation Forest detected an unusual "
                        "combination of infrastructure metrics."
                    )
                })
        except ValueError:
            pass

    return findings


# ---------------- MONITORING COLLECTOR ----------------

class Monitor:

    def __init__(self):
        self.running = False
        self.thread = None
        self.last_alert = {}

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(
            target=self.collect_loop,
            daemon=True
        )
        self.thread.start()

    def collect_loop(self):
        # First CPU measurement initializes psutil's CPU counter.
        psutil.cpu_percent(interval=None)

        previous_net = psutil.net_io_counters()
        previous_time = time.monotonic()

        while self.running:
            try:
                now = time.monotonic()
                current_net = psutil.net_io_counters()

                elapsed = max(now - previous_time, 0.001)

                recv_rate = (
                    current_net.bytes_recv - previous_net.bytes_recv
                ) / elapsed / (1024 * 1024)

                sent_rate = (
                    current_net.bytes_sent - previous_net.bytes_sent
                ) / elapsed / (1024 * 1024)

                previous_net = current_net
                previous_time = now

                disk_path = Path.home().anchor or os.path.abspath(os.sep)

                current = {
                    "cpu": psutil.cpu_percent(interval=None),
                    "memory": psutil.virtual_memory().percent,
                    "disk": psutil.disk_usage(disk_path).percent,
                    "net_recv": max(recv_rate, 0),
                    "net_sent": max(sent_rate, 0)
                }

                timestamp = datetime.now(timezone.utc).isoformat()

                # Read historical metrics before saving current sample.
                history = get_metrics(200)

                findings = detect_anomalies(current, history)

                with connect_db() as con:
                    con.execute("""
                        INSERT INTO metrics
                        (timestamp, cpu, memory, disk, net_recv, net_sent)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        timestamp,
                        current["cpu"],
                        current["memory"],
                        current["disk"],
                        current["net_recv"],
                        current["net_sent"]
                    ))

                    for finding in findings:
                        key = finding["metric"]
                        last = self.last_alert.get(key, 0)

                        # Prevent repeated alerts for the same metric.
                        if time.monotonic() - last >= 60:
                            con.execute("""
                                INSERT INTO alerts
                                (timestamp, severity, metric, value, reason)
                                VALUES (?, ?, ?, ?, ?)
                            """, (
                                timestamp,
                                finding["severity"],
                                key,
                                finding["value"],
                                finding["reason"]
                            ))

                            self.last_alert[key] = time.monotonic()

            except Exception as error:
                print("Monitoring error:", error)

            time.sleep(INTERVAL)


@st.cache_resource
def get_monitor():
    monitor = Monitor()
    monitor.start()
    return monitor


# ---------------- AI EXPLANATION ----------------

def ask_ollama(metrics, alerts):
    prompt = f"""
You are an infrastructure monitoring assistant.

Analyze the following measured system metrics and alerts.

METRICS:
{metrics}

DETECTED ALERTS:
{alerts}

Provide:
1. Current infrastructure condition.
2. Evidence from the supplied measurements.
3. Possible explanations, clearly marked as hypotheses.
4. Recommended investigation steps.
5. Safe corrective actions.

Do not claim that a root cause is confirmed without evidence.
Do not recommend destructive commands or automatic production changes.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]


# ---------------- DASHBOARD ----------------

st.set_page_config(
    page_title="Day 41 - AI Infrastructure Monitor",
    page_icon="📊",
    layout="wide"
)

initialize_db()
get_monitor()

st_autorefresh(interval=INTERVAL * 1000, key="live_refresh")

st.title("📊 Local AI Infrastructure Monitor")
st.caption("Live system monitoring | Anomaly detection | AI investigation")

metrics_df = get_metrics(200)
alerts_df = get_alerts(100)

if metrics_df.empty:
    st.info("Waiting for the first system measurement...")
    st.stop()

latest = metrics_df.iloc[-1]

# Current infrastructure metrics
c1, c2, c3, c4 = st.columns(4)

c1.metric("CPU Usage", f"{latest['cpu']:.1f}%")
c2.metric("Memory Usage", f"{latest['memory']:.1f}%")
c3.metric("Disk Usage", f"{latest['disk']:.1f}%")
c4.metric(
    "Network Receive",
    f"{latest['net_recv']:.3f} MB/s"
)

st.caption(
    f"Last measurement: {latest['timestamp']} | "
    f"Collection interval: {INTERVAL} seconds"
)

# Metric charts
st.subheader("Infrastructure Performance")

chart_data = metrics_df.tail(100)

fig = px.line(
    chart_data,
    x="timestamp",
    y=["cpu", "memory", "disk"],
    title="CPU, Memory and Disk Usage"
)

st.plotly_chart(fig, use_container_width=True)

network_fig = px.line(
    chart_data,
    x="timestamp",
    y=["net_recv", "net_sent"],
    title="Network Throughput (MB/s)"
)

st.plotly_chart(network_fig, use_container_width=True)

# Recent alerts
st.subheader("🚨 Detected Anomalies")

if alerts_df.empty:
    st.success("No anomalies have been recorded yet.")
else:
    st.dataframe(
        alerts_df.drop(columns=["id"]),
        use_container_width=True,
        hide_index=True
    )

# Disk capacity estimate
st.subheader("📈 Disk Capacity Trend")

if len(metrics_df) >= 10:
    recent = metrics_df.tail(30).copy()

    recent["minutes"] = (
        pd.to_datetime(recent["timestamp"]).astype("int64")
        / 60_000_000_000
    )

    slope = np.polyfit(recent["minutes"], recent["disk"], 1)[0]

    if slope > 0.001:
        remaining = max(100 - latest["disk"], 0)
        hours = remaining / (slope * 60)

        st.write(
            f"Estimated time to 100% disk usage: "
            f"{hours:.1f} hours, assuming the recent growth rate continues."
        )
    else:
        st.write("No meaningful upward disk usage trend detected.")
else:
    st.write("Collecting more measurements before estimating a trend.")

# AI investigation
st.subheader("🤖 AI Infrastructure Investigation")

if st.button("Analyze Current Infrastructure with Qwen3"):
    if not alerts_df.empty:
        alert_context = alerts_df.head(10).to_dict("records")
    else:
        alert_context = "No recorded alerts."

    metric_context = latest.to_dict()

    with st.spinner("Qwen3 is analyzing the infrastructure..."):
        try:
            answer = ask_ollama(metric_context, alert_context)
            st.markdown(answer)
        except requests.exceptions.ConnectionError:
            st.error("Ollama is unavailable. Start Ollama and try again.")
        except Exception as error:
            st.error(f"AI analysis failed: {error}")

# Export data
st.subheader("📥 Export Monitoring Data")

csv = metrics_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Metrics CSV",
    data=csv,
    file_name="infrastructure_metrics.csv",
    mime="text/csv"
)

if not alerts_df.empty:
    alert_csv = alerts_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Incident Report CSV",
        data=alert_csv,
        file_name="infrastructure_alerts.csv",
        mime="text/csv"
    )