import os
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration & Layout
st.set_page_config(
    page_title="IT Hardware Reliability Analytics BI Dashboard",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid #334155;
        text-align: center;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# 2. Database Connection & Data Load
@st.cache_data
def load_data():
    db_path = os.path.join('data', 'backblaze_2024.db')
    
    # If DB doesn't exist, execute pipeline script to create it
    if not os.path.exists(db_path):
        os.system("python scripts/execute_backblaze_pipeline.py")
        
    conn = sqlite3.connect(db_path)
    
    # Query 1: Fleet Exposure
    q1 = """
    WITH FleetSummary AS (
        SELECT 
            COUNT(DISTINCT serial_number) AS total_unique_drives,
            COUNT(*) AS total_drive_days_exposure,
            SUM(failure) AS total_failures,
            ROUND(AVG(capacity_bytes / 1073741824.0 / 1024.0), 2) AS avg_capacity_tb
        FROM backblaze_drive_stats
    )
    SELECT 
        total_unique_drives,
        total_drive_days_exposure,
        total_failures,
        avg_capacity_tb,
        ROUND(((CAST(total_failures AS FLOAT) / total_drive_days_exposure) * 365) * 100, 2) AS annualized_failure_rate_pct
    FROM FleetSummary;
    """
    df_fleet = pd.read_sql_query(q1, conn)
    
    # Query 2: Model Benchmarking
    q2 = """
    SELECT 
        model,
        ROUND(MAX(capacity_bytes) / 1073741824.0 / 1024.0, 0) AS capacity_tb,
        COUNT(DISTINCT serial_number) AS active_drives,
        COUNT(*) AS drive_days_exposure,
        SUM(failure) AS failure_count,
        ROUND(((CAST(SUM(failure) AS FLOAT) / COUNT(*)) * 365) * 100, 2) AS annualized_failure_rate_pct,
        CASE 
            WHEN ((CAST(SUM(failure) AS FLOAT) / COUNT(*)) * 365) * 100 > 2.5 THEN 'CRITICAL_RISK'
            WHEN ((CAST(SUM(failure) AS FLOAT) / COUNT(*)) * 365) * 100 >= 1.5 THEN 'MODERATE_RISK'
            ELSE 'LOW_RISK'
        END AS reliability_tier
    FROM backblaze_drive_stats
    GROUP BY model
    HAVING COUNT(*) >= 1000
    ORDER BY annualized_failure_rate_pct DESC;
    """
    df_models = pd.read_sql_query(q2, conn)
    
    # Query 3: SMART Signals
    q3 = """
    WITH SmartBuckets AS (
        SELECT 
            serial_number,
            model,
            failure,
            CASE 
                WHEN smart_5_raw > 0 OR smart_197_raw > 0 THEN 'Elevated SMART Anomaly (SMART 5/197 > 0)'
                ELSE 'Healthy SMART Profile (SMART 5 & 197 = 0)'
            END AS smart_health_status
        FROM backblaze_drive_stats
    )
    SELECT 
        smart_health_status,
        COUNT(DISTINCT serial_number) AS total_drives,
        COUNT(*) AS total_drive_days,
        SUM(failure) AS total_failures,
        ROUND(((CAST(SUM(failure) AS FLOAT) / COUNT(*)) * 365) * 100, 2) AS annualized_failure_rate_pct
    FROM SmartBuckets
    GROUP BY smart_health_status
    ORDER BY annualized_failure_rate_pct DESC;
    """
    df_smart = pd.read_sql_query(q3, conn)
    
    conn.close()
    return df_fleet, df_models, df_smart

df_fleet, df_models, df_smart = load_data()

# 3. Sidebar Navigation & Interactive Filters
st.sidebar.image("https://img.icons8.com/color/96/server.png", width=64)
st.sidebar.title("BI Filter Controls")

view_option = st.sidebar.radio(
    "Select Dashboard View:",
    ["📊 Backblaze Telemetry Reliability", "🔍 Data Quality Audit & Inventory"]
)

if view_option == "📊 Backblaze Telemetry Reliability":
    st.sidebar.subheader("Filter Drive Models")
    selected_models = st.sidebar.multiselect(
        "Select Drive Models:",
        options=df_models['model'].tolist(),
        default=df_models['model'].tolist()
    )
    
    selected_tiers = st.sidebar.multiselect(
        "Select Reliability Tiers:",
        options=['CRITICAL_RISK', 'MODERATE_RISK', 'LOW_RISK'],
        default=['CRITICAL_RISK', 'MODERATE_RISK', 'LOW_RISK']
    )
    
    critical_threshold = st.sidebar.slider(
        "Critical AFR Threshold (%)",
        min_value=1.0, max_value=5.0, value=2.5, step=0.1
    )
    
    # Filter dataset
    filtered_df_models = df_models[
        (df_models['model'].isin(selected_models)) & 
        (df_models['reliability_tier'].isin(selected_tiers))
    ]

# 4. Main Page Rendering
if view_option == "📊 Backblaze Telemetry Reliability":
    st.markdown("<div class='main-header'>🛠️ IT Hardware Reliability & Telemetry Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Interactive BI Dashboard evaluating 186,160 drive-days of operational exposure</div>", unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-title'>OPERATIONAL EXPOSURE</div>
            <div class='metric-value' style='color:#38bdf8;'>{df_fleet['total_drive_days_exposure'].iloc[0]:,} <span style='font-size:1rem;'>Days</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-title'>FLEET ANNUALIZED FAILURE RATE</div>
            <div class='metric-value' style='color:#f43f5e;'>{df_fleet['annualized_failure_rate_pct'].iloc[0]:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-title'>OBSERVED FAILURES</div>
            <div class='metric-value' style='color:#fbbf24;'>{df_fleet['total_failures'].iloc[0]} <span style='font-size:1rem;'>Drives</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-title'>ACTIVE MONITORED FLEET</div>
            <div class='metric-value' style='color:#34d399;'>{df_fleet['total_unique_drives'].iloc[0]:,} <span style='font-size:1rem;'>Assets</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Section
    c1, c2 = st.columns([1.6, 1])
    
    with c1:
        st.subheader("Annualized Failure Rate (AFR %) by Model")
        fig_bar = px.bar(
            filtered_df_models,
            x='annualized_failure_rate_pct',
            y='model',
            orientation='h',
            color='reliability_tier',
            color_discrete_map={
                'CRITICAL_RISK': '#ef4444',
                'MODERATE_RISK': '#f59e0b',
                'LOW_RISK': '#10b981'
            },
            text_auto='.2f',
            labels={'annualized_failure_rate_pct': 'Annualized Failure Rate (AFR %)', 'model': 'Drive Model'}
        )
        fig_bar.add_vline(x=critical_threshold, line_dash="dash", line_color="#ef4444", annotation_text=f"Critical Limit ({critical_threshold}%)")
        fig_bar.update_layout(template="plotly_dark", height=380, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        st.subheader("S.M.A.R.T. Degradation Multiplier")
        fig_pie = px.pie(
            df_smart,
            names='smart_health_status',
            values='annualized_failure_rate_pct',
            color='smart_health_status',
            color_discrete_map={
                'Elevated SMART Anomaly (SMART 5/197 > 0)': '#ef4444',
                'Healthy SMART Profile (SMART 5 & 197 = 0)': '#10b981'
            },
            hole=0.4
        )
        fig_pie.update_layout(template="plotly_dark", height=380, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    # Table View
    st.subheader("Model Reliability Data Table")
    st.dataframe(filtered_df_models, use_container_width=True)

else:
    st.markdown("<div class='main-header'>🔍 Legacy Inventory Data Quality Audit</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Detailed audit findings on 10,000 organizational hardware records</div>", unsafe_allow_html=True)
    
    st.warning("""
    **Data Quality Finding:** An audit of the raw dataset (`01_IT_ASSESMENT(raw data).xlsx`) revealed that 100% of the 10,000 records share identical static timestamps:
    - `LastServiceDate = 2025-04-29`
    - `NextServiceDue = 2025-04-30`
    
    **Analytical Action Taken:** Evaluating standard overdue formulas on historical snapshots marks 100% of assets as overdue. This was documented as a dataset limitation, and metrics were recalibrated to 'Current Repair Prevalence' (10.28%).
    """)
    
    # Category Distribution
    inv_data = pd.DataFrame({
        "Category": ["Monitors", "Laptops", "Printers", "Routers", "Keyboards"],
        "Total Units": [2015, 2011, 2008, 1988, 1978],
        "Under Repair": [215, 207, 185, 191, 230],
        "Current Repair Prevalence (%)": [10.67, 10.29, 9.21, 9.61, 11.63]
    })
    
    fig_inv = px.bar(
        inv_data,
        x="Category",
        y="Current Repair Prevalence (%)",
        color="Current Repair Prevalence (%)",
        color_continuous_scale="Reds",
        text_auto=".2f"
    )
    fig_inv.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_inv, use_container_width=True)
    
    st.dataframe(inv_data, use_container_width=True)
