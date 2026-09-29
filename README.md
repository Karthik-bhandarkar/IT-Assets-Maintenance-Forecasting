# 🛠️ IT Asset Maintenance Forecasting

### 📊 Data Analytics & Forecasting Pipeline using Python, MS SQL & Tableau

![Python](https://img.shields.io/badge/Python-Data%20Analysis-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-orange)
![SQL Server](https://img.shields.io/badge/MS%20SQL-Database-green)
![Tableau](https://img.shields.io/badge/Tableau-Dashboarding-blueviolet)

---

## 📘 Project Overview

The **IT Asset Maintenance Forecasting** project analyzes hardware performance, failure patterns, and upcoming service schedules for organizational IT assets (such as laptops, desktops, printers, and network devices).

The objective is to transition from reactive repairs to **predictive and proactive maintenance**, reducing equipment downtime, ensuring uninterrupted business operations, and optimizing lifecycle replacement costs.

---

## 📁 Repository Structure

| File | Description |
|------|-------------|
| **`01_IT_ASSESMENT(raw data).xlsx`** | Original dataset containing IT hardware records, purchase dates, last service dates, and operational status. |
| **`02_IT Asset Maintenance Forecasting.ipynb`** | Jupyter notebook performing data cleaning, null handling, datetime conversion, feature engineering, and exploratory data analysis. |
| **`03_IT Asset Maintenance Forecasting(for sql).xlsx`** | Processed and feature-enriched dataset ready for database ingestion. |
| **`04_SQLQuery5.sql`** | SQL scripts for table schema definition, data staging, aggregate analytics, and 30-day maintenance forecasting queries. |
| **`05_IT Asset.twbx`** | Packaged Tableau workbook with interactive KPI cards, heatmaps, failure rates, and geographic distribution views. |
| **`Project Documentation_ IT Asset Maintenance Forecasting.pdf`** | Comprehensive project report and executive documentation. |
| **`requirements.txt`** | Python library dependencies required to reproduce the notebook analysis. |

---

## 🧠 Key Objectives

- **Asset Health Monitoring**: Track the operational status (`Working` vs. `Under Repair`) across equipment categories.
- **Predictive Service Planning**: Identify all hardware requiring service within the next **30 days** (`DaysUntilDue < 30`).
- **Failure Analysis**: Quantify failure rates across equipment types and identify maintenance hotspots by office location.
- **Executive Dashboarding**: Present real-time actionable insights in Tableau with multi-dimensional filtering.

---

## 🧰 Technology Stack

| Component | Technology / Library | Purpose |
|-----------|----------------------|---------|
| **Programming Language** | Python (>= 3.9) | Data cleaning, transformation & feature engineering |
| **Libraries** | Pandas, NumPy, Matplotlib, Seaborn, openpyxl | Data processing & exploratory data visualization |
| **Database** | Microsoft SQL Server | Centralized relational data warehouse & SQL querying |
| **Visualization** | Tableau Desktop / Reader | Packaged interactive dashboards & executive KPIs |
| **Environment** | Jupyter Notebook / VS Code | Development & exploratory pipeline execution |

---

## 🚀 Project Workflow

### Phase 1: Data Analysis & Feature Engineering (Python)
- **Data Ingestion & Cleaning**:
  - Ingested `01_IT_ASSESMENT(raw data).xlsx`.
  - Audited missing values and standardized datetime fields (`PurchaseDate`, `LastServiceDate`, `NextServiceDue`).
- **Feature Engineering**:
  - `AssetAge`: Calculated elapsed days from purchase date to current date.
  - `DaysSinceLastService`: Calculated days since the previous service event.
  - `DaysUntilDue`: Forecasted remaining days until the scheduled service due date.
- **Exploratory Data Analysis (EDA)**:
  - Distribution and frequency of asset categories.
  - Breakdown of failure rates by equipment type (`Under Repair` vs `Working`).
  - Flagged critical at-risk assets where maintenance is due within 30 days.
- **Export**: Saved cleaned dataset as `03_IT Asset Maintenance Forecasting(for sql).xlsx`.

### Phase 2: Relational Database & SQL Analytics (MS SQL Server)
- **Schema Creation**: Created structured table `ITAssets` with primary keys and data types (`VARCHAR`, `DATE`, `INT`).
- **Data Loading**: Populated `ITAssets` from the staged Excel data.
- **Analytical Queries**:
  - Aggregated asset counts grouped by `AssetType` and `Location`.
  - Filtered high-priority assets due in the next 30 days:
    ```sql
    SELECT *
    FROM ITAssets
    WHERE NextServiceDue BETWEEN GETDATE() AND DATEADD(DAY, 30, GETDATE())
    ORDER BY NextServiceDue ASC;
    ```

### Phase 3: Interactive Dashboarding (Tableau)
- **Dashboard Highlights**:
  - **KPI Cards**: Total active assets, assets under repair, and assets due within 30 days.
  - **Asset Distribution**: Bar chart displaying volume per equipment category.
  - **Repair Concentration**: Bubble chart illustrating failure frequency by hardware type.
  - **Location Heatmap**: Cross-tabulation of asset volume across branches and regional offices.
  - **Global Filters**: Interactive slicing by `Location` and `AssetType`.

---

## 🔧 How to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Swati-Devas/IT-Assets-Maintenance-Forecasting.git
   cd IT-Assets-Maintenance-Forecasting
   ```

2. **Set Up Python Environment**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Data Analysis**:
   Open and execute `02_IT Asset Maintenance Forecasting.ipynb` in Jupyter Notebook or VS Code.

4. **Load to SQL Database**:
   Execute the scripts in `04_SQLQuery5.sql` within SQL Server Management Studio (SSMS).

5. **Explore Tableau Dashboard**:
   Open `05_IT Asset.twbx` using Tableau Desktop or the free Tableau Reader.
