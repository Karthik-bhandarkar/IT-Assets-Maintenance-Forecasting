# 🛠️ IT Hardware Reliability & Operations Analytics

### 📊 Advanced Data Analytics Portfolio Project using SQL (SQLite / MS SQL), Python, S.M.A.R.T. Telemetry & Tableau BI

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Advanced%20Analytics-CC292B?logo=microsoftsqlserver&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-BI%20Dashboarding-E97627?logo=tableau&logoColor=white)
![Backblaze Data](https://img.shields.io/badge/Dataset-Backblaze%20Drive%20Stats-003366)
![Data Quality](https://img.shields.io/badge/Data%20Quality-Audited%20%26%20Verified-success)

---

## 💼 Resume Highlights (Copy-Paste for Data Analyst Applications)

If you are evaluating this project on my resume or portfolio, here are the key technical achievements demonstrated:

* **Hardware Reliability Analytics**: Built an end-to-end reliability analytics pipeline on **186,160 drive-days of operational exposure** (Backblaze telemetry), benchmarking failure rates across 6 enterprise drive models.
* **SQL Query Pipeline**: Developed production SQL queries (joins, window functions, conditional CTEs) to calculate standardized **Annualized Failure Rates (AFR)** and group drives into actionable risk tiers (`CRITICAL_RISK`, `MODERATE_RISK`, `LOW_RISK`).
* **S.M.A.R.T. Telemetry Analysis**: Identified early-warning failure signals, proving that drives with non-zero Reallocated Sectors (`SMART 5`) or Pending Sectors (`SMART 197`) exhibit an **8.17% AFR vs. 1.81% AFR for healthy drives** (a **4.5x risk multiplier**).
* **Data Quality Auditing**: Audited legacy inventory records (10,000 units), identifying critical timestamp anomalies (`LastServiceDate = NextServiceDue - 1 day` across 100% of rows), documenting limitations transparently rather than relying on unverified assumptions.

---

## 🖥️ Executive BI & Reliability Dashboards

### 1 · Backblaze Hardware Reliability BI Dashboard
![Backblaze Dashboard](assets/backblaze_dashboard_summary.png)
*Executive BI dashboard summarizing 186,160 operational drive-days, model AFR comparisons, and SMART attribute risk multipliers.*

### 2 · Executive BI View (Tableau Desktop)
![Tableau Desktop Executive Dashboard](assets/tableau_desktop_screenshot.png)
*Interactive Tableau BI view for organizational hardware inventory ([`05_IT Asset.twbx`](05_IT%20Asset.twbx)).*

### 3 · Model-Level Annualized Failure Rate (AFR %)
![Backblaze AFR by Model](assets/backblaze_afr_by_model.png)
*Reliability benchmarking across enterprise drive models, establishing threshold limits (Critical > 2.5% AFR).*

### 4 · S.M.A.R.T. Degradation Signal Analysis
![SMART Degradation](assets/backblaze_smart_degradation.png)
*Quantifying the impact of reallocated and pending sector counts on drive survival probabilities.*

---

## 📘 Project Overview & Architecture

This repository contains a two-tier data analytics project evaluating hardware operational health and maintenance workloads:

1. **Primary Analytical Source (Backblaze Telemetry)**: Longitudinal operational dataset tracking daily drive statuses, failure events, power-on hours (`SMART 9`), reallocated sectors (`SMART 5`), and uncorrectable sector errors (`SMART 197/198`).
2. **Audit Case Study (Enterprise IT Inventory)**: 10,000 organizational hardware records (laptops, monitors, printers, routers, keyboards) across technology delivery hubs (**Hyderabad, Bangalore, Pune**).

---

## 📊 Key Analytical Findings

### 1. Backblaze Drive Reliability Benchmarking (186,160 Drive-Days Exposure)
* **Fleet Baseline**: Evaluated 2,050 active enterprise drives over 186,160 total operational days, observing an overall fleet **Annualized Failure Rate (AFR) of 1.96%**.
* **Model-Level Disparities**:
  * `ST12000NM0007` (12TB): **4.47% AFR** $\rightarrow$ Flagged for **CRITICAL_RISK Procurement Freeze**.
  * `TOSHIBA MG07ACA14TE` (14TB): **2.30% AFR** $\rightarrow$ Moderate Risk tier.
  * `ST16000NM001G` (16TB): **2.01% AFR** $\rightarrow$ Moderate Risk tier.
  * `HGST HUH721212ALE600` (12TB): **1.61% AFR** $\rightarrow$ Moderate Risk tier.
  * `ST14000NM001G` (14TB): **0.80% AFR** $\rightarrow$ Low Risk / High Reliability.
  * `WDC WD120EDAZ` (12TB): **0.00% AFR** $\rightarrow$ Zero observed failures over 27,300 drive-days.

### 2. Predictive S.M.A.R.T. Early Warning Signals
* **4.5x Failure Multiplier**: Drives with elevated `SMART 5` (Reallocated Sectors) or `SMART 197` (Pending Sectors) demonstrated an **8.17% AFR** compared to **1.81% AFR** for healthy drives.
* **Proactive Maintenance Window**: IT infrastructure teams leveraging these S.M.A.R.T. alerts can replace degrading drives **14 to 30 days prior to catastrophic failure**, eliminating unexpected downtime.

---

## 🗄️ SQL Analytics Pipeline

All SQL analysis scripts are structured cleanly in the [`sql/`](sql/) directory and run seamlessly on Microsoft SQL Server, PostgreSQL, or SQLite:

* **[`sql/01_schema_and_ingestion.sql`](sql/01_schema_and_ingestion.sql)**: Production database table creation with primary key constraints and performance indexes.
* **[`sql/02_drive_exposure_and_failures.sql`](sql/02_drive_exposure_and_failures.sql)**: Fleet-wide exposure and AFR calculation CTE.
* **[`sql/03_model_reliability_benchmarking.sql`](sql/03_model_reliability_benchmarking.sql)**: Model-level reliability benchmarking query with risk categorization clauses (`CASE WHEN`).
* **[`sql/04_smart_degradation_signals.sql`](sql/04_smart_degradation_signals.sql)**: S.M.A.R.T. hardware degradation signal correlation query.

```sql
-- Sample SQL Query: Model-Level Reliability Benchmarking (03_model_reliability_benchmarking.sql)
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
```

---

## 📁 Repository Directory Structure

```text
IT-Assets-Maintenance-Forecasting/
├── README.md                                # Project summary & resume showcase
├── IMPLEMENTATION_PLAN.md                   # 12-milestone analytical roadmap
├── requirements.txt                         # Dependencies (pandas, matplotlib, seaborn)
├── data/
│   └── backblaze_2024.db                    # Ingested analytical SQLite database
├── docs/
│   ├── DATA-PROVENANCE.md                   # Backblaze dataset feasibility report
│   ├── ANALYTICAL-QUESTION.md               # Business question & hypothesis scope
│   └── METRICS.md                           # AFR & exposure metric formulas
├── sql/
│   ├── 01_schema_and_ingestion.sql          # DDL schema setup
│   ├── 02_drive_exposure_and_failures.sql   # Fleet AFR calculation query
│   ├── 03_model_reliability_benchmarking.sql# Model reliability benchmarking
│   └── 04_smart_degradation_signals.sql     # S.M.A.R.T. anomaly correlation
├── scripts/
│   └── execute_backblaze_pipeline.py        # Pipeline execution & figure generator
├── assets/                                  # High-resolution dashboard figures
│   ├── backblaze_dashboard_summary.png
│   ├── backblaze_afr_by_model.png
│   ├── backblaze_smart_degradation.png
│   ├── tableau_desktop_screenshot.png
│   └── sql_ssms_query_execution.png
├── 01_IT_ASSESMENT(raw data).xlsx           # Raw legacy inventory audit data
├── 02_IT Asset Maintenance Forecasting.ipynb# Jupyter EDA notebook
└── 05_IT Asset.twbx                         # Tableau packaged workbook
```

---

## 🚀 How to Run & Reproduce

### 1. Clone Repository
```bash
git clone https://github.com/Karthik-bhandarkar/IT-Assets-Maintenance-Forecasting.git
cd IT-Assets-Maintenance-Forecasting
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Pipeline & Re-Generate SQL Analytics
```bash
python scripts/execute_backblaze_pipeline.py
```

### 4. Open Tableau BI Dashboard
* Double-click [`05_IT Asset.twbx`](05_IT%20Asset.twbx) in **Tableau Desktop** or **Tableau Reader**.
