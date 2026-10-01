# Data Provenance & Feasibility Audit: Backblaze Drive Stats

**Project:** IT Hardware Reliability Analytics  
**Primary Dataset:** Backblaze Hard Drive Test Data (2024 Observation Window)  
**Status:** Verified & Ingested  

---

## 1. Dataset Origin & Description
Backblaze publishes quarterly operational snapshots of enterprise hard drives operating across its cloud infrastructure data centers. Each record represents a single drive operational day (**drive-day**), recording operational status, failure events, and self-monitoring metrics (S.M.A.R.T. raw values).

* **Source Publisher:** Backblaze Data Center Drive Stats ([Backblaze Hard Drive Data](https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data))
* **Primary Observation Grain:** `1 row = 1 drive-day`
* **Dataset Scope:** 2024 Q1 (Contiguous 90-day observation window)
* **Sample Size:** 100,000 drive-day records across major enterprise drive models (Seagate, Western Digital, Toshiba, HGST).

---

## 2. Core Schema & Field Mapping

| Field Name | Type | Description | Analytical Purpose |
| :--- | :--- | :--- | :--- |
| `date` | `DATE` | Observation timestamp (YYYY-MM-DD) | Temporal grouping & daily exposure tracking |
| `serial_number` | `VARCHAR` | Unique drive identifier | Tracking individual asset lifecycle |
| `model` | `VARCHAR` | Drive model designation | Reliability benchmarking across drive models |
| `capacity_bytes` | `BIGINT` | Total drive storage capacity | Capacity-stratified failure analysis |
| `failure` | `INTEGER` | Binary indicator (`0` = Healthy, `1` = Operational Failure) | Failure event counting |
| `smart_5_raw` | `INTEGER` | Reallocated Sectors Count | Critical hardware degradation indicator |
| `smart_9_raw` | `INTEGER` | Power-On Hours | Asset age & usage exposure |
| `smart_187_raw` | `INTEGER` | Reported Uncorrectable Errors | Read/write reliability signal |
| `smart_197_raw` | `INTEGER` | Current Pending Sector Count | Impending failure precursor |
| `smart_198_raw` | `INTEGER` | Offline Uncorrectable Sector Count | Sector-level corruption signal |

---

## 3. Data Integrity & Exclusion Rules

1. **Exposure Threshold:** Drive models with total exposure of fewer than **1,000 drive-days** are excluded from model-level failure rate comparisons to eliminate small-sample noise.
2. **Missing S.M.A.R.T. Attributes:** Drives reporting null S.M.A.R.T. values are included in exposure counts but excluded from S.M.A.R.T. degradation correlation models.
3. **Population Isolation:** Backblaze drive observations are strictly isolated from the legacy IT Asset inventory dataset. No fictional merging of datasets is performed.

---

## 4. Verification Checkpoints
- [x] Contiguous date range verified (2024-01-01 to 2024-03-31)
- [x] Zero duplicate drive-days for any `(serial_number, date)` composite key
- [x] Failure event distribution validated against published Backblaze benchmark standards (~1.2% - 1.8% AFR)
