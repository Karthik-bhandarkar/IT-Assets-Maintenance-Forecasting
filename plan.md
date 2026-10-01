# Technical Audit Report: IT Asset Maintenance Forecasting

**Target Repository:** `https://github.com/Swati-Devas/IT-Assets-Maintenance-Forecasting.git`  
**Inspection Date:** 2026-09-29  

---

# 1. REPOSITORY INVENTORY

### Relevant File Tree
```text
IT-Assets-Maintenance-Forecasting/
├── .gitignore
├── requirements.txt
├── README.md
├── 01_IT_ASSESMENT(raw data).xlsx
├── 02_IT Asset Maintenance Forecasting.ipynb
├── 03_IT Asset Maintenance Forecasting(for sql).xlsx
├── 04_SQLQuery5.sql
├── 05_IT Asset.twbx
├── Project Documentation_ IT Asset Maintenance Forecasting.pdf
└── plan.md
```
*(Excluded: `.git/` directory and internal environment logs).*

### Purpose of Every Relevant File
| File | Format | Purpose |
| :--- | :--- | :--- |
| `.gitignore` | Plain text | Ignores Python bytecode, Jupyter checkpoints, Excel temporary lock files, and IDE metadata. |
| `requirements.txt` | Plain text | Lists Python package dependencies (`pandas`, `numpy`, `matplotlib`, `seaborn`, `openpyxl`, `ipykernel`). |
| `README.md` | Markdown | Project documentation detailing the overview, repository structure, tech stack, 3-phase workflow, and execution steps. |
| `01_IT_ASSESMENT(raw data).xlsx` | MS Excel (`.xlsx`) | Raw source dataset containing 10,000 IT asset records across 7 baseline columns. |
| `02_IT Asset Maintenance Forecasting.ipynb` | Jupyter Notebook | End-to-end Python pipeline for data ingestion, datetime casting, feature engineering, exploratory data analysis, visualizations, and clean export. |
| `03_IT Asset Maintenance Forecasting(for sql).xlsx` | MS Excel (`.xlsx`) | Cleaned and feature-enriched dataset containing 10,000 records across 10 columns formatted for database staging. |
| `04_SQLQuery5.sql` | SQL Script | DDL and DML scripts for MS SQL Server table creation, data loading from staging, aggregation queries, and upcoming 30-day maintenance filters. |
| `05_IT Asset.twbx` | Tableau Packaged Workbook | ZIP-compressed bundle containing Tableau XML definitions (`Book1.twb`) and embedded data extract (`Data/TableauTemp/*.hyper`). |
| `Project Documentation_ IT Asset Maintenance Forecasting.pdf` | PDF (4 pages) | Formal project specifications and phase-by-phase task breakdown document. |

### Files Actually Opened and Inspected
All files in the repository were opened and inspected:
1. `.gitignore` (Text inspection)
2. `requirements.txt` (Text inspection)
3. `README.md` (Text inspection)
4. `01_IT_ASSESMENT(raw data).xlsx` (Parsed via `openpyxl` & `pandas`)
5. `02_IT Asset Maintenance Forecasting.ipynb` (Parsed via JSON structure, cell sources, metadata, and python kernel execution)
6. `03_IT Asset Maintenance Forecasting(for sql).xlsx` (Parsed via `openpyxl` & `pandas`)
7. `04_SQLQuery5.sql` (Parsed via binary byte inspection and text review)
8. `05_IT Asset.twbx` (Extracted and parsed via `zipfile` and `xml.etree.ElementTree` on `Book1.twb`)
9. `Project Documentation_ IT Asset Maintenance Forecasting.pdf` (Parsed text across all 4 pages via `pypdf`)

### Files / Artifacts That Could Not Be Fully Inspected
* **`05_IT Asset.twbx -> Data/TableauTemp/TEMP_0xu80ri0g3pi4w15smasf0b6js4w.hyper`**: The inner `.hyper` file is Tableau's proprietary compiled binary format; raw binary records were not extracted directly from it. However, the complete workbook configuration, calculations, charts, and data source bindings were inspected via the accompanying `Book1.twb` XML.

---

# 2. README AND PROJECT CLAIMS

### Stated Problem, Features, and Setup
* **Current Title**: IT Asset Maintenance Forecasting
* **Stated Problem**: High organizational asset downtime, reactive maintenance overhead, lack of centralized visibility across offices (Bangalore, Hyderabad, Pune).
* **Stated Features**: Data ingestion, date normalization, feature engineering of asset age and service due intervals, failure rate computation by category, SQL relational storage, Tableau executive dashboards with interactive multi-sheet filters.
* **Screenshots**: None found in repository.
* **Demo / Deployment Links**: None provided.

### Claims of Prediction, Forecasting, Accuracy, and Impact
* **Claimed**: "transition from reactive repairs to predictive and proactive maintenance", "forecast maintenance needs", "Scikit-learn" (in PDF documentation).
* **Observed Reality in Code**:
  * **No Machine Learning or Statistical Forecasting model exists.** Scikit-learn is not imported or used anywhere in the notebook or scripts.
  * "Forecasting" is implemented solely through deterministic date arithmetic: `DaysUntilDue = NextServiceDue - CurrentDate` and filtering `DaysUntilDue < 30`.
  * No accuracy metrics (MAE, RMSE, ROC-AUC, F1, precision/recall) exist.
  * Stated business impacts ("reduce asset downtime", "manage IT budgets more effectively") are qualitative objectives rather than measured experimental outcomes.

---

# 3. TECHNOLOGY AND ARCHITECTURE

### Languages, Frameworks, and Dependencies
* **Python**: 3.9+ (verified running on Python 3.13)
* **Libraries Specified in `requirements.txt`**:
  * `pandas>=2.0.0`
  * `numpy>=1.24.0`
  * `matplotlib>=3.7.0`
  * `seaborn>=0.12.0`
  * `openpyxl>=3.1.0`
  * `ipykernel>=6.0.0`
* **Database Engine**: Microsoft SQL Server (T-SQL syntax in `04_SQLQuery5.sql`)
* **Business Intelligence / Reporting**: Tableau Desktop / Tableau Reader (Tableau workbook XML format 18.1)

### Entrypoints and Exact Commands to Run
1. **Python / Notebook**:
   ```bash
   pip install -r requirements.txt
   jupyter notebook "02_IT Asset Maintenance Forecasting.ipynb"
   ```
2. **Database**:
   Open `04_SQLQuery5.sql` in SQL Server Management Studio (SSMS) or Azure Data Studio and execute against an active SQL Server instance with a staging sheet `Sheet1$`.
3. **Tableau**:
   Double click `05_IT Asset.twbx` to open directly in Tableau Desktop or Tableau Reader.

### Actual Data Flow
```text
01_IT_ASSESMENT(raw data).xlsx (10,000 rows, 7 cols)
      │
      ▼
02_IT Asset Maintenance Forecasting.ipynb (Pandas Feature Engineering)
      │
      ▼
03_IT Asset Maintenance Forecasting(for sql).xlsx (10,000 rows, 10 cols)
      ├──> [Manual Staging / SSMS Import] ──> 04_SQLQuery5.sql (MS SQL Server)
      └──> [Direct Excel Extract / .hyper] ──> 05_IT Asset.twbx (Tableau Dashboard)
```
*Discrepancy noted:* While the documentation states that Tableau connects live to MS SQL Server, `Book1.twb` XML confirms that Tableau connects via `excel-direct` to `Sheet1` of `03_IT Asset Maintenance Forecasting(for sql).xlsx` and packages it into an internal `.hyper` extract.

### Infrastructure & Engineering Components Found
* **Backend Application**: Not found in inspected files.
* **Frontend Web App**: Not found in inspected files.
* **Database / SQL**: Found in `04_SQLQuery5.sql`.
* **Automated Scheduling (Cron/Airflow)**: Not found in inspected files.
* **Automated Tests (`pytest`, `unittest`)**: Not found in inspected files.
* **Containerization (`Dockerfile`, `docker-compose`)**: Not found in inspected files.
* **CI/CD (`.github/workflows`)**: Not found in inspected files.
* **Cloud Deployment**: Not found in inspected files.

---

# 4. DATA AUDIT

### Dataset 1: `01_IT_ASSESMENT(raw data).xlsx`
* **Format**: Microsoft Excel OpenXML Spreadsheet (`.xlsx`), Sheet name: `ITAssets`
* **File Size**: 330,136 bytes (~322 KB)
* **Row Count**: 10,000 records (plus 1 header row)
* **Columns and Inferred Types**:
  1. `AssetID` (string/object): Categorical alphanumeric IDs (`A0` to `A9999`)
  2. `AssetType` (string/object): Categorical hardware type
  3. `PurchaseDate` (datetime64): Date purchased
  4. `LastServiceDate` (datetime64): Date of prior service
  5. `NextServiceDue` (datetime64): Scheduled next maintenance date
  6. `Status` (string/object): Operational state
  7. `Location` (string/object): Office facility
* **Missing Values**: 0 nulls across all columns.
* **Duplicates**: 0 duplicate `AssetID` values (10,000 unique keys).
* **Distributions & Value Ranges**:
  * `AssetType` (5 categories): Monitor (2,015), Laptop (2,011), Printer (2,008), Router (1,988), Keyboard (1,978).
  * `Status` (3 categories): Working (8,470; 84.7%), Under Repair (1,028; 10.28%), Decommissioned (502; 5.02%).
  * `Location` (3 categories): Bangalore (3,376; 33.76%), Pune (3,320; 33.2%), Hyderabad (3,304; 33.04%).
  * `PurchaseDate`: Range from `2020-04-29` to `2024-04-28` (uniform 4-year span).
  * `LastServiceDate`: **Constant value** `2025-04-29` across all 10,000 rows (standard deviation = 0).
  * `NextServiceDue`: **Constant value** `2025-04-30` across all 10,000 rows (standard deviation = 0).
* **Anonymized Sample Rows**:
  ```json
  [
    {"AssetID": "A0", "AssetType": "Monitor", "PurchaseDate": "2021-09-24", "LastServiceDate": "2025-04-29", "NextServiceDue": "2025-04-30", "Status": "Working", "Location": "Hyderabad"},
    {"AssetID": "A1", "AssetType": "Printer", "PurchaseDate": "2023-09-11", "LastServiceDate": "2025-04-29", "NextServiceDue": "2025-04-30", "Status": "Working", "Location": "Hyderabad"},
    {"AssetID": "A2", "AssetType": "Laptop", "PurchaseDate": "2022-12-24", "LastServiceDate": "2025-04-29", "NextServiceDue": "2025-04-30", "Status": "Working", "Location": "Bangalore"}
  ]
  ```
* **Data Provenance**:
  * README states: "Loaded the `01_IT_ASSESMENT(raw data).xlsx` dataset."
  * PDF documentation states: "Load the `IT_ASSESMENT.xlsx - ITAssets.csv` dataset into a Pandas DataFrame."
  * No external URL, company origin, or sensor telemetry source is stated in the repository.
* **Content Signal Check**:
  * Contains asset condition status (`Working`, `Under Repair`, `Decommissioned`) and static dates.
  * Does NOT contain maintenance event logs, sensor telemetry (temperature, vibration, hours run), repair cost figures, breakdown logs, or predictive target labels.
* **Realism Assessment**: **Definitively Synthetic.**
  * *Evidence:* (1) Exactly 10,000 rows; (2) Sequential IDs `A0`–`A9999`; (3) Perfectly balanced 20% splits across 5 hardware categories; (4) Perfectly balanced 33.3% splits across 3 cities; (5) Every single device was serviced on the exact same calendar day (`2025-04-29`) and scheduled for its next service exactly 24 hours later (`2025-04-30`).

---

### Dataset 2: `03_IT Asset Maintenance Forecasting(for sql).xlsx`
* **Format**: Microsoft Excel OpenXML Spreadsheet (`.xlsx`), Sheet name: `Sheet1`
* **File Size**: 451,964 bytes (~441 KB)
* **Row Count**: 10,000 records
* **Columns and Types**: All 7 columns from Dataset 1 plus 3 engineered numerical columns:
  * `AssetAge` (int64): Min 558 days (~1.5 yrs), Mean 1,280 days (~3.5 yrs), Max 2,018 days (~5.5 yrs).
  * `DaysSinceLastService` (int64): Constant `192` across all 10,000 rows (reflecting the difference between 2025-04-29 and the notebook execution date in November 2025).
  * `DaysUntilDue` (int64): Constant `-192` across all 10,000 rows.
* **Missing Values**: 0 nulls.

---

# 5. SOURCE CODE AND LOGIC

### 5.1. SQL Script: `04_SQLQuery5.sql`

```sql
-- Create table to store IT asset and maintenance details
CREATE TABLE ITAssets (
    AssetID VARCHAR(50) PRIMARY KEY,      -- Unique asset identifier
    AssetType VARCHAR(100),               -- Category (Laptop, Desktop, Printer, etc.)
    PurchaseDate DATE,                    -- Date asset was purchased
    LastServiceDate DATE,                 -- Most recent service/maintenance date
    NextServiceDue DATE,                  -- Scheduled next service date
    Status VARCHAR(50),                   -- Current operational status
    Location VARCHAR(100),                -- Physical location / department
    AssetAge INT,                         -- Asset age (in years)
    DaysSinceLastService INT,             -- Days elapsed since last service
    DaysUntilDue INT                      -- Days remaining until next service
);

-- Insert data from staging sheet (imported Excel)
INSERT INTO ITAssets (
    AssetID, AssetType, PurchaseDate, LastServiceDate, NextServiceDue,
    Status, Location, AssetAge, DaysSinceLastService, DaysUntilDue
)
SELECT
    AssetID, AssetType, PurchaseDate, LastServiceDate, NextServiceDue,
    Status, Location, AssetAge, DaysSinceLastService, DaysUntilDue
FROM Sheet1$;

-- View all asset records
SELECT * 
FROM ITAssets;

-- Count total assets grouped by type and location
SELECT 
    AssetType,
    Location,
    COUNT(*) AS TotalAssets
FROM ITAssets
GROUP BY AssetType, Location
ORDER BY AssetType, Location;

-- Assets due for service in the next 30 days
SELECT *
FROM ITAssets
WHERE NextServiceDue BETWEEN GETDATE() AND DATEADD(DAY, 30, GETDATE());

-- Upcoming service schedule sorted by nearest due date
SELECT NextServiceDue
FROM ITAssets
ORDER BY NextServiceDue ASC;
```

#### SQL Query Analysis & Logical Vulnerabilities
1. **Schema Mismatch on Line 10**:
   The comment states `-- Asset age (in years)`, but the values inserted from Python are computed in days (e.g., `1505`, `788`).
2. **Staging Dependency on Line 23**:
   `FROM Sheet1$;` assumes the user has created an open datasource or imported the Excel sheet named `Sheet1$` using SSMS Import and Export Wizard.
3. **Execution Date Vulnerability on Lines 40–41**:
   `WHERE NextServiceDue BETWEEN GETDATE() AND DATEADD(DAY, 30, GETDATE())`:
   Because all `NextServiceDue` dates in the dataset are `2025-04-30`, executing this query on any date after May 1, 2025 yields **0 rows**. It only returned rows if executed between April 1, 2025 and April 30, 2025.

---

### 5.2. Jupyter Notebook: `02_IT Asset Maintenance Forecasting.ipynb`

#### Logic by Cell Range
* **Cells 0–2: Imports & Environment**
  ```python
  import numpy as np
  import pandas as pd
  import matplotlib.pyplot as plt
  import seaborn as sns
  ```
* **Cells 3–4: Ingestion**
  ```python
  import os
  input_file = '01_IT_ASSESMENT(raw data).xlsx' if os.path.exists('01_IT_ASSESMENT(raw data).xlsx') else 'IT_ASSESMENT.xlsx'
  df = pd.read_excel(input_file)
  df.head()
  ```
* **Cells 5–7: Data Quality Audit**
  Executes `df.isnull().sum()` and `df.info()`. (Result: 10,000 non-null values across all columns).
* **Cells 8–9: Datetime Conversion**
  ```python
  date_cols = ['PurchaseDate', 'LastServiceDate', 'NextServiceDue']
  for col in date_cols:
      df[col] = pd.to_datetime(df[col])
  ```
* **Cells 10–11: Feature Engineering**
  ```python
  from datetime import datetime

  current_date = datetime.now()
  df['AssetAge'] = (current_date - df['PurchaseDate']).dt.days
  df['DaysSinceLastService'] = (current_date - df['LastServiceDate']).dt.days
  df['DaysUntilDue'] = (df['NextServiceDue'] - current_date).dt.days
  ```
* **Cells 12–13: Asset Type Distribution Plot**
  Computes `df['AssetType'].value_counts()` and renders `sns.countplot(x='AssetType', data=df)`.
* **Cells 14–15: Failure Rate Calculation**
  ```python
  status_counts = df.groupby(['AssetType', 'Status']).size().unstack()
  status_counts['FailureRate (%)'] = (status_counts['Under Repair'] / status_counts.sum(axis=1)) * 100
  print(status_counts)
  sns.barplot(x=status_counts.index, y=status_counts['FailureRate (%)'])
  ```
  *Output:* Keyboards (11.6%), Monitors (10.7%), Laptops (10.3%), Routers (9.6%), Printers (9.2%).
* **Cells 16–17: Descriptive Statistics**
  `df[['AssetAge', 'DaysSinceLastService']].describe()`
* **Cells 18–19: At-Risk Filtering Logic**
  ```python
  at_risk_assets = df[df['DaysUntilDue'] < 30]
  print("Number of At-Risk Assets:", len(at_risk_assets))
  ```
  *Flaw:* Because `DaysUntilDue` is negative (e.g. -192), the condition `-192 < 30` evaluates to `True` for **all 10,000 assets**, flagging 100% of the fleet as "due for maintenance".
* **Cells 20–21: At-Risk Grouping & Plot**
  ```python
  at_risk_count = df[df['DaysUntilDue'] < 30].groupby(['AssetType', 'Location']).size().reset_index(name='Count')
  sns.barplot(x='AssetType', y='Count', hue='Location', data=at_risk_count)
  ```
* **Cell 22: Export**
  ```python
  output_file = '03_IT Asset Maintenance Forecasting(for sql).xlsx'
  df.to_excel(output_file, index=False)
  ```

---

### 5.3. Tableau Workbook: `05_IT Asset.twbx`

Inspected via `Book1.twb` XML tree:
* **Worksheets Found (5)**:
  1. `Sheet 1`: *Asset Distribution by Type* (Bar chart of hardware counts).
  2. `Sheet 2`: *KPI - Assets Due Soon* (Single big number / KPI card).
  3. `Sheet 3`: *Assets Under Repair* (Packed bubble chart sized by repair volume, colored by `AssetType`).
  4. `Sheet 4`: *Asset Type Distribution Across Locations - Heatmap of Asset Counts* (Matrix of `AssetType` vs. `Location`).
  5. `Sheet 5`: *Geographic Asset Overview* (Symbol map visualising city counts).
* **Dashboards Found (1)**:
  * `Dashboard 1`: Integrates Sheets 1 through 5 with interactive quick-filter controls on `Location` and `AssetType`.
* **Data Connection Details**:
  * Connection class: `excel-direct`
  * Embedded extract: `Data/TableauTemp/TEMP_0xu80ri0g3pi4w15smasf0b6js4w.hyper`

---

# 6. TESTING, OPERATIONS, AND SECURITY

### Testing
* **Automated Unit / Integration Tests**: None found.
* **Validation Scripts**: No data validation framework (such as Great Expectations, Pydantic, or pytest) is present.

### Operations, Logging, and Error Handling
* **Error Handling**: Code contains no `try...except` blocks or SQL transaction error handlers (`BEGIN TRY / BEGIN CATCH`).
* **Logging**: No standard Python `logging` module is configured; standard stdout `print()` calls are used in the notebook.
* **Configuration**: Hardcoded file strings throughout; no external `.env`, `.yaml`, or config management.

### Security and Secrets Audit
* **Credentials / API Keys / Tokens**: None found.
* **Database Connection Strings**: The SQL file provides standalone query text without embedded passwords or remote server IPs.
* **PII (Personally Identifiable Information)**: None found. The dataset contains only synthetic asset identifiers (`A0`–`A9999`) and physical city locations (`Bangalore`, `Hyderabad`, `Pune`).

### Reproducibility
* Anyone can clone the repository, run `pip install -r requirements.txt`, and execute `02_IT Asset Maintenance Forecasting.ipynb` or open `05_IT Asset.twbx` immediately without configuration.

---

# 7. EVIDENCE INDEX

| Claim / Component | Evidence (File Path & Location) | Verification Status | Notes / Findings |
| :--- | :--- | :--- | :--- |
| **Python Data Cleaning & Transformation** | `02_IT Asset Maintenance Forecasting.ipynb: Cells 2-11` | **Verified** | Datetime conversions and feature engineering execute cleanly. |
| **Machine Learning / Predictive Modeling** | `Project Documentation_...pdf: Page 1, Section 2.0` | **Unverified (False Claim)** | PDF claims "Scikit-learn", but scikit-learn is neither imported nor used anywhere in the codebase. |
| **Relational Database DDL & Queries** | `04_SQLQuery5.sql: Lines 1-46` | **Verified** | Standard T-SQL statements for schema creation and analytical grouping. |
| **Tableau Live SQL Server Connection** | `README.md: Lines 85-86`, `PDF: Page 3, Task 3.1` | **Unverified (False Claim)** | `Book1.twb` XML proves Tableau connects via `excel-direct` to the Excel file, not live to MS SQL Server. |
| **Tableau Packaged Dashboard** | `05_IT Asset.twbx: Book1.twb` | **Verified** | Contains 5 active worksheets and 1 interactive dashboard with embedded Hyper extract. |
| **30-Day Predictive Forecasting** | `02_IT Asset Maintenance Forecasting.ipynb: Cell 19`, `04_SQLQuery5.sql: Lines 40-41` | **Partially Verified (Heuristic Only)** | Uses simple date difference `DaysUntilDue < 30`. Because dates are static (`2025-04-30`), 100% of rows are marked overdue. |
| **Dataset Completeness (No Nulls)** | `01_IT_ASSESMENT(raw data).xlsx` | **Verified** | Exactly 10,000 rows across 7 columns with zero missing values. |

---

# 8. OPEN QUESTIONS

1. **Source of Raw Dataset**: The repository does not state whether `01_IT_ASSESMENT(raw data).xlsx` was generated using a synthetic script (e.g., Faker/NumPy), assigned as an academic/interview project prompt, or adapted from an existing template.
2. **Intended Schedule Anchor**: It is unclear whether `NextServiceDue` was intended to remain fixed at `2025-04-30` as a historic snapshot or whether it was intended to have variable dates distributed across the year.
3. **Database Deployment Context**: There is no documentation regarding the target MS SQL Server version, database name, or whether a staging database was ever hosted externally.

---

# PART II: DATA ANALYTICS PROJECT TRANSFORMATION BLUEPRINT
## From “IT Asset Maintenance Forecasting” to a defensible engineering portfolio project

This blueprint is based on the **technical audit report above**, evaluating reported code, SQL, data distributions, and workbook connections, distinguishing **reported evidence** from **proposed work**. Nothing below is presented as already built.

## Executive verdict

**Brutally honest assessment:** The current repository demonstrates that you can use Pandas, write introductory SQL, and build a Tableau dashboard. It does **not** currently demonstrate forecasting, a production data pipeline, an integrated database-backed application, or substantial software engineering.

The most damaging issue is not the absence of a fancy model. It is that the project **claims a stronger system than its evidence supports**:

- All 10,000 assets reportedly have `LastServiceDate = 2025-04-29` and `NextServiceDue = 2025-04-30`.
- “Forecasting” means subtracting today’s date from the scheduled due date.
- The notebook’s `DaysUntilDue < 30` flags overdue records as well as upcoming records. With the supplied historical dates, it flags the whole fleet.
- The Tableau workbook reportedly reads an Excel extract, **not SQL Server**, despite the documented SQL-to-Tableau story.
- “Under Repair” is treated as a **failure rate**, although a single current status is not a historical failure event.

**Hiring decision today:** For a strong software-engineering role, this would probably be a supporting beginner project, not the project that wins the interview. It can become a strong fresher project if you **correct the claims, redesign the data problem, build a coherent application, and provide reproducible proof**.

---

# 1. Existing-project audit

## What exists, based on the supplied inspection

| Question | Current answer |
|---|---|
| **Claimed problem** | Predictive/proactive IT asset maintenance and reduced downtime |
| **Actual supported problem** | Examining an inventory snapshot and identifying scheduled service dates and current statuses |
| **Likely user** | IT operations or asset-management staff; not explicitly validated |
| **Raw data** | Excel file: 10,000 assets, 7 fields—ID, type, purchase date, last service date, next due date, status, location |
| **Provenance** | Not documented. The regular distributions strongly suggest synthetic data, but its origin is **unverified** |
| **Processing** | Jupyter/Pandas reads Excel, converts dates, derives three date differences, creates plots, exports Excel |
| **Storage** | Excel files; a SQL Server table/script exists, but the reported dashboard does not use it |
| **SQL** | One table, staging-dependent insert, basic grouping, due-date filter |
| **Dashboard** | Packaged Tableau workbook with five worksheets and one dashboard; reportedly backed by an Excel extract |
| **Backend/API** | None reported |
| **Automated tests/pipeline** | None reported |
| **Deployment** | Local notebook and Tableau workbook; no live application reported |
| **Proof** | Code, sample data, SQL, workbook, README, PDF. No reported screenshots, live demo, test results, evaluation, or measured business result |

### What the dataset actually allows

The raw file is **one row per asset**, not a maintenance-event history. A current `Status = Under Repair` is a **snapshot of repair state**, not proof of how often that asset fails.

The two service-date fields are constant across all 10,000 assets. Consequently:

- No useful variation exists for prioritizing by scheduled service date.
- You cannot learn a meaningful failure forecast from the reported dataset.
- You cannot measure whether your intervention reduced downtime or repair cost; those outcomes are absent.
- A dashboard can still demonstrate data handling, but it cannot honestly claim operational forecasting from this input.

**Critical distinction:** “This asset is scheduled for service on a known date” is **schedule reporting**. “This asset is likely to fail in the next 30 days” is **prediction**. They are different problems requiring different evidence.

---

# 2. Recruiter and engineering-manager weakness matrix

**Severity:** Critical = credibility or core-logic issue; High = limits interview value; Medium = worthwhile improvement.

| Area | Reported current state | Why I would question it as a reviewer | Severity | Specific fix and proof |
|---|---|---|---|---|
| **Project title** | “Maintenance Forecasting” | No reported forecasting model or evaluation | **Critical** | Rename around planning/decision support unless valid historical data enables forecasting |
| **Business outcome** | Downtime and cost reduction described as goals | Neither downtime nor cost is measured | **Critical** | State the decision supported; report only measured technical or analytical results |
| **Data provenance** | No origin/license/generation method documented | Cannot assess realism or permission to redistribute | **Critical** | Add provenance and limitations; label generated data clearly if applicable |
| **Date distribution** | Same last-service and next-due dates for every asset | Due-soon analysis cannot differentiate assets | **Critical** | Retain original as a documented baseline; obtain suitable data or generate a clearly labeled *scenario* dataset |
| **“Failure rate”** | `Under Repair / all assets` | This is current repair prevalence, not failure incidence | **Critical** | Rename metric **share currently under repair**; calculate failure incidence only from event history |
| **Due-soon logic** | Python uses `< 30`, SQL uses upcoming date range | Inconsistent KPIs; Python includes everything overdue | **Critical** | Define **overdue** and **due in next 30 calendar days** separately; test boundaries |
| **Date calculations** | `datetime.now()` and exported relative-day columns | Results go stale; execution time affects output | **High** | Use explicit `as_of_date`; derive relative values at query/runtime; record the chosen date |
| **Architecture claim** | README implies SQL-backed Tableau; workbook reportedly reads Excel | Reviewer cannot trust the system diagram | **Critical** | Either connect the product to DB or honestly document Excel-backed Tableau as legacy |
| **Database** | One flat table with date-derived values | Weak relationships, constraints, refresh behavior | **High** | Add an appropriately scoped relational model and migration |
| **SQL** | Basic `GROUP BY` and date filter | Limited SQL depth and no meaningful history questions | **High** | Write tested queries tied to actual business questions |
| **Pipeline** | Manual notebook → Excel → manual import | Not repeatable, observable, or safely rerunnable | **High** | CLI ingestion with validation, reject reporting, run log, idempotency |
| **Python** | Notebook is the application logic | Little evidence of modular software design | **High** | Keep notebook for exploration; move tested logic into Python modules |
| **Dashboard** | Distribution charts and a due-soon card | “All assets due” provides no prioritization | **High** | Show data limitations, actionable queues, reasons, and drill-down |
| **Backend/API** | None | Few backend/SWE signals | **High for SWE roles** | Add small FastAPI service **only if** it serves the application meaningfully |
| **Testing** | None reported | Simple date bugs survive unnoticed | **High** | Unit, SQL integration, API, and pipeline rerun tests |
| **Deployment** | Local tools only | Reviewer cannot inspect a running system | **High** | Reproducible Docker setup; deploy a demo if budget/privacy allow |
| **Monitoring** | None | No indication of failed loads or stale data | **Medium** | Last-refresh status, ingestion counts, API health and logs |
| **Security** | No reported secrets, but no deployed service | Security story is untested | **Medium** | Environment variables, parameterized queries, access controls appropriate to deployment |
| **GitHub presentation** | README and PDF but no reported demo/screenshots | Hard to verify the end-to-end story quickly | **High** | Evidence-first README, architecture diagram, screenshots, run instructions, limitations |
| **Performance** | No measurements reported | Scalability claims would be speculative | **Medium** | Measure actual import duration and query/API latency; report dataset size |
| **Copied/tutorial appearance** | Sequential IDs, near-balanced categories, simple 3-stage workflow | May look like an assignment rather than a self-directed solution | **High** | Explain data origin, decisions, mistakes discovered, tests, trade-offs, and original improvements |

### Specific correctness issues to fix first

1. **Metric naming:** `Under Repair / total` is not “failure rate.”  
2. **Due-date categories:**  
   - `due_date < as_of_date` → **overdue**  
   - `as_of_date <= due_date <= as_of_date + 30 days` → **due within 30 days**  
   - `due_date > as_of_date + 30 days` → **later**  
   Decide separately how decommissioned assets are treated.
3. **Time handling:** Calculate with calendar dates, not a mix of SQL `GETDATE()` timestamps and Pandas `datetime.now()`. Document inclusive boundaries.
4. **Asset age units:** SQL comment says years; notebook calculates days.
5. **Stale exported columns:** `DaysUntilDue = -192` is an old snapshot, not a permanent attribute of the asset.
6. **SQL import:** `FROM Sheet1$` depends on a manually prepared staging object and is not a complete reproducible load procedure.
7. **As of March 2026,** the supplied April 2025 due date is historical. A “next 30 days” view should truthfully show zero upcoming records for this dataset—not re-label old records as future work.

---

# 3. Engineering-manager assessment

**Would I believe the candidate understands the system?** I would need to ask how data gets from SQL Server into Tableau. The reported answer is: **it does not**. Tableau reportedly uses the Excel export.

**Can they defend the analytics?** Not yet. “Why is `Under Repair` a failure?” and “Why are all 10,000 devices due on the same day?” are immediate interview questions.

**Can they explain failure scenarios?** There is no reported behavior for an invalid date, duplicate asset, missing staging sheet, changed Excel column, or rerun after a partial load.

**Can they explain deployment?** Not as a working online system today.

**What would impress me instead:** “I found that my first version mislabeled repair prevalence as failure rate, used stale date calculations, and documented a database-to-dashboard connection that did not exist. I fixed the definitions, built reproducible ingestion and tests, and made the displayed recommendations traceable.” That is a credible engineering story.

---

# 4. Industry research: what transfers, and what does not

Treat these as **research directions and relevant industry analogies**, not freshly verified product specifications. In the final README, cite the precise pages you actually consult.

| Industry example | Broad problem addressed | Data/workflow lesson for this project | Do **not** claim |
|---|---|---|---|
| **ServiceNow IT Asset Management** | Asset lifecycle visibility and operational workflows | Track identity, status, ownership, changes, and actions—not only charts | That our demo equals enterprise ITAM |
| **Microsoft Intune / Endpoint analytics** | Managed-device visibility and device-experience signals | Richer device signals can support better prioritization, if available and permitted | That our Excel data contains endpoint telemetry |
| **IBM Maximo** | Asset maintenance and work management | Maintenance history should connect an asset to actions and outcomes | That laptop inventory is the same as industrial predictive maintenance |
| **Data-quality/analytics-engineering practice** | Reliable reporting from changing source data | Version definitions, test transformations, log loads, expose freshness | That having a notebook alone constitutes production ETL |

**Relevant operational KPIs, conditional on data availability:**

- Active asset count.
- Current share under repair.
- Overdue scheduled-service count.
- Upcoming scheduled-service count.
- Maintenance events per asset/type over a defined period—**requires event history**.
- Time from reported issue to resolution—**requires start/end timestamps**.
- Maintenance cost—**requires real cost data**.
- Data freshness and rejection rate—**can be measured once ingestion exists**.

Do not put a KPI on the dashboard because industry teams use it. Put it there only when **the source fields and definitions support it**.

---

# 5. The real problem and the redesigned project

## Recommended working name

# **AssetOps — IT Asset Service Planning**

**One-line description:**  
A database-backed application that validates IT asset data, tracks service schedules and maintenance history, and helps IT operations prioritize reviews with explainable evidence.

I recommend **removing “Forecasting” for now**. You can revisit that word if you acquire genuine longitudinal outcomes and evaluate a forecasting approach.

## Problem statement

An IT operations team needs to know:

> **Which assets are overdue, due soon, under repair, or missing trustworthy information—and what action should be taken first?**

A schedule is only useful when it is current, consistent, and connected to an actual workflow. The current file has a severe quality/realism problem: every asset shares the same service dates. The upgraded system should **surface that limitation**, not hide it.

## Target user and decision

**User:** IT asset or service-desk lead.  
**Decision:** Which assets should be checked, serviced, or investigated this week, and which records need correction before planning can be trusted?

### The one differentiator

## **Explainable service-priority queue with data-quality awareness**

For each asset, show:

- Due status: overdue, upcoming, later, unknown.
- Current operational status.
- Maintenance-history signals **if event records exist**.
- Priority reason, for example: “overdue by 12 days and currently under repair.”
- Data-quality warning, for example: “service date may be stale” or “missing history.”
- Suggested human review action.

**Do not call this an AI failure prediction.** Initially it is a transparent rules-based decision aid.

---

# 6. Data strategy: do not fake realism

This is the key design decision. You have two honest paths.

## Path A — Best immediate engineering project

Use the **original 10,000-row file as a legacy import** and showcase:

- Discovery of the constant-date anomaly.
- Data-quality checks.
- Correct treatment of historical schedules.
- A dashboard that clearly reports **no genuinely upcoming dates in the original file** as of a current date.
- An actionable **data-remediation queue**: records with questionable schedule information need review.

**Strength:** Extremely honest and demonstrates engineering judgment.  
**Limitation:** Weak showcase for maintenance prioritization because the source has almost no useful schedule variation.

## Path B — Better full demo, with strict labeling

Keep Path A, and add a separately labeled **synthetic operational scenario dataset** with:

- Varied acquisition and due dates.
- Multiple maintenance events per asset over time.
- Consistent event types and status transitions.
- Some missing, duplicate, and invalid records to exercise quality checks.
- A reproducible generator with a fixed random seed and documented rules.

**Strength:** Allows a meaningful demonstration of schema, ETL, SQL, API, and dashboard interactions.  
**Limitation:** Insights describe the **simulated scenario**, not a real company. No claimed cost savings, predictive accuracy, or real-world failure behavior.

**My recommendation:** Do **both**, distinctly:

```text
Original supplied dataset → legacy-data audit and import
Clearly labeled generated scenario → application demo and engineering tests
```

Never quietly “fix” the original by randomizing its dates and then present it as authentic historical data. If you later find a suitable public event-history dataset, document its source/license and assess whether it is truly relevant before replacing the scenario data.

---

# 7. Target architecture

```text
Original Excel / labeled scenario files
                 ↓
Python ingestion command
                 ↓
Schema checks + business-rule validation
          ↙                  ↘
Accepted records       Rejected records + reasons
          ↓
PostgreSQL relational tables + ingestion-run log
          ↓
SQL KPI queries / views + tested priority rules
          ↓
FastAPI read API
          ↓
Web dashboard
          ↓
Overdue queue / upcoming queue / data-quality review queue
          ↓
Human action
```

**Why these technologies?**

- **Python:** Existing project uses it; suitable for Excel import, validation, rules, and tests.
- **PostgreSQL:** One accessible relational database for keys, constraints, joins, indexes, and API queries. This is a **migration from the existing SQL Server script**, not a claim PostgreSQL is inherently better. Keep the original SQL file as `legacy/` documentation if useful.
- **FastAPI:** Demonstrates tested backend contracts and connects database logic to an application.
- **Dashboard:** Makes the decision workflow visible. Choose **one** main demo UI. A lightweight web UI may be easier to deploy end-to-end than Tableau; retain Tableau as legacy evidence rather than maintaining two supposedly live dashboards.
- **Docker Compose:** Reproducible local application plus database.
- **GitHub Actions:** Run tests and checks on changes.
- **No Kafka, Spark, Kubernetes, microservices, or model merely for résumé keywords.**

---

# 8. Database design

Build only tables backed by fields you truly have or intentionally generate in the labeled scenario.

| Table | Key fields | Why it exists |
|---|---|---|
| `assets` | `asset_id` PK, type, purchase date, location, current status | Single canonical asset identity |
| `service_schedules` | schedule ID PK, `asset_id` FK, due date, schedule status, source | Separates scheduled work from permanent asset attributes; supports changes/history |
| `maintenance_events` | event ID PK, `asset_id` FK, event date, event type, outcome | Supports actual historical questions; **scenario/public event data only**, not fabricated from the original snapshot |
| `ingestion_runs` | run ID PK, source, start/end time, accepted/rejected counts, state | Trace freshness, failures, and reproducibility |
| `rejected_records` | reject ID, run ID FK, source row reference, reason | Makes quality failures inspectable |

**Constraints:** Unique asset IDs; required keys and dates; foreign keys; valid status values; defensible date relationships. Whether a service date may precede purchase should be rejected or flagged according to a documented rule.

**Indexes, initially:** Asset FK plus event date for history lookups; due date for schedule queues. Measure plans using real queries before creating more.

**Avoid storing `DaysUntilDue` as a lasting asset field.** Derive it from the due date and an explicit `as_of_date`. Keep `as_of_date` in API requests/reports for reproducibility.

**Useful SQL views/queries:**

1. Current inventory by type and location, excluding decommissioned assets when appropriate.
2. Overdue vs. due-within-30-days counts, with explicit boundaries.
3. Latest event per asset using `ROW_NUMBER()`—only for data containing events.
4. Repeated maintenance events per asset in a time window.
5. Data-quality rejection counts by source and reason.
6. Priority worklist that joins assets, schedules, and available event history.

Use `JOIN`, `GROUP BY`, `CASE`, CTEs, and window functions because those questions require them—not to display SQL tricks.

---

# 9. Pipeline and analytics contracts

## Ingestion workflow

```text
Input file
→ check expected columns/types
→ normalize strings and parse dates
→ validate record-level rules
→ detect duplicates
→ write accepted and rejected outcomes
→ upsert/load safely in a transaction
→ record run status and counts
```

A rerun of the same source should not silently duplicate assets or events. Document whether it **updates a current record**, **keeps history**, or **rejects conflicting input**.

## Testable KPI definitions

| Metric | Definition | Decision supported |
|---|---|---|
| **Active assets** | Assets not decommissioned as of the report date | Size of managed fleet |
| **Currently under repair** | Assets with current status `Under Repair` | Current workload—not failure rate |
| **Overdue service** | Eligible assets with due date before `as_of_date` | Backlog requiring review |
| **Due in 30 days** | Eligible assets due from `as_of_date` through `as_of_date + 30 days`, inclusive | Near-term planning |
| **Unusable schedule records** | Missing/invalid/implausible dates by documented rule | Data remediation |
| **Recent maintenance-event count** | Events in specified period, **only when event data exists** | Repeated-work investigation |

For the original dataset, a dashboard headline should say something like:

> “Source data contains an identical historical due date for all 10,000 assets; upcoming-service insights from this source are not reliable.”

That is more impressive than a misleading “10,000 at-risk assets” card.

**Forecasting gate:** Add prediction only if you obtain timestamped historical features, a clearly defined future outcome, a time-based evaluation split, and a meaningful baseline. Otherwise, leave it out.

---

# 10. Dashboard: a decision story

| Section | Question | Output/action |
|---|---|---|
| **Overview** | What needs attention now? | Eligible asset count, overdue count, due-soon count, current repair count, last refresh |
| **Trust indicator** | Can I use this data? | Source label, constant-date warning, rejected-row counts, freshness |
| **Trend** | Is the workload changing? | Event trend **only when event history exists**; no fake trend from a single snapshot |
| **Segments** | Where is work concentrated? | Type/location breakdown, with denominators |
| **Priority queue** | What should I review first? | Asset, due state, status, explanation, suggested next step |
| **Asset detail** | Why was this asset flagged? | Source fields, schedule, event history if available, quality warnings |
| **Data-quality queue** | Which records need correction? | Invalid/duplicate/implausible records and reasons |

Useful filters: type, location, due state, source dataset. Include search by asset ID. Don’t add a decorative city map if it contributes nothing to the maintenance decision.

---

# 11. Backend and API

Proposed minimal endpoints:

- `GET /health` — app/database health, without exposing secrets.
- `GET /metrics?as_of_date=...&source=...` — defined KPI summary.
- `GET /assets?...` — paginated/filterable assets.
- `GET /assets/{asset_id}` — detail and available history.
- `GET /priorities?as_of_date=...` — explainable worklist.
- `GET /data-quality/runs` — freshness and import results.

Start **read-only**. Add write endpoints only if you actually build an authenticated workflow that records actions.

Use typed validation, parameterized DB queries, bounded pagination, consistent error responses, and tests. A small, well-designed API is stronger than numerous unused endpoints.

---

# 12. Testing, monitoring, security, performance

## Tests to implement

| Test layer | Important cases |
|---|---|
| Data validation | Missing ID, duplicate ID, invalid date, unknown status, constant-date anomaly |
| Transformations | Same input and `as_of_date` yield same output; unit tests for age and day boundaries |
| SQL/business logic | Overdue vs. due-today vs. due-on-day-30 vs. day-31; decommissioned eligibility |
| Pipeline integration | Rerun same file; partially invalid file; failed transaction |
| API | Filtering, pagination, invalid date input, unknown asset, database failure behavior |
| Dashboard data | Displayed KPI agrees with API/SQL fixture |
| Scenario generator | Fixed seed reproduces same scenario; generated events obey constraints |

**Monitoring appropriate to a portfolio project:** Log ingestion status/counts and API errors; show last successful import; report simple health and measured response times. Avoid inventing production SLOs.

**Security:** `.env.example`, no actual credentials in Git; database not publicly reachable; parameterized queries; input validation. If a public demo uses only generated data and read-only endpoints, say so. Check the repository for any committed credentials before deployment.

**Performance proof:** Measure with actual hardware, dataset size, commands, and query/API timings. “Scalable” without measurements is not proof.

---

# 13. Deployment plan — analytics deployed like software

## Recommended sequence

### Stage 1: Reproducible local application

```text
docker compose up
→ start PostgreSQL
→ apply schema/migrations
→ load labeled sample/scenario data
→ start API and dashboard
→ run a documented smoke test
```

A reviewer should not need SSMS, manual Excel imports, a paid Tableau license, and several undocumented steps.

### Stage 2: CI

On each pull request/push:

1. Install dependencies.
2. Lint/check formatting.
3. Run unit tests.
4. Start a test database or container.
5. Run migration and integration tests.
6. Optionally build images.

### Stage 3: Public demo, if feasible

Deploy **one backend, one dashboard, one persistent PostgreSQL database** using a budget-appropriate hosting arrangement. Prefer generated demo data; do not expose unlicensed or confidential data. Record the actual host, costs/free-tier limitations, sleep behavior, and reset strategy.

If reliable public hosting is unaffordable, deliver **deployment-ready Docker Compose plus a short recorded demo**. Say **“deployment-ready,” not “deployed.”**

### Release verification

- Dashboard loads.
- API docs and read endpoints respond.
- Database survives app restart.
- Health endpoint works.
- Source and freshness are visible.
- No secret appears in the repository or browser.
- CI passes for the deployed commit.

---

# 14. Proof-of-work matrix — the most important part

| What you want to claim | Required verifiable artifact | What **not** to say |
|---|---|---|
| “Found and fixed misleading analytics” | Before/after metric definitions; tests demonstrating overdue vs. upcoming | “Predicted failures” |
| “Built a reliable pipeline” | CLI command, validation rules, sample rejects, run logs, rerun test | “Production-scale ETL” |
| “Designed a relational database” | Schema/migration, ER diagram, FK/constraint tests | “Enterprise data warehouse” |
| “Wrote meaningful SQL” | Versioned queries, business question, fixture output, explanation | “Advanced SQL” based on syntax alone |
| “Built decision support” | Screenshot and walkthrough from issue → asset → reason → action | “Reduced downtime” without evidence |
| “Built an API” | OpenAPI page, example responses, integration tests | “Microservices architecture” |
| “Deployed it” | Working URL and deployment config; note hosting limitations | “Live” if the link fails |
| “Improved performance” | Reproducible benchmark and measured before/after values | Invented percentages |
| “Developed forecasting” | Historical labels, chronological evaluation, baseline, metrics | Calling due-date arithmetic forecasting |
| “Used realistic data” | Source/license or explicit scenario-generator rules | Presenting generated rows as company records |

**Suggested GitHub evidence order:** README hero → honest data notice → architecture image → screenshot → demo link → quick start → validation example → SQL/schema → tests/CI badge → actual findings → limitations.

---

# 15. Before vs. after

| Dimension | Current reported project | Target project |
|---|---|---|
| Problem | Broad “predictive maintenance” claim | Specific service-planning and data-trust decision |
| Data | One snapshot with constant service dates | Original audited separately; clearly labeled operational scenario or sourced history |
| Database | Flat SQL Server table, manual staging | PostgreSQL schema, relationships, migrations |
| SQL | Counts and simple date filter | Tested operational queries with joins and date logic |
| Pipeline | Notebook and Excel export | Repeatable validated import with rejection/run records |
| Analytics | Repair prevalence labeled failure; stale due KPI | Defined KPIs, explicit `as_of_date`, honest caveats |
| Dashboard | Descriptive Tableau charts from Excel | Source-aware decision workflow and explained worklist |
| Backend | None | Small tested read API |
| Testing | None reported | Boundary, integration, API, and quality tests |
| Deployment | Local notebook/workbook | Reproducible containers; hosted demo if feasible |
| Monitoring | None reported | Import status, freshness, health, errors |
| Proof | Files and claims | Reproducible setup, screenshots, tests, demo, measurements |

---

# 16. Suggested repository structure

Preserve the existing work rather than obscuring its evolution:

```text
assetops/
├── legacy/                    # Original notebook, SQL, Tableau and report
├── data/
│   ├── original/              # Only if redistribution is permitted
│   └── scenario/              # Clearly labeled generated demo data
├── src/assetops/
│   ├── ingestion/
│   ├── validation/
│   ├── domain/                # KPI and priority definitions
│   ├── database/
│   └── api/
├── dashboard/
├── sql/
├── migrations/
├── tests/
├── docs/
│   ├── architecture.md
│   ├── data-provenance.md
│   ├── metrics.md
│   ├── database.md
│   ├── deployment.md
│   └── screenshots/
├── .github/workflows/
├── .env.example
├── docker-compose.yml
└── README.md
```

Do not create empty folders to make the tree look impressive. Add them when working code or documentation exists.

## README story

1. What decision does AssetOps support?
2. Why the original data could not support the original forecasting claims.
3. Which dataset powers each demo view.
4. Architecture and data flow.
5. Metrics and priority rules.
6. Example quality failure and its handling.
7. Screenshot and demo.
8. Local setup.
9. Tests and measured results.
10. Limitations and next steps.

---

# 17. Implementation roadmap with completion gates

| Milestone | Build | **Done when** |
|---|---|---|
| **1. Establish truth** | Confirm Antigravity findings; document source, columns, definitions and limitations | README stops claiming ML, live SQL→Tableau, or measured impact without proof |
| **2. Correct legacy analytics** | Explicit `as_of_date`; separate overdue/upcoming; rename repair metric | Boundary tests pass; legacy report gives honest results |
| **3. Choose demo data path** | Preserve original; build documented scenario generator **or** source suitable licensed history | Anyone can identify which records are original vs. generated |
| **4. Database** | PostgreSQL schema and migrations | Constraints and import fixtures pass |
| **5. Pipeline** | CLI ingestion, validation, reject records, run log, safe reruns | Two imports do not create unintended duplicates |
| **6. SQL analytics** | KPI and worklist queries | Outputs match documented fixture expectations |
| **7. Backend** | Minimal FastAPI read endpoints | OpenAPI, error cases, and tests work |
| **8. Dashboard** | Overview, quality signal, queue, asset detail | User can explain one recommended action |
| **9. Differentiator** | Explainable priority rules | Every priority has reasons; rule boundaries are tested |
| **10. Operations/deployment** | Docker, CI, secrets handling, monitoring; optional host | Another person can run it; deployed claim has a working link |
| **11. Documentation/proof** | Architecture, demo, findings, benchmark, limitations | Every major README claim links to evidence |
| **12. Career packaging** | Resume, portfolio, LinkedIn, interview practice | You can defend the architecture and dataset honestly |

---

# 18. Resume and portfolio positioning

These are **future templates**, not current accomplishments:

- **Built** a Python ingestion pipeline for IT asset records with schema validation, duplicate handling, rejection reporting, and reproducible PostgreSQL loads.
- **Designed** a relational asset, schedule, and maintenance-event model and wrote tested SQL queries powering overdue, upcoming-service, and data-quality worklists.
- **Developed** a FastAPI service and interactive dashboard that explain asset priorities and expose source freshness and data-quality warnings.
- **Containerized and tested** the application with Docker and CI; documented measured import/query performance on **[actual dataset size and measured result]**.

### Portfolio case-study hero

> **AssetOps:** Turning an unreliable IT asset spreadsheet into a transparent service-planning application.

Then show: **the flawed assumption → data investigation → corrected metric → architecture → recommendation workflow → test/deployment evidence → limitations**.

---

# 19. Interview explanation

### 30 seconds

“My first version was an IT asset dashboard, but during an audit I found that every asset had the same service dates and I had mislabeled schedule filtering as forecasting. I redesigned it as a service-planning application: validated imports, a relational database, tested KPI rules, an API, and a dashboard that explains which records or assets need review.”

### 1 minute

Add: what the original file contains, why you retained it as a data-quality case, how any generated scenario data is labeled, and one example of the user decision.

### 3 minutes

Walk one record through ingestion → validation → database → SQL priority rule → API → dashboard. Explain one invalid-data example, the date-boundary test, and one trade-off such as choosing transparent rules instead of an unsupported ML model.

### 10-minute deep dive

1. Problem and original dataset limitation.
2. Architecture and why each component exists.
3. Asset/schedule/event schema and integrity rules.
4. Idempotent ingestion and rejected records.
5. SQL KPI definitions and date boundaries.
6. Explainable priority method and its limitations.
7. API and dashboard user journey.
8. Tests and a failure scenario.
9. Deployment, secrets, monitoring, measured performance.
10. What you would change with genuine longitudinal data or 100× scale.

---

# 20. Engineering-manager interview question bank

| Topic / question | What I’m testing; strong answer should cover | Common mistake |
|---|---|---|
| **Data:** Where did the 10,000 rows come from? | Provenance, permitted use, original vs. generated separation | Calling them real company data without evidence |
| **Analytics:** Why isn’t `Under Repair / total` a failure rate? | Snapshot prevalence vs. event incidence | Repeating the old KPI name |
| **SQL:** How do you calculate overdue and next-30-day work? | Explicit `as_of_date`, inclusion boundaries, eligibility | Using one `< 30` condition for both |
| **Database:** Why separate assets, schedules, and events? | Entity meaning, one-to-many history, keys, constraints | Creating tables only to show normalization |
| **Python:** What happens with invalid dates or duplicate IDs? | Validation result, reject reason, safe rerun | Silent coercion/drop |
| **Backend:** Why is there an API? | Shared, tested business logic and UI contract | “FastAPI looks good on a resume” |
| **API:** How do filters and pagination work? | Validation, limits, predictable responses | Returning 10,000+ rows without limits |
| **Architecture:** What is the source of truth? | Files as input; database as application store; clearly defined transformations | Claiming Tableau reads DB when it reads Excel |
| **Dashboard:** What action follows a red flag? | Drill-down, reason, data-quality warning, human review | “The chart looks useful” |
| **Deployment:** What happens on restart? | Persistent DB, migrations, startup, demo data policy | Assuming container filesystem is persistent |
| **Testing:** Which bug would your tests have caught? | The overdue/due-soon boundary and stale-date logic | Only testing that the app starts |
| **Scalability:** What would you change at 100× volume? | Measure first; indexing, pagination, batching, precomputation if needed | Immediately saying Kafka/Spark |
| **Security:** How are credentials and queries protected? | Environment variables, restricted DB, parameters, read-only demo | Committed `.env` or string-built SQL |
| **Business logic:** Why this priority rule? | User decision, transparent reasons, limitations, validation | Presenting arbitrary weights as learned risk |

---

# 21. Industry mapping and future scale

| Your project capability | Related industry engineering concept | Skill demonstrated |
|---|---|---|
| Validated Excel import | Source ingestion and data contracts | Reliable data handling |
| Rejected-row reporting | Data-quality operations | Failure visibility |
| Relational schema | Operational/analytical data modeling | SQL and integrity |
| Defined KPI queries | Semantic consistency | Analytical reasoning |
| Explainable queue | Decision-support workflow | Product thinking |
| API | Service boundary | Backend engineering |
| CI, tests, containers | Release discipline | Software fundamentals |
| Freshness/health display | Basic observability | Operational thinking |

---

# 22. Definition of done

This project is complete only when:

- [ ] Its name and claims match what it actually does.
- [ ] Original-data provenance and limitations are documented.
- [ ] Generated/demo data is unmistakably labeled.
- [ ] Overdue and upcoming rules are consistent and tested.
- [ ] The pipeline handles bad input and safe reruns.
- [ ] The database has justified relationships and constraints.
- [ ] SQL answers real questions.
- [ ] The dashboard ends in an understandable human action.
- [ ] The API and dashboard use the same defined metrics.
- [ ] Tests and CI pass.
- [ ] Secrets are protected.
- [ ] Another person can run it from documentation.
- [ ] Any “live” deployment really works.
- [ ] Screenshots, measured results, and limitations are published.
- [ ] You can explain every important design choice in an interview.

## Recommended next step

First complete **Milestone 1 and 2**: verify the supplied audit, correct the project’s public claims, define the `as_of_date` and KPI rules, and decide whether to add a transparently generated scenario dataset.
