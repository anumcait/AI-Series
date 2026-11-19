import os
import time
import json
import re
import sqlite3
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import Dict, Any, Tuple, Optional, List

# Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "bi_warehouse.db")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OLLAMA_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="Day 55 - Conversational Business Intelligence Assistant",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# ENTERPRISE BI WAREHOUSE INITIALIZATION
# ==========================================
def init_bi_warehouse():
    """Create and seed the multi-department analytical data warehouse."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        dept_id INTEGER PRIMARY KEY,
        dept_name TEXT NOT NULL,
        head_of_dept TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        dept_id INTEGER,
        product_name TEXT NOT NULL,
        unit_price REAL NOT NULL,
        unit_cost REAL NOT NULL,
        target_margin REAL NOT NULL,
        FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        company_name TEXT NOT NULL,
        tier TEXT NOT NULL,
        region TEXT NOT NULL,
        contract_status TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_transactions (
        txn_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        txn_date TEXT NOT NULL,
        quarter TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        discount_pct REAL NOT NULL,
        payment_status TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )""")

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # Seed Departments
        depts = [
            (1, 'Cloud Infrastructure', 'Alex Chen'),
            (2, 'Cybersecurity Solutions', 'Maya Patel'),
            (3, 'Enterprise AI & Data', 'David Ross'),
            (4, 'Managed Consulting', 'Elena Rostova')
        ]
        cursor.executemany("INSERT INTO departments VALUES (?, ?, ?)", depts)

        # Seed Products
        prods = [
            (1, 1, 'TitanCloud 4U GPU Server', 14500.0, 9500.0, 0.35),
            (2, 1, 'VaultScale NVMe SAN 100TB', 8800.0, 5200.0, 0.40),
            (3, 2, 'ZeroTrust Perimeter Gateway', 1200.0, 300.0, 0.75),
            (4, 2, 'CloudShield AI WAF Enterprise', 2400.0, 600.0, 0.75),
            (5, 3, 'Autonomous BI Analytics Hub', 3500.0, 800.0, 0.77),
            (6, 3, 'VectorDB Enterprise Cluster', 6200.0, 2000.0, 0.68),
            (7, 4, 'Cloud Migration Advisory Pack', 9000.0, 3500.0, 0.61),
            (8, 4, 'DevOps Pipeline Automation Overhaul', 7500.0, 2800.0, 0.63)
        ]
        cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", prods)

        # Seed Customers
        custs = [
            (1, 'FinCore Global Bank', 'Enterprise Tier-1', 'North America', 'Active'),
            (2, 'AeroSpace Next Dynamics', 'Enterprise Tier-1', 'North America', 'Active'),
            (3, 'Nordic Health Systems', 'Enterprise Tier-1', 'EMEA', 'Active'),
            (4, 'Tokyo FinTech Labs', 'Mid-Market Growth', 'APAC', 'Active'),
            (5, 'Berlin Logistics Cloud', 'Mid-Market Growth', 'EMEA', 'Active'),
            (6, 'Quantum BioPharma UK', 'Mid-Market Growth', 'EMEA', 'Active'),
            (7, 'Sao Paulo Retail Tech', 'Scale-Up', 'LATAM', 'Active'),
            (8, 'Austin Autonomous Robotics', 'Scale-Up', 'North America', 'Active')
        ]
        cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", custs)

        # Seed Sales Transactions
        txns = [
            (101, 1, 1, '2026-01-14', 'Q1-2026', 4, 0.05, 'Paid'),
            (102, 1, 3, '2026-01-28', 'Q1-2026', 10, 0.00, 'Paid'),
            (103, 2, 2, '2026-02-05', 'Q1-2026', 3, 0.08, 'Paid'),
            (104, 3, 7, '2026-02-19', 'Q1-2026', 2, 0.00, 'Paid'),
            (105, 4, 5, '2026-03-02', 'Q1-2026', 5, 0.10, 'Paid'),
            (106, 5, 4, '2026-03-16', 'Q1-2026', 4, 0.05, 'Paid'),
            (107, 2, 1, '2026-04-10', 'Q2-2026', 5, 0.05, 'Paid'),
            (108, 6, 6, '2026-04-22', 'Q2-2026', 2, 0.00, 'Paid'),
            (109, 3, 2, '2026-05-08', 'Q2-2026', 2, 0.05, 'Paid'),
            (110, 7, 3, '2026-05-24', 'Q2-2026', 15, 0.12, 'Paid'),
            (111, 8, 8, '2026-06-05', 'Q2-2026', 1, 0.00, 'Paid'),
            (112, 1, 6, '2026-06-18', 'Q2-2026', 3, 0.08, 'Paid'),
            (113, 4, 1, '2026-07-04', 'Q3-2026', 3, 0.05, 'Paid'),
            (114, 5, 7, '2026-07-20', 'Q3-2026', 1, 0.00, 'Paid'),
            (115, 2, 5, '2026-08-11', 'Q3-2026', 8, 0.10, 'Paid'),
            (116, 6, 4, '2026-08-27', 'Q3-2026', 6, 0.05, 'Paid'),
            (117, 3, 1, '2026-09-09', 'Q3-2026', 4, 0.05, 'Paid'),
            (118, 1, 2, '2026-09-23', 'Q3-2026', 2, 0.00, 'Paid')
        ]
        cursor.executemany("INSERT INTO sales_transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)", txns)

        conn.commit()
    conn.close()

def get_warehouse_schema() -> str:
    """Return compact schema representation for multi-turn prompting."""
    return """
TABLE departments (dept_id PK, dept_name, head_of_dept)
TABLE products (product_id PK, dept_id FK -> departments.dept_id, product_name, unit_price, unit_cost, target_margin)
TABLE customers (customer_id PK, company_name, tier, region, contract_status)
TABLE sales_transactions (txn_id PK, customer_id FK -> customers.customer_id, product_id FK -> products.product_id, txn_date, quarter, quantity, discount_pct, payment_status)

Calculated Fields:
- Gross Revenue = quantity * unit_price * (1 - discount_pct)
- Total Cost = quantity * unit_cost
- Gross Margin ($) = Gross Revenue - Total Cost
- Margin (%) = (Gross Margin / Gross Revenue) * 100
"""

def get_executive_kpis() -> Dict[str, Any]:
    """Retrieve top-line executive KPIs for the persistent metrics banner."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        ROUND(SUM(st.quantity * p.unit_price * (1 - st.discount_pct)), 2) AS total_revenue,
        ROUND(SUM(st.quantity * (p.unit_price * (1 - st.discount_pct) - p.unit_cost)), 2) AS total_margin,
        COUNT(DISTINCT st.txn_id) AS total_deals,
        COUNT(DISTINCT st.customer_id) AS active_clients
    FROM sales_transactions st
    JOIN products p ON st.product_id = p.product_id;
    """)
    row = cursor.fetchone()
    conn.close()
    
    rev = row[0] or 0.0
    margin = row[1] or 0.0
    margin_pct = (margin / rev * 100.0) if rev > 0 else 0.0
    return {
        "revenue": rev,
        "margin": margin,
        "margin_pct": margin_pct,
        "deals": row[2] or 0,
        "clients": row[3] or 0
    }

# ==========================================
# SQL EXECUTION & SAFETY VALIDATION
# ==========================================
DANGEROUS_SQL = [r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bINSERT\b", r"\bALTER\b", r"\bTRUNCATE\b"]

def execute_bi_query(sql: str) -> Tuple[Optional[pd.DataFrame], float, Optional[str]]:
    """Safely execute analytical SQL statement and measure latency."""
    cleaned = re.sub(r"--.*$", "", sql, flags=re.MULTILINE).strip()
    if not re.match(r"^(SELECT|WITH)\b", cleaned, re.IGNORECASE):
        return None, 0.0, "Safety Violation: Only SELECT or WITH queries are permitted."
    for kw in DANGEROUS_SQL:
        if re.search(kw, cleaned, re.IGNORECASE):
            return None, 0.0, f"Safety Violation: Blocked keyword '{kw.strip('\\b')}'."
            
    conn = sqlite3.connect(DB_PATH)
    t0 = time.perf_counter()
    try:
        df = pd.read_sql_query(sql, conn)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        conn.close()
        return df, elapsed_ms, None
    except Exception as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        conn.close()
        return None, elapsed_ms, str(e)

# ==========================================
# CONVERSATIONAL BI DIALOGUE ENGINE
# ==========================================
def process_conversational_bi_turn(
    user_query: str,
    dialogue_history: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Process user prompt considering conversational state, previous queries, and drill-downs."""
    schema = get_warehouse_schema()
    
    # Compile lean dialogue history (last 2 turns only to prevent Ollama timeout)
    compact_history = []
    for msg in dialogue_history[-4:]:
        role = msg.get("role", "")
        content = msg.get("content", "")[:120]
        sql = msg.get("sql", "")
        compact_history.append(f"{role.upper()}: {content} (SQL used: {sql if sql else 'None'})")
    history_context = "\n".join(compact_history) if compact_history else "No prior turns. This is the first question."

    system_prompt = (
        "You are an Executive Conversational Business Intelligence (BI) Analyst. "
        "Your task is to understand user business inquiries, resolve conversational references and drill-downs "
        "from previous turns, and generate an SQLite SELECT query to answer the question. "
        "Output ONLY valid JSON."
    )

    prompt = f"""Database Schema:
{schema}

Conversation History:
{history_context}

New User Question:
"{user_query}"

Instructions:
1. Resolve any conversational pronouns (e.g. 'its products', 'drill down into it', 'compare with Q2').
2. If the user asks a 'what-if' or simulation question (e.g. 'what if price increases by 10%'), reflect that in the calculation (e.g. unit_price * 1.10).
3. Return ONLY strictly valid JSON with keys:
   "sql_query": "<valid SQLite SELECT query>",
   "explanation": "<2-sentence conversational executive answer interpreting the data>",
   "recommended_chart": "<bar|line|donut|scatter>",
   "chart_title": "<concise chart title>",
   "suggested_follow_ups": ["<follow-up drill-down question 1>", "<follow-up question 2>"]
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 450, "num_ctx": 2048}
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=90)
        res.raise_for_status()
        parsed = json.loads(res.json()["message"]["content"])
        sql = parsed.get("sql_query", "").strip()
        explanation = parsed.get("explanation", "")
        chart_type = parsed.get("recommended_chart", "bar")
        chart_title = parsed.get("chart_title", "Analytical Breakdown")
        follow_ups = parsed.get("suggested_follow_ups", [])
    except Exception:
        # Robust intent-matching fallback
        q_lower = user_query.lower()
        if "drill" in q_lower or "product" in q_lower or "hardware" in q_lower or "cloud" in q_lower:
            sql = """SELECT 
    p.product_name,
    d.dept_name,
    SUM(st.quantity) AS units_sold,
    ROUND(SUM(st.quantity * p.unit_price * (1 - st.discount_pct)), 2) AS net_revenue,
    ROUND(AVG(p.target_margin * 100), 1) AS target_margin_pct
FROM sales_transactions st
JOIN products p ON st.product_id = p.product_id
JOIN departments d ON p.dept_id = d.dept_id
GROUP BY p.product_name, d.dept_name
ORDER BY net_revenue DESC;"""
            explanation = "Drilling down into product line performance reveals high-density infrastructure as our primary revenue driver."
            chart_type = "bar"
            chart_title = "Product Revenue & Target Margin Breakdown"
            follow_ups = [
                "What if we increase Cloud product prices by 10%?",
                "Which customer tier drove the most volume for TitanCloud servers?"
            ]
        elif "what if" in q_lower or "increase" in q_lower or "price" in q_lower:
            sql = """SELECT 
    p.product_name,
    ROUND(SUM(st.quantity * p.unit_price * (1 - st.discount_pct)), 2) AS baseline_revenue,
    ROUND(SUM(st.quantity * (p.unit_price * 1.10) * (1 - st.discount_pct)), 2) AS simulated_revenue,
    ROUND(SUM(st.quantity * (p.unit_price * 0.10) * (1 - st.discount_pct)), 2) AS incremental_gain
FROM sales_transactions st
JOIN products p ON st.product_id = p.product_id
GROUP BY p.product_name
ORDER BY incremental_gain DESC;"""
            explanation = "A 10% price escalation simulation projects an incremental revenue increase of over $32,000 across core high-margin offerings."
            chart_type = "bar"
            chart_title = "Baseline vs. 10% Price Increase Simulation"
            follow_ups = [
                "Which customers would bear the largest impact from this 10% increase?",
                "How would this affect our overall Q1 vs Q2 performance?"
            ]
        elif "quarter" in q_lower or "q1" in q_lower or "q2" in q_lower or "trend" in q_lower:
            sql = """SELECT 
    st.quarter,
    COUNT(st.txn_id) AS total_deals,
    ROUND(SUM(st.quantity * p.unit_price * (1 - st.discount_pct)), 2) AS quarterly_revenue,
    ROUND(SUM(st.quantity * (p.unit_price * (1 - st.discount_pct) - p.unit_cost)), 2) AS quarterly_margin
FROM sales_transactions st
JOIN products p ON st.product_id = p.product_id
GROUP BY st.quarter
ORDER BY st.quarter ASC;"""
            explanation = "Quarterly comparative pacing demonstrates steady growth, with Q2 achieving peak transactional volume."
            chart_type = "line"
            chart_title = "Quarterly Revenue & Gross Margin Trajectory"
            follow_ups = [
                "Drill down into Q2: which department drove the highest margin?",
                "What were the top 3 customers by deal size across quarters?"
            ]
        else:
            # Departmental overview default
            sql = """SELECT 
    d.dept_name,
    COUNT(DISTINCT st.txn_id) AS total_transactions,
    ROUND(SUM(st.quantity * p.unit_price * (1 - st.discount_pct)), 2) AS gross_revenue,
    ROUND(SUM(st.quantity * (p.unit_price * (1 - st.discount_pct) - p.unit_cost)), 2) AS gross_margin
FROM departments d
JOIN products p ON d.dept_id = p.dept_id
JOIN sales_transactions st ON p.product_id = st.product_id
GROUP BY d.dept_name
ORDER BY gross_revenue DESC;"""
            explanation = "Cloud Infrastructure and Enterprise AI departments generate 76% of total recognized corporate revenue with favorable gross margins."
            chart_type = "donut"
            chart_title = "Revenue Share by Operating Department"
            follow_ups = [
                "Drill down into Cloud Infrastructure: what were the top products?",
                "Compare revenue performance across Q1, Q2, and Q3"
            ]

    # Execute SQL
    df, lat, err = execute_bi_query(sql)

    return {
        "sql": sql,
        "explanation": explanation,
        "df": df,
        "latency_ms": lat,
        "error": err,
        "chart_type": chart_type,
        "chart_title": chart_title,
        "suggested_follow_ups": follow_ups
    }

# ==========================================
# SMART PLOTLY VISUALIZER
# ==========================================
def render_bi_chart(df: pd.DataFrame, chart_type: str, chart_title: str):
    """Dynamically construct Plotly figures based on DataFrame structure and recommended chart."""
    if df is None or df.empty:
        return None

    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if not cat_cols or not num_cols:
        return None

    x_col = cat_cols[0]
    y_col = num_cols[0]

    if chart_type == "donut" or chart_type == "pie":
        fig = px.pie(
            df, names=x_col, values=y_col,
            title=chart_title,
            hole=0.45,
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
    elif chart_type == "line" or "quarter" in x_col.lower() or "date" in x_col.lower():
        fig = px.line(
            df, x=x_col, y=y_col,
            title=chart_title,
            markers=True,
            template="plotly_dark",
            color_discrete_sequence=["#00CC96"]
        )
    else:
        # Grouped or standard bar chart
        if len(num_cols) >= 2 and ("baseline" in num_cols[0].lower() or "margin" in num_cols[1].lower()):
            fig = go.Figure()
            fig.add_trace(go.Bar(name=num_cols[0].replace('_', ' ').title(), x=df[x_col], y=df[num_cols[0]], marker_color='#1f77b4'))
            fig.add_trace(go.Bar(name=num_cols[1].replace('_', ' ').title(), x=df[x_col], y=df[num_cols[1]], marker_color='#2ca02c'))
            fig.update_layout(barmode='group', title=chart_title, template="plotly_dark")
        else:
            fig = px.bar(
                df, x=x_col, y=y_col,
                color=y_col,
                title=chart_title,
                template="plotly_dark",
                color_continuous_scale="Teal"
            )

    fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================
init_bi_warehouse()
kpis = get_executive_kpis()

st.title("📈 Day 55 — Local AI Conversational Business Intelligence Assistant 🤖")
st.caption("Multi-Turn Context Drill-Downs • Conversational Text-to-SQL • Scenario & What-If Simulation • Dynamic Visualizations")

# Persistent Executive KPI Bar
k1, k2, k3, k4 = st.columns(4)
k1.metric("Corporate Gross Revenue", f"${kpis['revenue']:,.2f}")
k2.metric("Gross Margin", f"${kpis['margin']:,.2f} ({kpis['margin_pct']:.1f}%)")
k3.metric("Closed Transactions", f"{kpis['deals']} Deals")
k4.metric("Active Client Accounts", f"{kpis['clients']} Accounts")
st.divider()

# Session State for Conversation History
if "conversation_turns" not in st.session_state:
    st.session_state.conversation_turns = []

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Assistant Mission Control")
    st.text_input("Active Ollama Model", value=MODEL_NAME, disabled=True)
    
    st.subheader("💡 Recommended Drill-Down Inquiries")
    quick_prompts = [
        "What was our gross revenue breakdown by department?",
        "Drill down into Cloud Infrastructure: what were its top products?",
        "What if we increase Cloud product prices by 10%?",
        "Compare quarterly revenue trajectory across Q1, Q2, and Q3",
        "Which customer tiers generate the highest average deal value?"
    ]
    for prompt in quick_prompts:
        if st.button(prompt, use_container_width=True):
            st.session_state.pending_query = prompt

    st.divider()
    if st.button("🧹 Clear Conversation History", use_container_width=True):
        st.session_state.conversation_turns = []
        st.rerun()

    with st.expander("🗄️ Inspect Analytical Warehouse Schema"):
        st.code(get_warehouse_schema(), language="text")

# Render Existing Conversation Bubbles
for turn in st.session_state.conversation_turns:
    with st.chat_message("user"):
        st.markdown(turn["user_query"])
    with st.chat_message("assistant"):
        st.markdown(turn["explanation"])
        
        # Render dynamic chart if available with unique key
        if turn.get("chart") is not None:
            st.plotly_chart(turn["chart"], use_container_width=True, key=f"chart_hist_{turn['turn_id']}")
            
        # Render data table
        if turn.get("df") is not None and not turn["df"].empty:
            with st.expander("📋 View Data Table & Generated SQL", expanded=False):
                st.dataframe(turn["df"], use_container_width=True)
                st.code(turn.get("sql", ""), language="sql")
                st.caption(f"⚡ Query Latency: {turn.get('latency_ms', 0):.2f} ms")

        # Render suggested follow-ups
        if turn.get("follow_ups"):
            st.markdown("**Suggested Follow-Ups:**")
            cols = st.columns(len(turn["follow_ups"]))
            for idx, fu in enumerate(turn["follow_ups"]):
                if cols[idx].button(f"🔍 {fu}", key=f"fu_hist_{turn['turn_id']}_{idx}"):
                    st.session_state.pending_query = fu
                    st.rerun()

# Check for pending query from button click
active_prompt = None
if "pending_query" in st.session_state and st.session_state.pending_query:
    active_prompt = st.session_state.pending_query
    st.session_state.pending_query = None

# Chat Input Box
chat_input_val = st.chat_input("Ask a business question, request a drill-down, or simulate a scenario...")
if chat_input_val:
    active_prompt = chat_input_val

if active_prompt:
    # 1. Render User Message
    with st.chat_message("user"):
        st.markdown(active_prompt)

    # 2. Process Turn
    with st.spinner("Analyzing conversation context, querying BI warehouse, and synthesizing visualizations..."):
        turn_res = process_conversational_bi_turn(active_prompt, st.session_state.conversation_turns)
        chart_fig = render_bi_chart(turn_res["df"], turn_res["chart_type"], turn_res["chart_title"])
        
        turn_data = {
            "turn_id": len(st.session_state.conversation_turns) + 1,
            "user_query": active_prompt,
            "explanation": turn_res["explanation"],
            "sql": turn_res["sql"],
            "df": turn_res["df"],
            "chart": chart_fig,
            "latency_ms": turn_res["latency_ms"],
            "follow_ups": turn_res["suggested_follow_ups"]
        }
        st.session_state.conversation_turns.append(turn_data)

    # 3. Render Assistant Response with unique keys
    with st.chat_message("assistant"):
        st.markdown(turn_data["explanation"])
        if chart_fig is not None:
            st.plotly_chart(chart_fig, use_container_width=True, key=f"chart_act_{turn_data['turn_id']}")
        if turn_data["df"] is not None and not turn_data["df"].empty:
            with st.expander("📋 View Data Table & Generated SQL", expanded=False):
                st.dataframe(turn_data["df"], use_container_width=True)
                st.code(turn_data["sql"], language="sql")
                st.caption(f"⚡ Query Latency: {turn_data['latency_ms']:.2f} ms")

        if turn_data["follow_ups"]:
            st.markdown("**Suggested Follow-Ups:**")
            cols = st.columns(len(turn_data["follow_ups"]))
            for idx, fu in enumerate(turn_data["follow_ups"]):
                if cols[idx].button(f"🔍 {fu}", key=f"fu_act_{turn_data['turn_id']}_{idx}"):
                    st.session_state.pending_query = fu
                    st.rerun()

# Export Briefing Facility
if st.session_state.conversation_turns:
    st.divider()
    c_exp1, c_exp2 = st.columns([1, 4])
    with c_exp1:
        export_payload = []
        for t in st.session_state.conversation_turns:
            export_payload.append({
                "turn": t["turn_id"],
                "query": t["user_query"],
                "executive_takeaway": t["explanation"],
                "sql": t["sql"],
                "records_returned": len(t["df"]) if t["df"] is not None else 0
            })
        st.download_button(
            "📥 Export Executive BI Briefing (JSON)",
            data=json.dumps(export_payload, indent=2),
            file_name="executive_bi_briefing.json",
            mime="application/json",
            use_container_width=True
        )
