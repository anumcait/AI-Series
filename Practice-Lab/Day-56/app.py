import os
import time
import json
import re
import sqlite3
import requests
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import Dict, Any, Tuple, Optional, List

# Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), "benchmark_vault.db")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OLLAMA_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="Day 56 - SQL Query Evaluation & Benchmarking Platform",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# ENTERPRISE BENCHMARK DATABASE SETUP
# ==========================================
def init_benchmark_database():
    """Create and seed a high-volume multi-table database for SQL evaluation."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        dept_id INTEGER PRIMARY KEY,
        dept_name TEXT NOT NULL,
        cost_center TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        dept_id INTEGER,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        unit_price REAL NOT NULL,
        unit_cost REAL NOT NULL,
        FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        company_name TEXT NOT NULL,
        tier TEXT NOT NULL,
        country TEXT NOT NULL,
        status TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL,
        total_amount REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        discount REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )""")

    cursor.execute("SELECT COUNT(*) FROM orders")
    count = cursor.fetchone()[0]
    if count < 500:
        # Seed 5 Departments
        depts = [
            (1, 'Enterprise Cloud Infrastructure', 'CC-101'),
            (2, 'Cybersecurity Engineering', 'CC-202'),
            (3, 'Enterprise AI & Data Platforms', 'CC-303'),
            (4, 'Managed Cloud Services', 'CC-404'),
            (5, 'Autonomous DevOps Tooling', 'CC-505')
        ]
        cursor.executemany("INSERT OR REPLACE INTO departments VALUES (?, ?, ?)", depts)

        # Seed 20 Products
        prods = []
        for i in range(1, 21):
            d_id = ((i - 1) % 5) + 1
            cat = ["Compute", "Storage", "Security", "Analytics", "Automation"][d_id - 1]
            prods.append((i, d_id, f"Enterprise Tier Product {i}", cat, 500.0 + (i * 250.0), 300.0 + (i * 120.0)))
        cursor.executemany("INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?, ?)", prods)

        # Seed 100 Customers
        tiers = ['Enterprise-Elite', 'Corporate-Growth', 'Mid-Market-Standard']
        countries = ['USA', 'Germany', 'United Kingdom', 'Japan', 'Singapore', 'Canada', 'Australia']
        custs = []
        for i in range(1, 101):
            custs.append((i, f"Global Enterprise Client {i}", tiers[i % 3], countries[i % len(countries)], 'Active'))
        cursor.executemany("INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?, ?)", custs)

        # Seed 1000 Orders and 3000 Order Items
        orders_batch = []
        items_batch = []
        item_id = 1
        for o_id in range(1, 1001):
            c_id = ((o_id * 7) % 100) + 1
            month = ((o_id % 12) + 1)
            day = ((o_id % 28) + 1)
            date_str = f"2026-{month:02d}-{day:02d}"
            status = 'Completed' if (o_id % 10) != 0 else 'Pending'
            amt = (o_id * 150.0) % 25000 + 1200.0
            orders_batch.append((o_id, c_id, date_str, status, round(amt, 2)))

            # 2 to 4 items per order
            num_items = (o_id % 3) + 2
            for _ in range(num_items):
                p_id = ((item_id * 13) % 20) + 1
                qty = (item_id % 5) + 1
                u_price = 500.0 + (p_id * 250.0)
                disc = 0.05 if (item_id % 4 == 0) else 0.0
                items_batch.append((item_id, o_id, p_id, qty, u_price, disc))
                item_id += 1

        cursor.executemany("INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?)", orders_batch)
        cursor.executemany("INSERT OR REPLACE INTO order_items VALUES (?, ?, ?, ?, ?, ?)", items_batch)

        # Baseline Index
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_cust ON orders(customer_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);")

        conn.commit()
    conn.close()

# ==========================================
# PRE-BUILT EVALUATION BENCHMARK SUITE
# ==========================================
BENCHMARK_SCENARIOS = {
    "1. Revenue Aggregation by Customer Tier": {
        "description": "Calculate total spending, order count, and average order value grouped by customer tier for completed orders.",
        "reference_sql": """SELECT 
    c.tier,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS gross_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.tier
ORDER BY gross_revenue DESC;""",
        "candidate_sql": """SELECT 
    c.tier,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.total_amount), 2) AS gross_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'Completed'
GROUP BY c.tier
ORDER BY gross_revenue DESC;""",
        "category": "Aggregation & Joins"
    },
    "2. Subquery Anti-Pattern vs. Direct Join": {
        "description": "Identify products that generated over $50,000 in gross sales with total units sold.",
        "reference_sql": """SELECT 
    p.product_name,
    p.category,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS total_sales
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, p.category
HAVING total_sales > 50000
ORDER BY total_sales DESC;""",
        "candidate_sql": """SELECT 
    p.product_name,
    p.category,
    (SELECT SUM(oi.quantity) FROM order_items oi WHERE oi.product_id = p.product_id) AS total_units_sold,
    ROUND((SELECT SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) FROM order_items oi WHERE oi.product_id = p.product_id), 2) AS total_sales
FROM products p
WHERE (SELECT SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) FROM order_items oi WHERE oi.product_id = p.product_id) > 50000
ORDER BY total_sales DESC;""",
        "category": "Query Architecture & Correlated Subqueries"
    },
    "3. High-Value Orders with Customer Country Filtering": {
        "description": "List all completed orders exceeding $15,000 originating from Germany or the USA.",
        "reference_sql": """SELECT 
    o.order_id,
    c.company_name,
    c.country,
    o.order_date,
    o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Completed' 
  AND o.total_amount > 15000.0
  AND c.country IN ('USA', 'Germany')
ORDER BY o.total_amount DESC;""",
        "candidate_sql": """SELECT 
    o.order_id,
    c.company_name,
    c.country,
    o.order_date,
    o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Completed' 
  AND (c.country = 'USA' OR c.country = 'Germany')
  AND o.total_amount > 15000.0
ORDER BY o.total_amount DESC;""",
        "category": "Predicate Filtering & Index Access"
    }
}

# ==========================================
# CORE EVALUATION & BENCHMARKING ENGINES
# ==========================================
def evaluate_result_set_equivalence(df_ref: pd.DataFrame, df_cand: pd.DataFrame) -> Dict[str, Any]:
    """Evaluate whether candidate SQL output is equivalent to reference ground truth."""
    if df_ref is None or df_cand is None:
        return {"equivalent": False, "score": 0.0, "reason": "One or both queries failed execution."}

    # 1. Shape comparison
    shape_match = (df_ref.shape == df_cand.shape)
    col_count_match = len(df_ref.columns) == len(df_cand.columns)
    row_count_match = len(df_ref) == len(df_cand)

    # 2. Schema / column matching (case-insensitive)
    ref_cols = [c.lower().strip() for c in df_ref.columns]
    cand_cols = [c.lower().strip() for c in df_cand.columns]
    cols_match = (ref_cols == cand_cols)

    # 3. Value comparison (normalizing column names & sorting for set equivalence)
    try:
        norm_ref = df_ref.copy()
        norm_cand = df_cand.copy()
        norm_ref.columns = [f"c_{i}" for i in range(len(norm_ref.columns))]
        norm_cand.columns = [f"c_{i}" for i in range(len(norm_cand.columns))]
        
        # Round numeric values to avoid float micro-precision mismatches
        for col in norm_ref.select_dtypes(include=[np.number]).columns:
            norm_ref[col] = norm_ref[col].round(2)
        for col in norm_cand.select_dtypes(include=[np.number]).columns:
            norm_cand[col] = norm_cand[col].round(2)

        # Sort values across all columns to evaluate set equivalence
        sorted_ref = norm_ref.sort_values(by=list(norm_ref.columns)).reset_index(drop=True)
        sorted_cand = norm_cand.sort_values(by=list(norm_cand.columns)).reset_index(drop=True)
        
        exact_value_match = sorted_ref.equals(sorted_cand)
    except Exception:
        exact_value_match = False

    # Score synthesis
    score = 0.0
    if exact_value_match:
        score = 100.0
    elif row_count_match and cols_match:
        score = 80.0
    elif row_count_match:
        score = 60.0
    elif col_count_match:
        score = 40.0
    else:
        score = 20.0

    return {
        "equivalent": exact_value_match,
        "score": score,
        "ref_rows": len(df_ref),
        "cand_rows": len(df_cand),
        "ref_cols": len(df_ref.columns),
        "cand_cols": len(df_cand.columns),
        "cols_matched": cols_match,
        "exact_values": exact_value_match
    }

def profile_query_performance(sql: str, iterations: int = 15) -> Dict[str, Any]:
    """Execute SQL query across multiple iterations to measure robust latency statistics."""
    conn = sqlite3.connect(DB_PATH)
    latencies = []
    
    # Warm-up run
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        cursor.fetchall()
    except Exception as e:
        conn.close()
        return {"error": str(e), "mean_ms": 0.0, "p50_ms": 0.0, "p95_ms": 0.0, "latencies": []}

    # Measured runs
    for _ in range(iterations):
        t0 = time.perf_counter()
        cursor.execute(sql)
        cursor.fetchall()
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000.0)

    conn.close()

    lat_arr = np.array(latencies)
    return {
        "error": None,
        "mean_ms": float(np.mean(lat_arr)),
        "p50_ms": float(np.median(lat_arr)),
        "p95_ms": float(np.percentile(lat_arr, 95)),
        "min_ms": float(np.min(lat_arr)),
        "max_ms": float(np.max(lat_arr)),
        "latencies": latencies
    }

def analyze_query_plan(sql: str) -> Dict[str, Any]:
    """Inspect SQLite execution plan and detect performance bottlenecks."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(f"EXPLAIN QUERY PLAN {sql}")
        plan_rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        conn.close()
        return {"error": str(e), "full_scans": 0, "indexes_used": 0, "plan_text": "", "score": 50.0}

    plan_details = []
    full_scans = 0
    indexes_used = 0
    temp_trees = 0

    for row in plan_rows:
        text = str(row[3])
        plan_details.append(text)
        if "SCAN TABLE" in text.upper() or "SCAN" in text.upper():
            full_scans += 1
        if "USING INDEX" in text.upper() or "SEARCH" in text.upper():
            indexes_used += 1
        if "USE TEMP B-TREE" in text.upper():
            temp_trees += 1

    # Plan Efficiency Score
    plan_score = 100.0 - (full_scans * 25.0) - (temp_trees * 15.0) + (indexes_used * 10.0)
    plan_score = max(10.0, min(100.0, plan_score))

    return {
        "error": None,
        "full_scans": full_scans,
        "indexes_used": indexes_used,
        "temp_trees": temp_trees,
        "plan_text": "\n".join(plan_details),
        "score": plan_score
    }

def compute_overall_sql_health_score(
    equiv_score: float,
    cand_latency: float,
    ref_latency: float,
    plan_score: float
) -> Dict[str, Any]:
    """Calculate composite SQL Health Score (0-100%)."""
    # Latency Score: 100 if faster or equal, decays as candidate gets slower than reference
    if ref_latency > 0:
        ratio = cand_latency / ref_latency
        if ratio <= 1.0:
            latency_score = 100.0
        else:
            latency_score = max(10.0, 100.0 - (ratio - 1.0) * 40.0)
    else:
        latency_score = 100.0

    # Weighted Composite: 40% Accuracy, 30% Latency, 20% Plan Efficiency, 10% Baseline Structure
    health_score = (equiv_score * 0.40) + (latency_score * 0.30) + (plan_score * 0.20) + 10.0
    health_score = round(max(0.0, min(100.0, health_score)), 1)

    grade = "A+" if health_score >= 95 else ("A" if health_score >= 85 else ("B" if health_score >= 70 else ("C" if health_score >= 50 else "F")))

    return {
        "health_score": health_score,
        "grade": grade,
        "equiv_score": equiv_score,
        "latency_score": round(latency_score, 1),
        "plan_score": plan_score
    }

# ==========================================
# LOCAL AI SQL CRITIQUE & ADVISORY ENGINE
# ==========================================
def generate_ai_sql_evaluation(
    scenario_desc: str,
    ref_sql: str,
    cand_sql: str,
    equiv_info: Dict[str, Any],
    perf_comp: Dict[str, Any],
    plan_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Query local Ollama Qwen3 to conduct Senior Principal Database evaluation and code review."""
    system_prompt = (
        "You are a Principal Database Architect and Query Optimization Engineer. "
        "Evaluate the candidate SQL query against the reference gold-standard query, performance benchmarks, "
        "and execution plan. Return strictly valid JSON."
    )

    prompt = f"""Task Requirement: {scenario_desc}

Reference SQL (Ground Truth):
{ref_sql}

Candidate SQL (Under Review):
{cand_sql}

Evaluation Metrics:
- Result Set Equivalent: {equiv_info.get('equivalent')} (Score: {equiv_info.get('score')}/100)
- Reference Latency: {perf_comp.get('ref_p50', 0):.2f} ms vs Candidate Latency: {perf_comp.get('cand_p50', 0):.2f} ms
- Candidate Plan Details: {plan_info.get('plan_text')}

Instructions:
1. Provide an executive architectural critique.
2. Highlight specific strengths, architectural risks (e.g. correlated subqueries, Cartesian risk, missing indexes).
3. Return strictly valid JSON with keys:
   "verdict": "<APPROVED|NEEDS_REVISION|REJECTED>",
   "executive_summary": "<2-sentence review summary>",
   "strengths": ["<strength 1>", "<strength 2>"],
   "risks_and_anti_patterns": ["<risk 1>", "<risk 2>"],
   "optimization_recommendation": "<exact concrete optimization advice>"
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
        return json.loads(res.json()["message"]["content"])
    except Exception:
        # High-load deterministic fallback critique
        is_equiv = equiv_info.get("equivalent", False)
        is_slower = perf_comp.get("cand_p50", 0) > (perf_comp.get("ref_p50", 0) * 1.5)
        
        if is_equiv and not is_slower:
            return {
                "verdict": "APPROVED",
                "executive_summary": "Candidate SQL produces 100% equivalent result sets with competitive latency and clean plan structure.",
                "strengths": ["Result set matches ground truth exactly", "Execution time within acceptable production SLAs"],
                "risks_and_anti_patterns": ["Ensure appropriate covering indexes are maintained in high-throughput environments"],
                "optimization_recommendation": "Query is production-ready. Maintain standard index monitoring."
            }
        elif is_equiv and is_slower:
            return {
                "verdict": "NEEDS_REVISION",
                "executive_summary": "Query produces correct outputs but suffers from suboptimal execution architecture causing significant latency degradation.",
                "strengths": ["Functional correctness verified against ground truth"],
                "risks_and_anti_patterns": ["Repeated subquery evaluation or unindexed scans increase CPU utilization"],
                "optimization_recommendation": "Refactor correlated subqueries into explicit JOINs or common table expressions."
            }
        else:
            return {
                "verdict": "REJECTED",
                "executive_summary": "Query failed output verification. Candidate SQL emits mismatched row counts or inaccurate projections.",
                "strengths": ["Syntactically parsed and executed without fatal database engine errors"],
                "risks_and_anti_patterns": ["Semantic discrepancy in aggregation predicates or join criteria"],
                "optimization_recommendation": "Align join conditions and filter clauses directly with reference specification."
            }

# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================
init_benchmark_database()

st.title("⚡ Day 56 — Local AI SQL Query Evaluation & Benchmarking Platform 🗄️🤖")
st.caption("Ground Truth Result Verification • Multi-Run Latency Profiling • EXPLAIN Query Plan Scoring • Local Qwen3 Code Review")

with st.sidebar:
    st.header("⚙️ Evaluation Mode Setup")
    mode = st.radio("Select Evaluation Mode:", ["Pre-Packaged Benchmark Suite", "Custom SQL Evaluator"])
    
    if mode == "Pre-Packaged Benchmark Suite":
        scenario_key = st.selectbox("Select Benchmark Case:", list(BENCHMARK_SCENARIOS.keys()))
        scenario = BENCHMARK_SCENARIOS[scenario_key]
        desc = scenario["description"]
        default_ref = scenario["reference_sql"]
        default_cand = scenario["candidate_sql"]
    else:
        desc = "Evaluate custom Candidate SQL against a Reference SQL statement on the benchmark database."
        default_ref = "SELECT country, COUNT(*) as cust_count FROM customers GROUP BY country ORDER BY cust_count DESC;"
        default_cand = "SELECT country, COUNT(customer_id) as cust_count FROM customers GROUP BY country ORDER BY cust_count DESC;"

    benchmark_runs = st.slider("Benchmark Iterations (Runs)", min_value=5, max_value=30, value=15, step=5)
    st.divider()
    st.text_input("Active Ollama Evaluator", value=MODEL_NAME, disabled=True)
    run_eval_btn = st.button("🚀 Run Comprehensive SQL Evaluation", type="primary", use_container_width=True)

# Main SQL Workspaces
st.subheader("📝 Query Under Evaluation")
st.markdown(f"**Scenario Objective:** {desc}")

c_ref, c_cand = st.columns(2)
with c_ref:
    st.markdown("### 🏆 Reference SQL (Ground Truth)")
    ref_sql_input = st.text_area("Reference Query:", value=default_ref, height=180)

with c_cand:
    st.markdown("### 🧪 Candidate SQL (Under Test)")
    cand_sql_input = st.text_area("Candidate Query:", value=default_cand, height=180)

if "eval_state" not in st.session_state or run_eval_btn:
    with st.spinner("Executing queries, profiling multi-run latencies, parsing query plans, and generating AI critique..."):
        # 1. Execute both queries
        conn = sqlite3.connect(DB_PATH)
        df_ref, df_cand = None, None
        ref_err, cand_err = None, None
        try:
            df_ref = pd.read_sql_query(ref_sql_input, conn)
        except Exception as e:
            ref_err = str(e)

        try:
            df_cand = pd.read_sql_query(cand_sql_input, conn)
        except Exception as e:
            cand_err = str(e)
        conn.close()

        # 2. Result Equivalence
        equiv_res = evaluate_result_set_equivalence(df_ref, df_cand)

        # 3. Latency Benchmarking
        ref_perf = profile_query_performance(ref_sql_input, iterations=benchmark_runs)
        cand_perf = profile_query_performance(cand_sql_input, iterations=benchmark_runs)

        perf_comp = {
            "ref_p50": ref_perf["p50_ms"],
            "cand_p50": cand_perf["p50_ms"],
            "speedup": round(ref_perf["p50_ms"] / max(0.001, cand_perf["p50_ms"]), 2),
            "ref_latencies": ref_perf["latencies"],
            "cand_latencies": cand_perf["latencies"]
        }

        # 4. Plan Analysis
        cand_plan = analyze_query_plan(cand_sql_input)

        # 5. Composite Health Score
        health = compute_overall_sql_health_score(
            equiv_res["score"],
            cand_perf["p50_ms"],
            ref_perf["p50_ms"],
            cand_plan["score"]
        )

        # 6. Local AI Critique
        ai_critique = generate_ai_sql_evaluation(
            desc, ref_sql_input, cand_sql_input,
            equiv_res, perf_comp, cand_plan
        )

        st.session_state.eval_state = {
            "df_ref": df_ref,
            "df_cand": df_cand,
            "equiv": equiv_res,
            "ref_perf": ref_perf,
            "cand_perf": cand_perf,
            "perf_comp": perf_comp,
            "cand_plan": cand_plan,
            "health": health,
            "critique": ai_critique
        }

ev = st.session_state.eval_state
h = ev["health"]
critique = ev["critique"]

st.divider()

# Top Scorecard KPIs
k1, k2, k3, k4, k5 = st.columns(5)
grade_color = "🟢" if h["grade"] in ["A+", "A"] else ("🟡" if h["grade"] == "B" else "🔴")
k1.metric("Overall SQL Grade", f"{grade_color} {h['grade']} ({h['health_score']}%)")
k2.metric("Result Equivalence", "PASSED ✅" if ev["equiv"]["equivalent"] else "MISMATCH ❌")
k3.metric("Candidate P50 Latency", f"{ev['cand_perf']['p50_ms']:.2f} ms")
k4.metric("Reference P50 Latency", f"{ev['ref_perf']['p50_ms']:.2f} ms")
k5.metric("Plan Efficiency Score", f"{ev['cand_plan']['score']:.0f}/100")

# Primary Tabs
t_review, t_perf, t_data, t_plan, t_export = st.tabs([
    "🤖 AI Architectural Code Review",
    "📊 Latency Benchmarking & Histograms",
    "📋 Result Set Verification Matrix",
    "🔍 EXPLAIN Query Plan Inspector",
    "💾 Export Evaluation Package"
])

with t_review:
    st.subheader("Senior Database Architect Audit & Critique")
    v_badge = "🟢 APPROVED" if critique.get("verdict") == "APPROVED" else ("🟡 REVISION REQUIRED" if critique.get("verdict") == "NEEDS_REVISION" else "🔴 REJECTED")
    st.markdown(f"**Audit Verdict:** `{v_badge}`")
    st.markdown(f"**Executive Summary:** {critique.get('executive_summary', 'Evaluation completed.')}")
    
    col_str, col_risk = st.columns(2)
    with col_str:
        st.markdown("#### ✅ Architectural Strengths")
        for s in critique.get("strengths", []):
            st.markdown(f"- {s}")
    with col_risk:
        st.markdown("#### ⚠️ Risks & Anti-Patterns")
        for r in critique.get("risks_and_anti_patterns", []):
            st.markdown(f"- {r}")

    st.info(f"💡 **Optimization Recommendation:** {critique.get('optimization_recommendation', 'No modifications necessary.')}")

with t_perf:
    st.subheader(f"Multi-Run Latency Profiling ({benchmark_runs} Iterations)")
    
    # Latency Bar Comparison
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=['Reference SQL', 'Candidate SQL'],
        y=[ev['ref_perf']['p50_ms'], ev['cand_perf']['p50_ms']],
        text=[f"{ev['ref_perf']['p50_ms']:.2f} ms", f"{ev['cand_perf']['p50_ms']:.2f} ms"],
        textposition='auto',
        marker_color=['#2ca02c', '#1f77b4' if ev['cand_perf']['p50_ms'] <= ev['ref_perf']['p50_ms'] else '#d62728']
    ))
    fig_bar.update_layout(title="Median Execution Latency (P50 in ms)", template="plotly_dark", height=350)
    st.plotly_chart(fig_bar, use_container_width=True, key="chart_perf_bar")

    # Latency Distribution Box Plot
    df_lat = pd.DataFrame({
        "Reference SQL": ev['perf_comp']['ref_latencies'],
        "Candidate SQL": ev['perf_comp']['cand_latencies']
    })
    fig_box = px.box(df_lat, title="Iteration Latency Distribution (ms)", template="plotly_dark")
    fig_box.update_layout(height=350)
    st.plotly_chart(fig_box, use_container_width=True, key="chart_perf_box")

with t_data:
    st.subheader("Data Equivalence & Result Set Diff")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("**Reference Output (First 5 Rows):**")
        if ev["df_ref"] is not None:
            st.dataframe(ev["df_ref"].head(5), use_container_width=True)
        else:
            st.error("Reference query failed execution.")
    with col_d2:
        st.markdown("**Candidate Output (First 5 Rows):**")
        if ev["df_cand"] is not None:
            st.dataframe(ev["df_cand"].head(5), use_container_width=True)
        else:
            st.error("Candidate query failed execution.")

    if ev["equiv"]["equivalent"]:
        st.success(f"✅ Exact match verified! Output dimensions ({ev['equiv']['cand_rows']} rows × {ev['equiv']['cand_cols']} columns) and all cell values match ground truth.")
    else:
        st.error(f"❌ Output mismatch: Candidate returned {ev['equiv']['cand_rows']} rows vs. Reference {ev['equiv']['ref_rows']} rows.")

with t_plan:
    st.subheader("SQLite Query Planner Breakdown")
    col_p1, col_p2, col_p3 = st.columns(3)
    col_p1.metric("Full Table Scans", ev["cand_plan"]["full_scans"])
    col_p2.metric("Index Lookups", ev["cand_plan"]["indexes_used"])
    col_p3.metric("Temp B-Trees", ev["cand_plan"]["temp_trees"])
    st.code(ev["cand_plan"]["plan_text"] if ev["cand_plan"]["plan_text"] else "No plan available", language="text")

with t_export:
    st.subheader("Export Evaluation Audit Package")
    export_data = {
        "scenario": desc,
        "overall_health_score": h["health_score"],
        "grade": h["grade"],
        "result_equivalence": ev["equiv"],
        "performance_profile": {
            "ref_p50_ms": ev["ref_perf"]["p50_ms"],
            "cand_p50_ms": ev["cand_perf"]["p50_ms"],
            "ref_mean_ms": ev["ref_perf"]["mean_ms"],
            "cand_mean_ms": ev["cand_perf"]["mean_ms"]
        },
        "query_plan_summary": ev["cand_plan"],
        "ai_critique": critique,
        "reference_sql": ref_sql_input,
        "candidate_sql": cand_sql_input
    }
    
    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        st.download_button(
            "📥 Download Audit Report (JSON)",
            data=json.dumps(export_data, indent=2),
            file_name="sql_benchmark_evaluation.json",
            mime="application/json",
            use_container_width=True
        )
    with col_ex2:
        df_export = pd.DataFrame([{
            "Health Score": h["health_score"],
            "Grade": h["grade"],
            "Equivalent": ev["equiv"]["equivalent"],
            "Cand Latency P50 (ms)": ev["cand_perf"]["p50_ms"],
            "Ref Latency P50 (ms)": ev["ref_perf"]["p50_ms"],
            "Table Scans": ev["cand_plan"]["full_scans"]
        }])
        st.download_button(
            "📥 Download Summary Metrics (CSV)",
            data=df_export.to_csv(index=False),
            file_name="sql_benchmark_summary.csv",
            mime="text/csv",
            use_container_width=True
        )
