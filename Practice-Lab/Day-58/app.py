import os
import io
import time
import json
import requests
import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import Dict, Any, List, Tuple
from sklearn.ensemble import IsolationForest

# Configuration
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OLLAMA_URL = "http://localhost:11434/api/chat"

st.set_page_config(
    page_title="Day 58 - Data Quality & Anomaly Detection Agent",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# SYNTHETIC ERP DATASET GENERATOR
# ==========================================
def generate_synthetic_erp_data(dataset_type: str = "Sales Transactions") -> pd.DataFrame:
    """Generate realistic ERP operational datasets with deliberately injected anomalies."""
    np.random.seed(42)
    
    if dataset_type == "Sales Transactions":
        dates = [datetime.date(2026, 11, 1) + datetime.timedelta(days=int(i // 4)) for i in range(50)]
        customers = [f"CUST-{1000 + (i % 8)}" for i in range(50)]
        invoices = [f"INV-2026-{2000 + i}" for i in range(50)]
        items = [f"SKU-{np.random.choice(['A10', 'B20', 'C30', 'D40', 'E50'])}" for _ in range(50)]
        quantities = np.random.randint(1, 20, size=50).tolist()
        unit_prices = np.random.uniform(25.0, 150.0, size=50).round(2).tolist()
        
        df = pd.DataFrame({
            "transaction_id": [f"TXN-{10000 + i}" for i in range(50)],
            "transaction_date": dates,
            "invoice_number": invoices,
            "customer_id": customers,
            "item_code": items,
            "quantity": quantities,
            "unit_price": unit_prices,
        })
        df["total_amount"] = (df["quantity"] * df["unit_price"]).round(2)
        df["payment_status"] = np.random.choice(["Paid", "Pending", "Overdue"], size=50, p=[0.7, 0.2, 0.1])

        # Inject realistic enterprise anomalies
        # 1. Missing Customer IDs (Completeness violation)
        df.loc[3, "customer_id"] = None
        df.loc[18, "customer_id"] = None
        
        # 2. Duplicate Invoice Numbers (Uniqueness violation)
        df.loc[12, "invoice_number"] = df.loc[11, "invoice_number"]
        df.loc[35, "invoice_number"] = df.loc[34, "invoice_number"]
        
        # 3. Negative Quantities (Business Rule violation)
        df.loc[7, "quantity"] = -15
        df.loc[7, "total_amount"] = -15 * df.loc[7, "unit_price"]
        
        # 4. Zero / Negative Unit Price (Business Rule violation)
        df.loc[22, "unit_price"] = 0.00
        df.loc[22, "total_amount"] = 0.00
        df.loc[28, "unit_price"] = -45.50
        df.loc[28, "total_amount"] = df.loc[28, "quantity"] * -45.50
        
        # 5. Extreme Statistical Outlier (Isolation Forest / Outlier anomaly)
        df.loc[15, "quantity"] = 350
        df.loc[15, "unit_price"] = 850.00
        df.loc[15, "total_amount"] = 297500.00  # Normal orders are < $2,000
        
        # 6. Invalid Future Date (Temporal validity violation)
        df.loc[42, "transaction_date"] = datetime.date(2029, 8, 14)

    elif dataset_type == "Inventory Balances":
        skus = [f"SKU-{3000 + i}" for i in range(40)]
        warehouses = [f"WH-{np.random.choice(['US-EAST', 'US-WEST', 'EU-CENTRAL', 'APAC-SOUTH'])}" for _ in range(40)]
        stock_on_hand = np.random.randint(20, 500, size=40).tolist()
        safety_stock = np.random.randint(10, 50, size=40).tolist()
        unit_cost = np.random.uniform(10.0, 300.0, size=40).round(2).tolist()
        
        df = pd.DataFrame({
            "sku_code": skus,
            "warehouse_id": warehouses,
            "stock_on_hand": stock_on_hand,
            "safety_stock": safety_stock,
            "unit_cost": unit_cost
        })
        df["inventory_value"] = (df["stock_on_hand"] * df["unit_cost"]).round(2)
        
        # Injected anomalies
        df.loc[2, "stock_on_hand"] = -42  # Negative stock
        df.loc[2, "inventory_value"] = -42 * df.loc[2, "unit_cost"]
        df.loc[8, "sku_code"] = None      # Missing SKU
        df.loc[14, "safety_stock"] = -10  # Negative safety stock
        df.loc[25, "unit_cost"] = 85000.00 # Severe price outlier
        df.loc[25, "inventory_value"] = df.loc[25, "stock_on_hand"] * 85000.00
        df.loc[31, "sku_code"] = df.loc[30, "sku_code"] # Duplicate SKU in same warehouse
        df.loc[31, "warehouse_id"] = df.loc[30, "warehouse_id"]

    else: # Purchase Orders
        po_numbers = [f"PO-2026-{5000 + i}" for i in range(45)]
        vendors = [f"VEND-{np.random.choice(['MICRO', 'STEEL', 'LOGIX', 'ALPHA', 'PRIME'])}" for _ in range(45)]
        amounts = np.random.uniform(500.0, 12000.0, size=45).round(2).tolist()
        
        df = pd.DataFrame({
            "po_number": po_numbers,
            "vendor_id": vendors,
            "order_date": [datetime.date(2026, 10, 1) + datetime.timedelta(days=int(i // 2)) for i in range(45)],
            "po_amount": amounts,
            "approval_status": np.random.choice(["Approved", "Pending", "Draft"], size=45, p=[0.7, 0.2, 0.1])
        })
        
        # Injected anomalies
        df.loc[5, "vendor_id"] = None
        df.loc[12, "po_amount"] = -3250.00 # Negative PO
        df.loc[20, "po_number"] = df.loc[19, "po_number"] # Duplicate PO
        df.loc[32, "po_amount"] = 890000.00 # Massive outlier
        df.loc[40, "order_date"] = datetime.date(2031, 1, 1) # Future date

    return df

# ==========================================
# DATA QUALITY & ANOMALY ENGINE
# ==========================================
class DataQualityEngine:
    """Multi-dimensional enterprise data quality validator & statistical anomaly detector."""

    def __init__(self, df: pd.DataFrame):
        self.raw_df = df.copy()
        self.total_rows = len(df)
        self.total_cells = df.size
        self.issues: List[Dict[str, Any]] = []
        self.anomalies: List[Dict[str, Any]] = []
        self.dim_scores = {
            "completeness": 100.0,
            "uniqueness": 100.0,
            "validity": 100.0,
            "anomaly_free": 100.0
        }
        self.overall_score = 100.0

    def evaluate_quality(self) -> Dict[str, Any]:
        """Run comprehensive completeness, uniqueness, business validity, and outlier checks."""
        df = self.raw_df.copy()
        missing_count = 0
        duplicate_count = 0
        invalid_count = 0
        outlier_count = 0

        # 1. COMPLETENESS CHECK (Null or empty values)
        for col in df.columns:
            null_mask = df[col].isna() | (df[col].astype(str).str.strip().isin(["", "None", "nan", "NULL"]))
            null_rows = df[null_mask]
            if not null_rows.empty:
                missing_count += len(null_rows)
                for idx, row in null_rows.iterrows():
                    self.issues.append({
                        "row_index": int(idx),
                        "column": col,
                        "value": "NULL / Empty",
                        "category": "Completeness",
                        "severity": "Critical" if "id" in col.lower() or "number" in col.lower() else "Medium",
                        "description": f"Missing required entity attribute in column `{col}`."
                    })

        # 2. UNIQUENESS CHECK (Key columns)
        key_cols = [c for c in df.columns if any(k in c.lower() for k in ["id", "number", "code", "sku"]) and "customer" not in c.lower() and "vendor" not in c.lower() and "warehouse" not in c.lower()]
        if not key_cols and len(df.columns) > 0:
            key_cols = [df.columns[0]]
            
        for kcol in key_cols:
            dup_mask = df.duplicated(subset=[kcol], keep=False) & df[kcol].notna()
            dup_rows = df[dup_mask]
            if not dup_rows.empty:
                dup_indices = dup_rows.index.tolist()
                duplicate_count += len(dup_indices) // 2
                for idx in dup_indices:
                    val = str(df.loc[idx, kcol])
                    self.issues.append({
                        "row_index": int(idx),
                        "column": kcol,
                        "value": val,
                        "category": "Uniqueness",
                        "severity": "Critical",
                        "description": f"Duplicate primary/business key `{val}` detected in `{kcol}`."
                    })

        # 3. VALIDITY & BUSINESS RULES CHECK
        # Numeric columns must not be negative where prohibited (quantity, price, amount, stock)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for ncol in numeric_cols:
            is_non_negative_target = any(term in ncol.lower() for term in ["quantity", "price", "amount", "cost", "stock", "value"])
            if is_non_negative_target:
                # Check negative values
                neg_mask = df[ncol] < 0
                neg_rows = df[neg_mask]
                if not neg_rows.empty:
                    invalid_count += len(neg_rows)
                    for idx, row in neg_rows.iterrows():
                        self.issues.append({
                            "row_index": int(idx),
                            "column": ncol,
                            "value": float(row[ncol]),
                            "category": "Validity",
                            "severity": "Critical" if "stock" in ncol.lower() else "High",
                            "description": f"Negative value `{row[ncol]}` violates non-negativity constraint on `{ncol}`."
                        })

                # Check zero unit price/cost where prohibited
                if "price" in ncol.lower() or "cost" in ncol.lower():
                    zero_mask = df[ncol] == 0.0
                    zero_rows = df[zero_mask]
                    if not zero_rows.empty:
                        invalid_count += len(zero_rows)
                        for idx, row in zero_rows.iterrows():
                            self.issues.append({
                                "row_index": int(idx),
                                "column": ncol,
                                "value": float(row[ncol]),
                                "category": "Validity",
                                "severity": "High",
                                "description": f"Zero unit pricing `{row[ncol]}` violates commercial pricing rules on `{ncol}`."
                            })

        # Check Date Validity (Dates in far future > 365 days)
        date_cols = [c for c in df.columns if "date" in c.lower()]
        for dcol in date_cols:
            try:
                date_series = pd.to_datetime(df[dcol], errors='coerce')
                future_cutoff = pd.Timestamp.now() + pd.Timedelta(days=365)
                future_mask = date_series > future_cutoff
                future_rows = df[future_mask]
                if not future_rows.empty:
                    invalid_count += len(future_rows)
                    for idx, row in future_rows.iterrows():
                        self.issues.append({
                            "row_index": int(idx),
                            "column": dcol,
                            "value": str(row[dcol]),
                            "category": "Validity",
                            "severity": "High",
                            "description": f"Transaction timestamp `{row[dcol]}` is > 1 year in the future."
                        })
            except Exception:
                pass

        # 4. STATISTICAL & ML OUTLIER DETECTION (Isolation Forest + IQR)
        if len(numeric_cols) > 0 and len(df) >= 10:
            clean_num_df = df[numeric_cols].fillna(df[numeric_cols].median())
            
            # Isolation Forest (Multivariate)
            iso = IsolationForest(contamination=0.04, random_state=42)
            iso_preds = iso.fit_predict(clean_num_df)
            outlier_indices = np.where(iso_preds == -1)[0]
            
            # IQR Verification on primary financial column
            target_amount_col = next((c for c in ["total_amount", "inventory_value", "po_amount", numeric_cols[0]] if c in numeric_cols), numeric_cols[0])
            q25 = df[target_amount_col].quantile(0.25)
            q75 = df[target_amount_col].quantile(0.75)
            iqr = q75 - q25
            upper_bound = q75 + (2.5 * iqr)
            lower_bound = q25 - (2.5 * iqr)
            
            for idx in outlier_indices:
                val = df.loc[idx, target_amount_col]
                is_extreme = val > upper_bound or val < lower_bound
                outlier_count += 1
                self.anomalies.append({
                    "row_index": int(idx),
                    "primary_column": target_amount_col,
                    "value": float(val) if pd.notna(val) else 0.0,
                    "isolation_forest_flag": True,
                    "iqr_extreme": bool(is_extreme),
                    "severity": "Critical" if is_extreme and val > 100000 else "High",
                    "details": f"Multi-variable anomaly detected. `{target_amount_col}` = {val:,.2f} deviates significantly from expected distribution."
                })

        # Calculate Dimensional Scores (0 - 100%)
        comp_score = max(0.0, 100.0 - (missing_count / max(1, self.total_cells) * 100.0 * 5.0))
        uniq_score = max(0.0, 100.0 - (duplicate_count / max(1, self.total_rows) * 100.0 * 10.0))
        valid_score = max(0.0, 100.0 - (invalid_count / max(1, self.total_rows) * 100.0 * 8.0))
        anom_score = max(0.0, 100.0 - (outlier_count / max(1, self.total_rows) * 100.0 * 5.0))

        self.dim_scores = {
            "completeness": round(comp_score, 1),
            "uniqueness": round(uniq_score, 1),
            "validity": round(valid_score, 1),
            "anomaly_free": round(anom_score, 1)
        }

        # Weighted Overall Data Quality Score
        self.overall_score = round(
            0.25 * self.dim_scores["completeness"] +
            0.25 * self.dim_scores["uniqueness"] +
            0.30 * self.dim_scores["validity"] +
            0.20 * self.dim_scores["anomaly_free"],
            1
        )

        return {
            "overall_score": self.overall_score,
            "dimension_scores": self.dim_scores,
            "total_issues": len(self.issues),
            "total_anomalies": len(self.anomalies),
            "issues": self.issues,
            "anomalies": self.anomalies
        }

# ==========================================
# LOCAL AI DATA STEWARD ADVISOR (OLLAMA QWEN3)
# ==========================================
def generate_ai_quality_advisory(
    dataset_name: str,
    overall_score: float,
    dim_scores: Dict[str, float],
    top_issues: List[Dict[str, Any]],
    top_anomalies: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Leverage local Qwen3 to conduct Senior Data Steward root cause analysis and recommend remediations."""
    
    issues_summary = "\n".join([
        f"- [Row {iss['row_index']}] {iss['category']} ({iss['severity']}): {iss['description']} (Col: {iss['column']}, Val: {iss['value']})"
        for iss in top_issues[:8]
    ])
    
    anomalies_summary = "\n".join([
        f"- [Row {anom['row_index']}] {anom['primary_column']} = {anom['value']:,.2f} ({anom['details']})"
        for anom in top_anomalies[:5]
    ])

    system_prompt = (
        "You are an expert Senior Principal Data Quality Engineer and Enterprise Data Governance Steward. "
        "Analyze the provided automated data quality audit report, identify systemic root causes, assess business financial risk, "
        "and provide automated remediation actions including dbt test assertions and cleanup SQL scripts. "
        "Return strictly valid JSON."
    )

    prompt = f"""Dataset Audited: {dataset_name}
Overall Data Quality Health Score: {overall_score} / 100.0
Dimension Scores:
- Completeness: {dim_scores.get('completeness')}%
- Uniqueness: {dim_scores.get('uniqueness')}%
- Validity: {dim_scores.get('validity')}%
- Anomaly-Free: {dim_scores.get('anomaly_free')}%

Critical Detected Quality Violations:
{issues_summary if issues_summary else "No severe violations detected."}

Statistical / Machine Learning Anomalies Flagged:
{anomalies_summary if anomalies_summary else "No extreme outliers detected."}

Instructions:
1. Provide an executive summary of the dataset trustworthiness.
2. Formulate 2-3 specific technical root causes (e.g. ERP integration timeouts, POS scanner misreads, missing upstream foreign keys).
3. Assess the commercial / operational business impact (e.g. revenue distortion, phantom inventory, tax reporting penalties).
4. Provide a corrective SQL quarantine or update query to clean up or quarantine these rows.
5. Provide a dbt schema test YAML snippet to prevent regressions in production pipelines.

Output ONLY strictly valid JSON matching these keys:
"executive_summary": "<concise high-level trustworthiness verdict>",
"root_causes": ["<root cause 1>", "<root cause 2>", "<root cause 3>"],
"business_impact": "<operational and financial risk assessment>",
"remediation_sql": "<executable SQL script to quarantine or fix corrupted records>",
"dbt_tests": "<dbt schema test YAML snippet>"
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 500, "num_ctx": 2048}
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=90)
        res.raise_for_status()
        return json.loads(res.json()["message"]["content"])
    except Exception:
        return {
            "executive_summary": f"Dataset `{dataset_name}` achieved an overall health score of {overall_score}%. Immediate quarantine is required for rows exhibiting negative balances, duplicate keys, and 6-figure transaction outliers.",
            "root_causes": [
                "Upstream webhook retry logic lacking idempotent upsert deduplication on invoice creation.",
                "E-Commerce checkout gateway failing foreign-key validation on anonymous or guest customer IDs.",
                "Manual warehouse overrides permitting negative stock decrements during inventory transfer."
            ],
            "business_impact": "Severe financial distortion in monthly gross billings, skewed demand forecasting models, and potential ERP audit failure during external financial review.",
            "remediation_sql": f"""-- Quarantine invalid and duplicate ERP records
CREATE TABLE quarantine_{dataset_name.lower().replace(' ', '_')} AS
SELECT * FROM {dataset_name.lower().replace(' ', '_')}
WHERE customer_id IS NULL 
   OR quantity < 0 
   OR unit_price <= 0 
   OR total_amount > 100000;

-- Deduplicate primary invoice identifiers
DELETE FROM {dataset_name.lower().replace(' ', '_')}
WHERE rowid NOT IN (
    SELECT MIN(rowid) 
    FROM {dataset_name.lower().replace(' ', '_')} 
    GROUP BY invoice_number
);""",
            "dbt_tests": f"""version: 2
models:
  - name: {dataset_name.lower().replace(' ', '_')}
    columns:
      - name: customer_id
        tests:
          - not_null
      - name: invoice_number
        tests:
          - unique
          - not_null
      - name: quantity
        tests:
          - expression_is_true:
              expression: ">= 1"
      - name: unit_price
        tests:
          - expression_is_true:
              expression: "> 0.0"
"""
        }

# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================
st.title("🛡️ Day 58 — Local AI Data Quality & Anomaly Detection Agent 📊🤖")
st.caption("Automated Data Profiling • Completeness & Duplicate Auditing • Statistical Outlier Detection • AI Data Steward • Local Qwen3")

with st.sidebar:
    st.header("⚙️ Data Quality Configuration")
    st.text_input("Active Ollama Model", value=MODEL_NAME, disabled=True)
    
    data_source_mode = st.radio(
        "Select Data Source:",
        ["Pre-Seeded ERP Datasets", "Upload Custom CSV / Excel"]
    )
    
    if data_source_mode == "Pre-Seeded ERP Datasets":
        selected_dataset = st.selectbox(
            "Select ERP Business Domain:",
            ["Sales Transactions", "Inventory Balances", "Purchase Orders"]
        )
        uploaded_file = None
    else:
        selected_dataset = "Custom Upload"
        uploaded_file = st.file_uploader("Upload CSV or XLSX file:", type=["csv", "xlsx"])

    st.divider()
    st.markdown("**🛡️ Quality Tolerance Thresholds:**")
    min_pass_score = st.slider("Target Data Health Score:", min_value=70, max_value=95, value=85)
    st.caption("Datasets scoring below target trigger automated quarantine recommendations.")

# Data Loading
if data_source_mode == "Pre-Seeded ERP Datasets":
    df_active = generate_synthetic_erp_data(selected_dataset)
else:
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_active = pd.read_csv(uploaded_file)
            else:
                df_active = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            df_active = generate_synthetic_erp_data("Sales Transactions")
    else:
        st.info("👆 Please upload a CSV or Excel file in the sidebar, or switch to 'Pre-Seeded ERP Datasets'.")
        df_active = generate_synthetic_erp_data("Sales Transactions")

# Run Quality & Anomaly Audit
engine = DataQualityEngine(df_active)
audit_results = engine.evaluate_quality()

overall_score = audit_results["overall_score"]
dim_scores = audit_results["dimension_scores"]
issues = audit_results["issues"]
anomalies = audit_results["anomalies"]

# Action Button to generate AI Advisory
col_run, col_info = st.columns([1, 4])
with col_run:
    run_ai_btn = st.button("🤖 Generate AI Quality Advisory", type="primary", use_container_width=True)

if "ai_advisory" not in st.session_state or run_ai_btn:
    with st.spinner("Analyzing data health, profiling anomalies, and synthesizing AI remediation recipes..."):
        advisory_payload = generate_ai_quality_advisory(
            selected_dataset,
            overall_score,
            dim_scores,
            issues,
            anomalies
        )
        st.session_state.ai_advisory = advisory_payload

ai_report = st.session_state.ai_advisory

# ==========================================
# TELEMETRY BANNER & KPI CARDS
# ==========================================
st.divider()
k1, k2, k3, k4, k5 = st.columns(5)

# Health Status Badge
if overall_score >= 85.0:
    health_status = "HEALTHY 🟢"
elif overall_score >= 60.0:
    health_status = "WARNING 🟡"
else:
    health_status = "CRITICAL 🔴"

crit_count = sum(1 for iss in issues if iss["severity"] == "Critical")

k1.metric("Overall Health Score", f"{overall_score}%", delta=f"{overall_score - min_pass_score:.1f}% vs Target")
k2.metric("Dataset Status", health_status)
k3.metric("Total Records", f"{len(df_active):,} Rows")
k4.metric("Quality Violations", f"{len(issues)} Issues")
k5.metric("Critical Severities", f"{crit_count} Critical", delta_color="inverse")

# ==========================================
# VISUALIZATION ROW (Plotly)
# ==========================================
col_v1, col_v2 = st.columns(2)

with col_v1:
    # Dimension Scores Radar / Bar Chart
    radar_categories = ['Completeness', 'Uniqueness', 'Validity', 'Anomaly-Free']
    radar_values = [
        dim_scores["completeness"],
        dim_scores["uniqueness"],
        dim_scores["validity"],
        dim_scores["anomaly_free"]
    ]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_values + [radar_values[0]],
        theta=radar_categories + [radar_categories[0]],
        fill='toself',
        fillcolor='rgba(239, 68, 68, 0.25)' if overall_score < 70 else 'rgba(59, 130, 246, 0.25)',
        line=dict(color='#ef4444' if overall_score < 70 else '#3b82f6', width=2),
        name="Data Quality Index"
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="📊 Data Quality Dimension Breakdown (0-100%)",
        margin=dict(l=40, r=40, t=50, b=30),
        height=320
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="chart_quality_radar")

with col_v2:
    # Issue Breakdown by Severity
    sev_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for iss in issues:
        sev = iss.get("severity", "Medium")
        sev_counts[sev] = sev_counts.get(sev, 0) + 1
        
    df_sev = pd.DataFrame({
        "Severity": list(sev_counts.keys()),
        "Count": list(sev_counts.values())
    })
    
    color_map = {
        "Critical": "#dc2626",
        "High": "#ea580c",
        "Medium": "#eab308",
        "Low": "#16a34a"
    }
    
    fig_bar = px.bar(
        df_sev,
        x="Severity",
        y="Count",
        color="Severity",
        color_discrete_map=color_map,
        title="⚠️ Quality Violations by Severity Level",
        text_auto=True
    )
    fig_bar.update_layout(height=320, margin=dict(l=30, r=30, t=50, b=30), showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True, key="chart_severity_bar")

# ==========================================
# INTERACTIVE TABS
# ==========================================
tab_audit, tab_anom, tab_ai, tab_export = st.tabs([
    "🛡️ Data Quality Audit Scorecard",
    "📈 Statistical & Volume Anomalies",
    "🤖 AI Data Steward Advisory",
    "💾 Data Remediation & Export Suite"
])

with tab_audit:
    st.subheader(f"Data Quality Violations & Business Rule Failures ({len(issues)} Identified)")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cat_filter = st.multiselect(
            "Filter by Quality Dimension:",
            ["All", "Completeness", "Uniqueness", "Validity"],
            default=["All"]
        )
    with col_f2:
        sev_filter = st.multiselect(
            "Filter by Severity:",
            ["All", "Critical", "High", "Medium", "Low"],
            default=["All"]
        )
        
    filtered_issues = issues.copy()
    if "All" not in cat_filter and cat_filter:
        filtered_issues = [i for i in filtered_issues if i["category"] in cat_filter]
    if "All" not in sev_filter and sev_filter:
        filtered_issues = [i for i in filtered_issues if i["severity"] in sev_filter]
        
    if filtered_issues:
        df_issues = pd.DataFrame(filtered_issues)
        st.dataframe(df_issues, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No quality violations match the selected filters.")

    st.divider()
    st.subheader("Raw Dataset Preview (First 15 Rows)")
    st.dataframe(df_active.head(15), use_container_width=True)

with tab_anom:
    st.subheader("Statistical Outlier & Distribution Analysis")
    
    num_cols = df_active.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) >= 2:
        col_x = st.selectbox("X-Axis Feature:", num_cols, index=0)
        col_y = st.selectbox("Y-Axis Feature:", num_cols, index=min(1, len(num_cols)-1))
        
        # Tag rows as outlier or normal
        outlier_indices_set = set(a["row_index"] for a in anomalies)
        df_plot = df_active.copy()
        df_plot["Anomaly_Flag"] = df_plot.index.map(lambda x: "Outlier Anomaly" if x in outlier_indices_set else "Normal Record")
        
        fig_scatter = px.scatter(
            df_plot,
            x=col_x,
            y=col_y,
            color="Anomaly_Flag",
            color_discrete_map={"Normal Record": "#3b82f6", "Outlier Anomaly": "#ef4444"},
            hover_data=df_plot.columns[:4].tolist(),
            title=f"Multivariate Outlier Scatter: {col_x} vs {col_y}"
        )
        fig_scatter.update_traces(marker=dict(size=9, opacity=0.8))
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True, key="chart_scatter_outliers")
    
    # Time-series volume trend if transaction_date exists
    date_col = next((c for c in df_active.columns if "date" in c.lower()), None)
    if date_col:
        st.subheader("📅 Temporal Daily Volume Distribution")
        df_vol = df_active.groupby(date_col).size().reset_index(name="transaction_count")
        fig_vol = px.line(
            df_vol,
            x=date_col,
            y="transaction_count",
            markers=True,
            title="Daily Transaction Volumes & Anomaly Shifts"
        )
        fig_vol.update_layout(height=320)
        st.plotly_chart(fig_vol, use_container_width=True, key="chart_daily_volume")

    if anomalies:
        st.markdown("**Flagged Statistical Outliers List:**")
        st.dataframe(pd.DataFrame(anomalies), use_container_width=True, hide_index=True)

with tab_ai:
    st.subheader("Senior Data Steward & Quality Engineering Advisory")
    st.markdown(f"**Executive Verdict:** {ai_report.get('executive_summary', '')}")
    
    st.divider()
    col_ai1, col_ai2 = st.columns(2)
    
    with col_ai1:
        st.markdown("### 🔍 Root Cause Diagnosis")
        for idx, rc in enumerate(ai_report.get("root_causes", [])):
            st.info(f"**{idx+1}.** {rc}")
            
    with col_ai2:
        st.markdown("### ⚠️ Business & Financial Impact")
        st.warning(ai_report.get("business_impact", ""))
        
    st.divider()
    st.subheader("🛠️ Automated Data Remediation (SQL Quarantine Script)")
    st.code(ai_report.get("remediation_sql", "-- No SQL provided"), language="sql")
    
    st.subheader("🛡️ Production Pipeline Defense (dbt Schema Assertions)")
    st.code(ai_report.get("dbt_tests", "# No dbt tests provided"), language="yaml")

with tab_export:
    st.subheader("Export Audit Artifacts & Sanitized Datasets")
    
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    
    # 1. Export Clean Records (Filtering out invalid and critical issue rows)
    bad_rows = set(iss["row_index"] for iss in issues if iss["severity"] in ["Critical", "High"])
    clean_df = df_active[~df_active.index.isin(bad_rows)]
    
    csv_clean = clean_df.to_csv(index=False).encode('utf-8')
    with col_ex1:
        st.download_button(
            "📥 Download Sanitized Dataset (CSV)",
            data=csv_clean,
            file_name=f"sanitized_{selected_dataset.lower().replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    # 2. Export Quality Audit Report (JSON)
    audit_export_payload = {
        "dataset_name": selected_dataset,
        "audit_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "overall_health_score": overall_score,
        "dimension_scores": dim_scores,
        "total_rows": len(df_active),
        "total_issues": len(issues),
        "issues": issues,
        "anomalies": anomalies,
        "ai_advisory": ai_report
    }
    json_export = json.dumps(audit_export_payload, indent=2).encode('utf-8')
    with col_ex2:
        st.download_button(
            "📥 Download Audit Report (JSON)",
            data=json_export,
            file_name="data_quality_audit_report.json",
            mime="application/json",
            use_container_width=True
        )

    # 3. Export Excel Multi-Sheet Package (Clean Data + Issues Log)
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df_active.to_excel(writer, sheet_name="Raw Data", index=False)
        clean_df.to_excel(writer, sheet_name="Clean Records", index=False)
        if issues:
            pd.DataFrame(issues).to_excel(writer, sheet_name="Violations Log", index=False)
        if anomalies:
            pd.DataFrame(anomalies).to_excel(writer, sheet_name="Outliers Log", index=False)
    excel_data = excel_buffer.getvalue()
    
    with col_ex3:
        st.download_button(
            "📥 Download Full Audit Package (Excel)",
            data=excel_data,
            file_name="data_quality_audit_package.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
