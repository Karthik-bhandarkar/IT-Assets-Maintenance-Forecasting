# AssetOps — Complete Implementation Specification

**Hand this single file to Antigravity (or follow it manually). Every milestone contains
exact commands, exact file contents, and exact pass/fail checks.**

- **Target repo name:** `AssetOps` (rename of `IT-Assets-Maintenance-Forecasting`)
- **Project title:** *AssetOps — IT Asset Service Planning*
- **One-line description:** A database-backed application that validates IT asset records,
  tracks service schedules, and gives IT operations an explainable queue of assets and
  data-quality issues to review.
- **Spec version:** 1.0
- **Stack:** Python 3.11 · PostgreSQL 16 · FastAPI · Streamlit + Plotly · Docker Compose · GitHub Actions
- **Explicitly NOT in scope:** machine learning, failure prediction, forecasting claims,
  Kubernetes, Kafka, Spark, microservices, LLMs.

---

## 0. How to use this document

### 0.1 Note on the requested model

The instruction *"use GPT-6 Astra / Fable"* is passed through to the implementing agent in
§0.2. An agent must **never claim** which model is active unless its tooling exposes that
verifiably. Use the highest-capability model your IDE offers for repository-wide
engineering work. Model choice does not change a single requirement in this document.

### 0.2 Prompt to paste into Antigravity at the start of EVERY session

```text
You are working as a careful senior software/data engineer on the AssetOps repository.
Use the highest-capability reasoning/coding model your environment offers for
architecture, code changes, debugging and review. Do not claim which model is active
unless your tooling verifiably reports it.

Your specification is the file ASSETOPS_BUILD_PLAN.md. Read the whole file before acting.

RULES:
1. Implement ONE milestone at a time, in order. Stop after each milestone and wait for
   human approval. Never mark your own milestone approved.
2. Re-inspect the repository before editing. If the repo contradicts the spec, STOP and
   report the contradiction instead of guessing.
3. Never invent: dataset provenance, business outcomes, model performance, deployment
   status, benchmark numbers, or test results. Only report commands you actually ran and
   output you actually saw.
4. Never use the words forecast, predict, predictive, risk score, ML, or AI to describe
   AssetOps behaviour. The priority queue is RULE-BASED and must be described as such.
5. Do not delete or overwrite any existing repository file. Move legacy files into
   legacy/ only when the milestone says to, using `git mv`.
6. Never commit secrets, .env files, database volumes, or large binaries.
7. Report using the DELIVERY FORMAT in §0.3 of the spec.

Begin with MILESTONE 0. Do not touch any file during Milestone 0.
```

### 0.3 Delivery format the agent must use after every milestone

```text
MILESTONE:
WHAT I INSPECTED:
FINDINGS WITH FILE EVIDENCE:      (path + line/cell reference + actual value)
PROPOSED/IMPLEMENTED CHANGES:
FILES CREATED:
FILES MODIFIED:
FILES MOVED OR DELETED:
COMMANDS ACTUALLY RUN:            (verbatim, with exit codes)
TEST RESULTS:                     (verbatim pytest tail, not a summary)
SCREENSHOTS OR OUTPUT ARTIFACTS:
RISKS / LIMITATIONS:
WHAT I DID NOT VERIFY:
QUESTIONS REQUIRING APPROVAL:
```

"Done, everything works" is not an acceptable report.

### 0.4 Stop conditions (agent must halt and ask)

- Redistribution rights of the original spreadsheet are unclear.
- Its own inspection contradicts the audit in §2.
- A schema needs a field the data does not contain.
- It wants to add a major technology, delete a file, or rename a public claim.
- A test fails and it cannot explain the cause.
- Deployment would need paid services or exposure of data with uncertain rights.

### 0.5 Relationship to earlier work in this workspace

An earlier experiment (`/home/user/assetpulse`, an ML "predictive maintenance" build)
**is superseded and must NOT be merged into AssetOps.** It relies on a simulated failure
history and produces model metrics; this specification forbids predictive framing.
Keep it outside the repo, or keep it as a separate personal repo clearly labelled as a
modelling exercise on synthetic data. Nothing from it may be cited in AssetOps docs.

---

## 1. Definition of done (whole project)

The project is complete when a stranger can do all of this without asking you anything:

1. `git clone` → `cp .env.example .env` → `docker compose up -d` → three healthy containers.
2. `docker compose exec api python -m scripts.migrate` → schema created, printed summary.
3. `docker compose exec api assetops ingest --source original --file legacy/01_IT_ASSESMENT(raw data).xlsx`
   → run recorded, accepted/rejected counts printed, constant-date warning raised.
4. `docker compose exec api assetops generate-scenario --seed 42 --output data/scenario`
   then `assetops ingest --source scenario --directory data/scenario` → events loaded.
5. `http://localhost:8000/docs` → interactive OpenAPI, every endpoint returns 200 on a
   happy path and a typed error otherwise.
6. `http://localhost:8501` → dashboard with dataset-mode banner, `as_of_date` control,
   KPI cards, filters, priority queue with a plain-English **Reason** column, asset
   drill-down, and a data-quality page.
7. `pytest` → all tests pass, including the boundary tests in §12.
8. GitHub Actions badge green.
9. Every claim in `README.md` maps to a row of the claim-to-proof matrix (§16).

---

## 2. Facts about the current repository (must be re-verified in Milestone 0)

| # | Reported finding | Consequence if confirmed |
|---|---|---|
| F1 | 10,000 assets, 7 columns: AssetID, AssetType, PurchaseDate, LastServiceDate, NextServiceDue, Status, Location | Snapshot, not event history |
| F2 | `LastServiceDate` has 1 distinct value (2025-04-29); `NextServiceDue` has 1 distinct value (2025-04-30) | Schedule cannot rank assets; must be surfaced as a dataset-level warning |
| F3 | `DaysUntilDue < 30` filter includes negative values | "Due soon" silently mixes overdue in |
| F4 | `Under Repair / total` is labelled a failure rate | Wrong name: it is current repair prevalence |
| F5 | Tableau `.twbx` reads an Excel extract | Must not be described as live SQL-backed |
| F6 | No model, no evaluation, no tests, no API, no CI | Cannot claim forecasting or engineering maturity |
| F7 | Dataset origin undocumented | Cannot claim real organisational data |

**Status values observed:** Working / Under Repair / Decommissioned.
**Locations observed:** Hyderabad / Bangalore / Pune.
**Asset types observed:** Laptop / Printer / Router / Monitor / Keyboard.

---

## 3. Prerequisites (do this before Milestone 0)

| Tool | Minimum | Verify with |
|---|---|---|
| Git | 2.30 | `git --version` |
| Python | 3.11 | `python --version` |
| Docker Desktop / Engine | 24 | `docker --version` |
| Docker Compose plugin | v2 | `docker compose version` |
| Disk | 3 GB free | — |

Windows users: run all commands in **PowerShell** or **WSL2 Ubuntu**; WSL2 is strongly
preferred and is assumed by the shell snippets in this document.

---

## 4. Final repository layout (target)

```text
AssetOps/
├── README.md
├── ASSETOPS_BUILD_PLAN.md          # this file
├── pyproject.toml
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.dashboard
│
├── legacy/
│   ├── README.md
│   ├── 01_IT_ASSESMENT(raw data).xlsx
│   ├── 02_IT Asset Maintenance Forecasting.ipynb
│   ├── 03_IT Asset Maintenance Forecasting(for sql).xlsx
│   ├── 04_SQLQuery5.sql
│   ├── 05_IT Asset.twbx
│   └── Project Documentation_ IT Asset Maintenance Forecasting.pdf
│
├── data/
│   ├── README.md
│   ├── scenario/          # generated; .gitignored except a tiny committed sample
│   └── samples/           # small hand-written CSVs used by tests
│
├── migrations/
│   ├── 0001_initial_schema.sql
│   └── 0002_indexes.sql
│
├── scripts/
│   ├── migrate.py
│   └── smoke_test.py
│
├── sql/
│   ├── README.md
│   └── analytical_queries.sql
│
├── src/assetops/
│   ├── __init__.py
│   ├── config.py
│   ├── cli.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── due_status.py
│   │   ├── priority.py
│   │   └── metrics.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── excel_reader.py
│   │   ├── validation.py
│   │   └── loader.py
│   ├── scenario/
│   │   ├── __init__.py
│   │   └── generate.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── queries.py
│   └── api/
│       ├── __init__.py
│       ├── main.py
│       ├── schemas.py
│       ├── deps.py
│       └── routes/
│           ├── __init__.py
│           ├── health.py
│           ├── metrics.py
│           ├── assets.py
│           ├── priorities.py
│           └── data_quality.py
│
├── dashboard/
│   ├── app.py
│   ├── api_client.py
│   └── components/
│       ├── __init__.py
│       ├── kpi.py
│       └── banner.py
│
├── tests/
│   ├── conftest.py
│   ├── fixtures/
│   ├── test_due_status.py
│   ├── test_priority.py
│   ├── test_validation.py
│   ├── test_scenario.py
│   ├── test_excel_reader.py
│   ├── test_ingestion_db.py
│   ├── test_sql_metrics.py
│   └── test_api.py
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA-PROVENANCE.md
│   ├── DATA-QUALITY.md
│   ├── DATABASE.md
│   ├── METRICS.md
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── DECISIONS.md
│   └── screenshots/
│
└── .github/workflows/ci.yml
```

---

# MILESTONE 0 — Re-audit (NO FILE EDITS)

**Objective:** independently confirm or refute §2 before any code is written.

### 0.1 Commands to run

```bash
cd ~
git clone https://github.com/Swati-Devas/IT-Assets-Maintenance-Forecasting.git AssetOps
cd AssetOps
git log --oneline --stat | head -50
ls -la
python -m venv .venv && source .venv/bin/activate
pip install pandas openpyxl
```

### 0.2 Audit script (run it, paste the real output in the report)

Create this as a **temporary** file outside the repo, e.g. `/tmp/audit.py`:

```python
import pandas as pd, hashlib, pathlib, sys

RAW = pathlib.Path("01_IT_ASSESMENT(raw data).xlsx")
print("sha256:", hashlib.sha256(RAW.read_bytes()).hexdigest())
xl = pd.ExcelFile(RAW)
print("sheets:", xl.sheet_names)
df = xl.parse(xl.sheet_names[0])
print("shape:", df.shape)
print("columns:", list(df.columns))
print("dtypes:\n", df.dtypes)
print("nulls:\n", df.isna().sum())
print("duplicate AssetIDs:", int(df["AssetID"].duplicated().sum()))
for c in df.columns:
    u = df[c].nunique()
    print(f"{c:<18} distinct={u:<6} sample={df[c].dropna().unique()[:5]}")
for c in ["PurchaseDate", "LastServiceDate", "NextServiceDue"]:
    s = pd.to_datetime(df[c], errors="coerce")
    print(f"{c}: min={s.min()} max={s.max()} distinct={s.nunique()} nat={s.isna().sum()}")
print(df["Status"].value_counts(dropna=False))
print(df["Location"].value_counts(dropna=False))
print(df["AssetType"].value_counts(dropna=False))
# F3 check: does the notebook's due-soon filter admit overdue rows?
asof = pd.Timestamp("2025-04-01")
d = (pd.to_datetime(df["NextServiceDue"]) - asof).dt.days
print("rows with DaysUntilDue < 0 :", int((d < 0).sum()))
print("rows with DaysUntilDue < 30:", int((d < 30).sum()))
```

### 0.3 Also inspect by hand

```bash
jupyter nbconvert --to script "02_IT Asset Maintenance Forecasting.ipynb" --stdout | head -200
cat 04_SQLQuery5.sql
unzip -o "05_IT Asset.twbx" -d /tmp/twbx && ls -R /tmp/twbx | head -40
grep -o 'class=.[a-z-]*connection[^>]*' /tmp/twbx/*.twb | head -20   # shows the data source type
git log -p | grep -iE "password|secret|api[_-]?key|token" | head     # secret scan
```

### 0.4 Deliverables

A table with one row per finding F1–F7: **Confirmed / Refuted / Cannot determine**, each
with a file path and the literal observed value.

Plus answers to:
- Does the `.twb` XML show an Excel/CSV connection or a SQL Server connection? (evidence F5)
- Does the notebook contain any `sklearn`/`statsmodels`/`train_test_split` call? (evidence F6)
- Is there any statement of dataset origin/licence anywhere in the repo? (evidence F7)

### 0.5 GATE 0 — pass criteria

- [ ] Zero files changed (`git status` clean).
- [ ] Every finding F1–F7 has a verdict with literal evidence.
- [ ] SHA-256 of the raw workbook recorded (used later to prove the original was untouched).
- [ ] Secret scan run; result reported.
- [ ] Open questions listed (especially dataset provenance/licence).

**STOP. Wait for human approval.**

---

# MILESTONE 1 — Correct the project's claims

**Objective:** make the repository honest before making it bigger. No application code yet.

### 1.1 Steps

1. Create the branch: `git checkout -b m1-honest-claims`
2. Create `legacy/` and move the six original artefacts with `git mv` (preserves history):

```bash
mkdir -p legacy
git mv "01_IT_ASSESMENT(raw data).xlsx" legacy/
git mv "02_IT Asset Maintenance Forecasting.ipynb" legacy/
git mv "03_IT Asset Maintenance Forecasting(for sql).xlsx" legacy/
git mv "04_SQLQuery5.sql" legacy/
git mv "05_IT Asset.twbx" legacy/
git mv "Project Documentation_ IT Asset Maintenance Forecasting.pdf" legacy/
```

3. Write `legacy/README.md` — content template:

```markdown
# Legacy artefacts (v1: "IT Asset Maintenance Forecasting")

These files are the original project, preserved unmodified for provenance.
SHA-256 of the raw workbook at the time of archiving: <PASTE FROM MILESTONE 0>

| File | What it actually does |
|---|---|
| 01_IT_ASSESMENT(raw data).xlsx | 10,000-row asset snapshot, 7 columns |
| 02_...ipynb | pandas cleaning + descriptive charts. No model is trained. |
| 03_...(for sql).xlsx | the same rows with derived columns, used as a SQL import staging sheet |
| 04_SQLQuery5.sql | CREATE TABLE + a few SELECTs |
| 05_IT Asset.twbx | Tableau workbook. Its data source is an <Excel extract / SQL connection — state what Milestone 0 proved>. |

## Why v1 was renamed and rebuilt

1. The title claimed forecasting. No model, target variable or evaluation exists in v1.
2. `LastServiceDate` and `NextServiceDue` each contain a single distinct value across all
   10,000 rows, so the schedule cannot distinguish which asset to service first, and the
   KPI "assets due in the next 30 days" is not meaningful.
3. The "due soon" filter used `DaysUntilDue < 30`, which also admits overdue (negative)
   values, conflating two different operational states.
4. "Failure rate" was computed as `Under Repair / total assets`. That is current repair
   prevalence, not failure incidence over a period.

AssetOps (this repository) keeps the honest parts — the asset register, the SQL work and
the dashboard idea — and rebuilds them as a validated, tested, database-backed service
planning tool. It does not forecast anything.
```

4. Replace root `README.md` with the honest version (full template in §Appendix A).
   At Milestone 1 the README must contain a **"Status: under construction"** section
   listing which milestones are done. Do not describe unbuilt components in the present
   tense.
5. Create `docs/DECISIONS.md` with the first four decisions (ADR style, template in
   Appendix B): why the rename; why no ML; why PostgreSQL; why Streamlit over Tableau
   Public for the new dashboard (legacy Tableau retained).
6. Create `.gitignore`:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.ipynb_checkpoints/
.env
.env.*
!.env.example
data/scenario/*
!data/scenario/.gitkeep
pgdata/
*.log
.DS_Store
docs/screenshots/*.tmp
```

### 1.2 Global vocabulary rule (applies to every later milestone)

| Banned | Use instead |
|---|---|
| failure rate | currently under repair (share of active assets) |
| predict / forecast / risk score | rule-based priority, scheduled-service status |
| real-time | refreshed at `<last successful ingestion timestamp>` |
| live SQL dashboard (for the Tableau file) | legacy Tableau workbook, Excel-extract backed |
| reduced downtime by X% | *(do not claim; no outcome data exists)* |

Enforcement (add in Milestone 10 CI, but start honouring now):

```bash
! grep -rniE "\b(forecast|predict(ive|ion)?|failure rate|machine learning|\bML\b)\b" \
    README.md docs/ src/ dashboard/ --include="*.md" --include="*.py" \
  | grep -v "docs/DECISIONS.md" | grep -v "legacy/" | grep -v "does not"
```

### 1.3 GATE 1 — pass criteria

- [ ] `git status` shows only moves + new docs; **no original file byte-modified**
      (`sha256sum legacy/"01_IT_ASSESMENT(raw data).xlsx"` equals the Milestone 0 hash).
- [ ] README contains: real problem, what v1 did, why forecasting was removed, current
      status, and no future-tense claims written as present-tense facts.
- [ ] Vocabulary grep above returns nothing.
- [ ] `legacy/README.md` states the Tableau data-source type proved in Milestone 0.

**STOP. Wait for approval.**

---

# MILESTONE 2 — Contracts: metrics, dates, dataset modes, priority

**Objective:** freeze the definitions *before* any code depends on them. Documentation only.

### 2.1 `docs/METRICS.md` — write exactly these rules

```markdown
# Metric and rule contract  (v1.0 — changes require a version bump + test update)

## 1. Time basis
- All date logic uses an explicit `as_of_date` (a calendar date, no time component).
- Default `as_of_date` = current date in **Asia/Kolkata**, resolved once per API request.
- All dates are stored as SQL `DATE`. No timezone conversion is applied to stored dates.
- The dashboard always displays the `as_of_date` in use.

## 2. Eligibility
An asset is **eligible for service planning** when `current_status <> 'Decommissioned'`.
- `Working` and `Under Repair` are both eligible.
- Decommissioned assets are excluded from OVERDUE / DUE_WITHIN_30 / LATER counts and
  from the priority queue. They remain visible in the asset list with a filter.

## 3. Schedule resolution
An asset may have several rows in `service_schedules`. The **governing schedule** is the
row with the earliest `due_date` among rows with `schedule_status = 'open'`.
If no open row exists, the asset's due status is UNKNOWN.

## 4. Due status (mutually exclusive, exhaustive)
Let D = governing due_date, A = as_of_date.

| Category | Condition |
|---|---|
| UNKNOWN | no governing schedule, or D is NULL |
| OVERDUE | D < A |
| DUE_WITHIN_30 | A <= D <= A + 30 days  (both ends inclusive; day 0 and day 30 included) |
| LATER | D > A + 30 days |

Boundary decisions (frozen):
- D = A  -> DUE_WITHIN_30 (not overdue).
- D = A + 30 -> DUE_WITHIN_30.
- D = A + 31 -> LATER.
- D = A - 1 -> OVERDUE.
- "30 days" means 30 calendar days added to the date (month/leap-year safe).

`days_until_due = (D - A).days`; negative means overdue. It is COMPUTED, never stored.

## 5. KPI definitions
| KPI | Definition | Denominator |
|---|---|---|
| active_assets | count of assets where status <> 'Decommissioned' | — |
| currently_under_repair | count where status = 'Under Repair' | active_assets |
| overdue_scheduled_service | eligible assets with due status OVERDUE | active_assets |
| due_within_30_days | eligible assets with due status DUE_WITHIN_30 | active_assets |
| unknown_schedule | eligible assets with due status UNKNOWN | active_assets |
| maintenance_events_90d | count of rows in maintenance_events with event_date in (A-90, A] | — |
| data_freshness | finished_at of the most recent successful ingestion run for the active dataset mode | — |

`currently_under_repair` is NOT a failure rate and must never be labelled as one.
`maintenance_events_90d` is shown only for dataset modes that contain event rows.

## 6. Priority rules (rule-based, evaluated top-down, first match wins)
| Rank | Priority | Condition | Reason text shown to user |
|---|---|---|---|
| 1 | P1_DATA_REVIEW | eligible AND due status UNKNOWN | "No usable service schedule on record — this asset cannot be planned until the schedule is corrected." |
| 2 | P2_URGENT_OPERATIONAL | eligible AND OVERDUE AND status = 'Under Repair' | "Overdue by {n} days and currently under repair." |
| 3 | P3_OVERDUE | eligible AND OVERDUE | "Overdue by {n} days." |
| 4 | P4_DUE_SOON | eligible AND DUE_WITHIN_30 | "Due in {n} days." |
| 5 | P5_NO_ACTION | eligible AND LATER | "Next service due in {n} days — no action required now." |
| — | EXCLUDED | not eligible (Decommissioned) | "Decommissioned — excluded from service planning." |

Ordering within a priority band: most overdue first (`days_until_due` ascending),
then `asset_id` ascending for determinism.

These weights are NOT learned from data and must never be described as a risk score.

## 7. Dataset modes
| Mode | Label shown in UI | Contains events? |
|---|---|---|
| original | "Original dataset (as supplied, unmodified)" | No |
| scenario | "Synthetic demonstration data (generated, seed 42)" | Yes |

Every asset, schedule and event row carries `source_dataset`. The API requires a
`source` parameter (default: `original`). KPIs never mix modes in one number.

## 8. Dataset-level warnings
| Code | Trigger | User-facing meaning |
|---|---|---|
| CONSTANT_DUE_DATE | >90% of ingested rows share one `NextServiceDue` value | "All records share a single service-due date, so this dataset cannot rank which asset to service first." |
| CONSTANT_LAST_SERVICE | >90% share one `LastServiceDate` | "Service history is identical for every asset; elapsed-time analysis is not meaningful." |
| ALL_DATES_IN_PAST | 100% of due dates < as_of_date | "Every scheduled date is historical; figures describe a past state, not upcoming work." |
```

### 2.2 `docs/DATA-PROVENANCE.md`

Must state, with no hedging: where the workbook came from (or that the origin is
**unknown/undocumented**), whether redistribution rights were confirmed, the SHA-256 hash,
and the full generation rules + seed for the scenario dataset. If rights are unknown →
record the decision made at the Milestone 2 gate (keep public / move to a private
submodule / replace with scenario-only demo).

### 2.3 GATE 2 — pass criteria

- [ ] `docs/METRICS.md` exists and contains every boundary decision verbatim.
- [ ] Human has explicitly approved: eligibility rule, inclusive 30-day boundary,
      schedule-resolution rule, priority order, and the two dataset modes.
- [ ] `docs/DATA-PROVENANCE.md` answers the licence question with a decision, not a maybe.

**STOP. Wait for approval.**

---

# MILESTONE 3 — Data strategy: preserve original, generate scenario

**Objective:** a reproducible, clearly labelled synthetic dataset + the untouched original.

### 3.1 Project scaffolding (create now, used from here on)

`pyproject.toml`:

```toml
[project]
name = "assetops"
version = "0.1.0"
description = "IT asset service planning: validation, scheduling and an explainable review queue"
requires-python = ">=3.11"
dependencies = [
  "pandas>=2.2",
  "numpy>=1.26",
  "openpyxl>=3.1",
  "pydantic>=2.7",
  "pydantic-settings>=2.3",
  "psycopg[binary,pool]>=3.2",
  "fastapi>=0.111",
  "uvicorn[standard]>=0.30",
  "typer>=0.12",
  "python-dateutil>=2.9",
]

[project.optional-dependencies]
dashboard = ["streamlit>=1.36", "plotly>=5.22", "requests>=2.32"]
dev = ["pytest>=8.2", "pytest-cov>=5.0", "httpx>=0.27", "ruff>=0.5", "black>=24.4"]

[project.scripts]
assetops = "assetops.cli:app"

[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = ["db: requires a live PostgreSQL database"]
addopts = "-q"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.black]
line-length = 100
```

`.env.example`:

```dotenv
# Copy to .env and adjust. NEVER commit .env
POSTGRES_USER=assetops
POSTGRES_PASSWORD=change_me_locally
POSTGRES_DB=assetops
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://assetops:change_me_locally@db:5432/assetops
TEST_DATABASE_URL=postgresql://assetops:change_me_locally@db:5432/assetops_test
API_BASE_URL=http://api:8000
APP_TIMEZONE=Asia/Kolkata
LOG_LEVEL=INFO
```

`src/assetops/config.py`:

```python
from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://assetops:change_me_locally@localhost:5432/assetops"
    test_database_url: str = "postgresql://assetops:change_me_locally@localhost:5432/assetops_test"
    api_base_url: str = "http://localhost:8000"
    app_timezone: str = "Asia/Kolkata"
    log_level: str = "INFO"

    # Frozen business constants — see docs/METRICS.md
    due_soon_window_days: int = 30
    constant_date_warn_threshold: float = 0.90
    max_page_size: int = 200


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

`src/assetops/scenario/generate.py`:

```python
"""Deterministic generator for the synthetic demonstration dataset.

Rules are documented in docs/DATA-PROVENANCE.md. Same seed -> byte-identical CSVs.
Writes three files: assets.csv, service_schedules.csv, maintenance_events.csv
plus invalid_rows.csv used to demonstrate validation.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np

ASSET_TYPES = ["Laptop", "Printer", "Router", "Monitor", "Keyboard"]
LOCATIONS = ["Hyderabad", "Bangalore", "Pune"]
STATUSES = ["Working", "Under Repair", "Decommissioned"]
STATUS_P = [0.847, 0.103, 0.050]          # matches the original register's mix
SERVICE_INTERVAL_DAYS = {"Laptop": 365, "Printer": 180, "Router": 365,
                         "Monitor": 730, "Keyboard": 730}


@dataclass
class ScenarioConfig:
    n_assets: int = 1200
    seed: int = 42
    anchor: date = date(2026, 1, 15)      # generation anchor; NOT "today"
    n_invalid_rows: int = 12


def generate(cfg: ScenarioConfig, out_dir: Path) -> dict[str, int]:
    rng = np.random.default_rng(cfg.seed)
    out_dir.mkdir(parents=True, exist_ok=True)

    assets, schedules, events = [], [], []
    for i in range(cfg.n_assets):
        aid = f"S{i:05d}"
        atype = ASSET_TYPES[int(rng.integers(0, len(ASSET_TYPES)))]
        loc = LOCATIONS[int(rng.integers(0, len(LOCATIONS)))]
        status = str(rng.choice(STATUSES, p=STATUS_P))
        purchase = cfg.anchor - timedelta(days=int(rng.integers(90, 2200)))
        assets.append({"asset_id": aid, "asset_type": atype, "purchase_date": purchase,
                       "location": loc, "current_status": status})

        # past maintenance events on a per-type interval, with jitter
        interval = SERVICE_INTERVAL_DAYS[atype]
        cursor = purchase + timedelta(days=int(rng.integers(30, interval)))
        n_ev = 0
        while cursor < cfg.anchor:
            etype = "preventive" if rng.random() < 0.7 else "corrective"
            events.append({"asset_id": aid, "event_date": cursor, "event_type": etype,
                           "outcome": "completed"})
            n_ev += 1
            cursor += timedelta(days=int(interval + rng.normal(0, interval * 0.12)))

        # one open schedule per asset, spread so every due category is populated
        last = max((e["event_date"] for e in events if e["asset_id"] == aid),
                   default=purchase)
        offset = int(rng.choice([-120, -45, -7, 0, 5, 18, 30, 45, 120, 300],
                                p=[.05, .08, .07, .02, .10, .13, .05, .15, .20, .15]))
        due = cfg.anchor + timedelta(days=offset)
        # ~4% of assets deliberately have no usable schedule -> UNKNOWN + P1
        if rng.random() < 0.04:
            due = None
        schedules.append({"asset_id": aid, "due_date": due, "schedule_status": "open",
                          "last_service_date": last})

    _write(out_dir / "assets.csv", assets)
    _write(out_dir / "service_schedules.csv", schedules)
    _write(out_dir / "maintenance_events.csv", events)
    _write(out_dir / "invalid_rows.csv", _invalid_rows(cfg))
    return {"assets": len(assets), "schedules": len(schedules),
            "events": len(events), "invalid_rows": cfg.n_invalid_rows}


def _invalid_rows(cfg: ScenarioConfig) -> list[dict]:
    """Deliberately broken rows so validation failures can be demonstrated."""
    return [
        {"asset_id": "", "asset_type": "Laptop", "purchase_date": "2024-01-01",
         "location": "Pune", "current_status": "Working"},                       # missing id
        {"asset_id": "S00001", "asset_type": "Laptop", "purchase_date": "2024-01-01",
         "location": "Pune", "current_status": "Working"},                       # duplicate id
        {"asset_id": "BAD001", "asset_type": "Toaster", "purchase_date": "2024-01-01",
         "location": "Pune", "current_status": "Working"},                       # unknown type
        {"asset_id": "BAD002", "asset_type": "Laptop", "purchase_date": "not-a-date",
         "location": "Pune", "current_status": "Working"},                       # unparseable date
        {"asset_id": "BAD003", "asset_type": "Laptop", "purchase_date": "2035-01-01",
         "location": "Pune", "current_status": "Working"},                       # future purchase
        {"asset_id": "BAD004", "asset_type": "Laptop", "purchase_date": "2024-01-01",
         "location": "Atlantis", "current_status": "Working"},                   # unknown location
        {"asset_id": "BAD005", "asset_type": "Laptop", "purchase_date": "2024-01-01",
         "location": "Pune", "current_status": "Exploded"},                      # unknown status
    ][: cfg.n_invalid_rows]


def _write(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
```

### 3.2 Test (`tests/test_scenario.py`)

```python
import hashlib
from pathlib import Path
from assetops.scenario.generate import ScenarioConfig, generate


def _hash(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_generator_is_deterministic(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    s1 = generate(ScenarioConfig(seed=42), a)
    s2 = generate(ScenarioConfig(seed=42), b)
    assert s1 == s2
    for name in ["assets.csv", "service_schedules.csv", "maintenance_events.csv"]:
        assert _hash(a / name) == _hash(b / name), name


def test_different_seed_changes_output(tmp_path):
    generate(ScenarioConfig(seed=42), tmp_path / "a")
    generate(ScenarioConfig(seed=7), tmp_path / "b")
    assert _hash(tmp_path / "a" / "assets.csv") != _hash(tmp_path / "b" / "assets.csv")


def test_every_due_category_is_represented(tmp_path):
    import csv
    generate(ScenarioConfig(seed=42), tmp_path)
    rows = list(csv.DictReader((tmp_path / "service_schedules.csv").open()))
    assert any(r["due_date"] == "" for r in rows)          # UNKNOWN exists
    assert len(rows) == 1200
```

### 3.3 GATE 3 — pass criteria

- [ ] `pytest tests/test_scenario.py -v` → 3 passed.
- [ ] Original workbook SHA-256 still equals the Milestone 0 value.
- [ ] `data/README.md` explains both modes and points to `docs/DATA-PROVENANCE.md`.
- [ ] `data/scenario/` is gitignored except `.gitkeep`; generation is a documented command.

**STOP. Wait for approval.**

---

# MILESTONE 4 — Database schema and migrations

**Objective:** a coherent relational model with real constraints, applied by a repeatable
migration runner.

### 4.1 `migrations/0001_initial_schema.sql`

```sql
-- AssetOps initial schema. Idempotent: safe to re-run.
BEGIN;

CREATE TABLE IF NOT EXISTS ingestion_runs (
    run_id          BIGSERIAL PRIMARY KEY,
    source_dataset  TEXT        NOT NULL CHECK (source_dataset IN ('original','scenario')),
    source_name     TEXT        NOT NULL,          -- file or directory actually read
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at     TIMESTAMPTZ,
    status          TEXT        NOT NULL DEFAULT 'running'
                    CHECK (status IN ('running','success','failed')),
    rows_read       INTEGER     NOT NULL DEFAULT 0,
    rows_accepted   INTEGER     NOT NULL DEFAULT 0,
    rows_rejected   INTEGER     NOT NULL DEFAULT 0,
    warnings        JSONB       NOT NULL DEFAULT '[]'::jsonb,
    error_message   TEXT
);

CREATE TABLE IF NOT EXISTS assets (
    asset_id        TEXT        NOT NULL,
    source_dataset  TEXT        NOT NULL CHECK (source_dataset IN ('original','scenario')),
    asset_type      TEXT        NOT NULL,
    purchase_date   DATE        NOT NULL,
    location        TEXT        NOT NULL,
    current_status  TEXT        NOT NULL
                    CHECK (current_status IN ('Working','Under Repair','Decommissioned')),
    first_seen_run  BIGINT      REFERENCES ingestion_runs(run_id),
    last_seen_run   BIGINT      REFERENCES ingestion_runs(run_id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (source_dataset, asset_id),
    CONSTRAINT purchase_not_future CHECK (purchase_date <= CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS service_schedules (
    schedule_id     BIGSERIAL PRIMARY KEY,
    source_dataset  TEXT NOT NULL,
    asset_id        TEXT NOT NULL,
    due_date        DATE,                       -- NULL is legal => UNKNOWN due status
    last_service_date DATE,
    schedule_status TEXT NOT NULL DEFAULT 'open'
                    CHECK (schedule_status IN ('open','closed','cancelled')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    FOREIGN KEY (source_dataset, asset_id)
        REFERENCES assets(source_dataset, asset_id) ON DELETE CASCADE,
    CONSTRAINT due_after_last_service
        CHECK (due_date IS NULL OR last_service_date IS NULL OR due_date >= last_service_date)
);

-- one OPEN schedule per asset per dataset (documented design choice: current schedule only)
CREATE UNIQUE INDEX IF NOT EXISTS uq_open_schedule_per_asset
    ON service_schedules (source_dataset, asset_id)
    WHERE schedule_status = 'open';

CREATE TABLE IF NOT EXISTS maintenance_events (
    event_id        BIGSERIAL PRIMARY KEY,
    source_dataset  TEXT NOT NULL,
    asset_id        TEXT NOT NULL,
    event_date      DATE NOT NULL,
    event_type      TEXT NOT NULL CHECK (event_type IN ('preventive','corrective','inspection')),
    outcome         TEXT CHECK (outcome IN ('completed','incomplete','cancelled')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    FOREIGN KEY (source_dataset, asset_id)
        REFERENCES assets(source_dataset, asset_id) ON DELETE CASCADE,
    CONSTRAINT event_not_future CHECK (event_date <= CURRENT_DATE)
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_event_natural_key
    ON maintenance_events (source_dataset, asset_id, event_date, event_type);

CREATE TABLE IF NOT EXISTS rejected_records (
    rejection_id    BIGSERIAL PRIMARY KEY,
    run_id          BIGINT NOT NULL REFERENCES ingestion_runs(run_id) ON DELETE CASCADE,
    source_row_no   INTEGER,
    source_key      TEXT,             -- asset id if it could be read, else NULL
    reason_code     TEXT NOT NULL,
    reason_message  TEXT NOT NULL,
    field_name      TEXT,
    offending_value TEXT,             -- truncated to 200 chars by the loader
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMIT;
```

### 4.2 `migrations/0002_indexes.sql`

```sql
BEGIN;
CREATE INDEX IF NOT EXISTS ix_assets_status   ON assets (source_dataset, current_status);
CREATE INDEX IF NOT EXISTS ix_assets_type_loc ON assets (source_dataset, asset_type, location);
CREATE INDEX IF NOT EXISTS ix_sched_due       ON service_schedules (source_dataset, due_date)
    WHERE schedule_status = 'open';
CREATE INDEX IF NOT EXISTS ix_events_asset    ON maintenance_events (source_dataset, asset_id, event_date DESC);
CREATE INDEX IF NOT EXISTS ix_rejected_run    ON rejected_records (run_id, reason_code);
CREATE INDEX IF NOT EXISTS ix_runs_recent     ON ingestion_runs (source_dataset, finished_at DESC);
COMMIT;
```

> **Decision to record in `docs/DECISIONS.md`:** plain SQL migrations + a 40-line runner
> are used instead of Alembic. Rationale: the schema is small and stable, the runner is
> auditable in one screen, and it removes an ORM-metadata failure mode from CI. Trade-off:
> no autogenerate, no downgrade — documented, not hidden.

### 4.3 `scripts/migrate.py`

```python
"""Apply SQL migrations in filename order, recording what has been applied."""
from __future__ import annotations

import pathlib
import sys

import psycopg

from assetops.config import get_settings

MIGRATIONS = pathlib.Path(__file__).resolve().parents[1] / "migrations"

BOOTSTRAP = """
CREATE TABLE IF NOT EXISTS schema_migrations (
    filename    TEXT PRIMARY KEY,
    applied_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


def main(dsn: str | None = None) -> int:
    dsn = dsn or get_settings().database_url
    files = sorted(MIGRATIONS.glob("*.sql"))
    if not files:
        print("no migration files found", file=sys.stderr)
        return 1
    with psycopg.connect(dsn, autocommit=True) as conn:
        conn.execute(BOOTSTRAP)
        applied = {r[0] for r in conn.execute("SELECT filename FROM schema_migrations")}
        for f in files:
            if f.name in applied:
                print(f"skip    {f.name}")
                continue
            print(f"apply   {f.name}")
            conn.execute(f.read_text())
            conn.execute("INSERT INTO schema_migrations(filename) VALUES (%s)", (f.name,))
        tables = conn.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema='public' ORDER BY table_name").fetchall()
    print("tables:", ", ".join(t[0] for t in tables))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else None))
```

### 4.4 `src/assetops/database/connection.py`

```python
from __future__ import annotations

from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from assetops.config import get_settings

_pool: ConnectionPool | None = None


def get_pool() -> ConnectionPool:
    global _pool
    if _pool is None:
        _pool = ConnectionPool(get_settings().database_url, min_size=1, max_size=8,
                               kwargs={"row_factory": dict_row}, open=True)
    return _pool


@contextmanager
def get_conn():
    with get_pool().connection() as conn:
        yield conn


def healthcheck() -> bool:
    try:
        with get_conn() as c:
            c.execute("SELECT 1")
        return True
    except psycopg.Error:
        return False
```

### 4.5 Verification commands

```bash
docker compose up -d db
docker compose exec -T db psql -U assetops -d assetops -c "CREATE DATABASE assetops_test;" || true
python -m scripts.migrate
python -m scripts.migrate     # second run must print only "skip" lines
```

Constraint proof (run each; **each must fail** with the stated error):

```sql
-- 1. FK violation
INSERT INTO service_schedules(source_dataset, asset_id, due_date)
VALUES ('original','GHOST','2026-01-01');                 -- expect: violates foreign key

-- 2. status domain
INSERT INTO assets(asset_id,source_dataset,asset_type,purchase_date,location,current_status)
VALUES ('X1','original','Laptop','2024-01-01','Pune','Exploded');  -- expect: check constraint

-- 3. duplicate open schedule
-- (insert a valid asset first, then two open schedules)   -- expect: unique index violation

-- 4. future purchase date
VALUES (... '2099-01-01' ...)                              -- expect: purchase_not_future
```

### 4.6 `docs/DATABASE.md` must contain

- An ER diagram (Mermaid is fine — renders on GitHub):

```mermaid
erDiagram
    ingestion_runs ||--o{ rejected_records : produces
    assets ||--o{ service_schedules : has
    assets ||--o{ maintenance_events : has
    assets {
      text asset_id PK
      text source_dataset PK
      text asset_type
      date purchase_date
      text location
      text current_status
    }
    service_schedules {
      bigint schedule_id PK
      date due_date
      text schedule_status
    }
    maintenance_events {
      bigint event_id PK
      date event_date
      text event_type
    }
```

- Why `(source_dataset, asset_id)` is the composite key (two modes coexist without collision).
- Why `days_until_due` is **not** stored.
- Why only the *current* schedule is stored (no schedule history) — and what would change
  if history were needed.

### 4.7 GATE 4 — pass criteria

- [ ] `python -m scripts.migrate` twice: first applies, second is a no-op.
- [ ] All four constraint-violation statements fail with the expected Postgres error
      (paste the real error text).
- [ ] `docs/DATABASE.md` contains the ER diagram and the three design rationales.

**STOP. Wait for approval.**

---

# MILESTONE 5 — Ingestion CLI with validation and safe reruns

### 5.1 `src/assetops/ingestion/validation.py`

```python
"""Row-level validation. Pure functions: no DB, no file IO -> fast unit tests."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

VALID_STATUSES = {"Working", "Under Repair", "Decommissioned"}
VALID_TYPES = {"Laptop", "Printer", "Router", "Monitor", "Keyboard"}
VALID_LOCATIONS = {"Hyderabad", "Bangalore", "Pune"}


@dataclass(frozen=True)
class Rejection:
    row_no: int
    source_key: str | None
    reason_code: str
    reason_message: str
    field_name: str | None = None
    offending_value: str | None = None


@dataclass
class ValidationResult:
    accepted: list[dict[str, Any]] = field(default_factory=list)
    rejections: list[Rejection] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)

    @property
    def counts(self) -> dict[str, int]:
        return {"accepted": len(self.accepted), "rejected": len(self.rejections)}


def parse_date(value: Any) -> date | None:
    if value in (None, "", "NaT"):
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(str(value).strip()[:10], fmt).date()
        except ValueError:
            continue
    return None


REQUIRED_COLUMNS = ["asset_id", "asset_type", "purchase_date", "location", "current_status"]


def validate_rows(rows: list[dict[str, Any]], *, as_of: date) -> ValidationResult:
    res = ValidationResult()
    seen: set[str] = set()

    for i, raw in enumerate(rows, start=2):        # start=2 -> spreadsheet row numbers
        aid = str(raw.get("asset_id", "") or "").strip()
        if not aid:
            res.rejections.append(Rejection(i, None, "MISSING_ASSET_ID",
                                            "asset_id is empty", "asset_id", ""))
            continue
        if aid in seen:
            res.rejections.append(Rejection(i, aid, "DUPLICATE_ASSET_ID",
                                            f"asset_id {aid} appears more than once in this file",
                                            "asset_id", aid))
            continue

        atype = str(raw.get("asset_type", "") or "").strip()
        if atype not in VALID_TYPES:
            res.rejections.append(Rejection(i, aid, "UNKNOWN_ASSET_TYPE",
                                            f"'{atype}' is not a known asset type",
                                            "asset_type", atype))
            continue

        loc = str(raw.get("location", "") or "").strip()
        if loc not in VALID_LOCATIONS:
            res.rejections.append(Rejection(i, aid, "UNKNOWN_LOCATION",
                                            f"'{loc}' is not a known location", "location", loc))
            continue

        status = str(raw.get("current_status", "") or "").strip()
        if status not in VALID_STATUSES:
            res.rejections.append(Rejection(i, aid, "UNKNOWN_STATUS",
                                            f"'{status}' is not a known status",
                                            "current_status", status))
            continue

        pdate = parse_date(raw.get("purchase_date"))
        if pdate is None:
            res.rejections.append(Rejection(i, aid, "UNPARSEABLE_DATE",
                                            "purchase_date could not be parsed",
                                            "purchase_date", str(raw.get("purchase_date"))[:200]))
            continue
        if pdate > as_of:
            res.rejections.append(Rejection(i, aid, "FUTURE_PURCHASE_DATE",
                                            f"purchase_date {pdate} is after {as_of}",
                                            "purchase_date", str(pdate)))
            continue

        due = parse_date(raw.get("due_date"))
        last = parse_date(raw.get("last_service_date"))
        if due and last and due < last:
            res.rejections.append(Rejection(i, aid, "DUE_BEFORE_LAST_SERVICE",
                                            f"due_date {due} precedes last_service_date {last}",
                                            "due_date", str(due)))
            continue

        seen.add(aid)
        res.accepted.append({"asset_id": aid, "asset_type": atype, "location": loc,
                             "current_status": status, "purchase_date": pdate,
                             "due_date": due, "last_service_date": last})

    res.warnings = dataset_warnings(res.accepted, as_of=as_of)
    return res


def dataset_warnings(rows: list[dict[str, Any]], *, as_of: date,
                     threshold: float = 0.90) -> list[dict[str, Any]]:
    """Dataset-level anomalies. These WARN; they never reject rows."""
    out: list[dict[str, Any]] = []
    n = len(rows)
    if n == 0:
        return out

    def _dominant(field_name: str) -> tuple[Any, float]:
        vals = [r.get(field_name) for r in rows if r.get(field_name) is not None]
        if not vals:
            return None, 0.0
        top = max(set(vals), key=vals.count)
        return top, vals.count(top) / n

    top_due, share_due = _dominant("due_date")
    if share_due >= threshold:
        out.append({"code": "CONSTANT_DUE_DATE", "value": str(top_due),
                    "share": round(share_due, 4),
                    "message": ("All records share a single service-due date, so this dataset "
                                "cannot rank which asset to service first.")})

    top_last, share_last = _dominant("last_service_date")
    if share_last >= threshold:
        out.append({"code": "CONSTANT_LAST_SERVICE", "value": str(top_last),
                    "share": round(share_last, 4),
                    "message": ("Service history is identical for every asset; elapsed-time "
                                "analysis is not meaningful.")})

    dues = [r["due_date"] for r in rows if r.get("due_date")]
    if dues and all(d < as_of for d in dues):
        out.append({"code": "ALL_DATES_IN_PAST", "value": str(max(dues)), "share": 1.0,
                    "message": ("Every scheduled date is historical; figures describe a past "
                                "state, not upcoming work.")})
    return out
```

### 5.2 `src/assetops/ingestion/excel_reader.py`

```python
"""Read the original workbook and map its columns to the canonical schema."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

COLUMN_MAP = {
    "AssetID": "asset_id",
    "AssetType": "asset_type",
    "PurchaseDate": "purchase_date",
    "LastServiceDate": "last_service_date",
    "NextServiceDue": "due_date",
    "Status": "current_status",
    "Location": "location",
}


class SchemaMismatch(RuntimeError):
    pass


def read_original(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"input file not found: {path}")
    df = pd.read_excel(path)
    df.columns = [str(c).strip() for c in df.columns]
    missing = [c for c in COLUMN_MAP if c not in df.columns]
    if missing:
        raise SchemaMismatch(f"missing expected columns: {missing}; found {list(df.columns)}")
    df = df.rename(columns=COLUMN_MAP)[list(COLUMN_MAP.values())]
    return df.to_dict("records")
```

### 5.3 `src/assetops/ingestion/loader.py` (upsert + run recording)

```python
from __future__ import annotations

import json
from datetime import date
from typing import Any

from assetops.database.connection import get_conn
from assetops.ingestion.validation import Rejection, ValidationResult

UPSERT_ASSET = """
INSERT INTO assets (asset_id, source_dataset, asset_type, purchase_date, location,
                    current_status, first_seen_run, last_seen_run)
VALUES (%(asset_id)s, %(src)s, %(asset_type)s, %(purchase_date)s, %(location)s,
        %(current_status)s, %(run_id)s, %(run_id)s)
ON CONFLICT (source_dataset, asset_id) DO UPDATE SET
    asset_type = EXCLUDED.asset_type,
    purchase_date = EXCLUDED.purchase_date,
    location = EXCLUDED.location,
    current_status = EXCLUDED.current_status,
    last_seen_run = EXCLUDED.last_seen_run,
    updated_at = now();
"""

CLOSE_OPEN_SCHEDULES = """
UPDATE service_schedules SET schedule_status='closed', updated_at=now()
WHERE source_dataset=%(src)s AND asset_id=%(asset_id)s AND schedule_status='open';
"""

INSERT_SCHEDULE = """
INSERT INTO service_schedules (source_dataset, asset_id, due_date, last_service_date,
                               schedule_status)
VALUES (%(src)s, %(asset_id)s, %(due_date)s, %(last_service_date)s, 'open');
"""

INSERT_EVENT = """
INSERT INTO maintenance_events (source_dataset, asset_id, event_date, event_type, outcome)
VALUES (%(src)s, %(asset_id)s, %(event_date)s, %(event_type)s, %(outcome)s)
ON CONFLICT (source_dataset, asset_id, event_date, event_type) DO NOTHING;
"""


def start_run(source_dataset: str, source_name: str) -> int:
    with get_conn() as c:
        row = c.execute(
            "INSERT INTO ingestion_runs (source_dataset, source_name) "
            "VALUES (%s, %s) RETURNING run_id", (source_dataset, source_name)).fetchone()
        c.commit()
    return row["run_id"]


def finish_run(run_id: int, *, status: str, read: int, accepted: int, rejected: int,
               warnings: list[dict[str, Any]], error: str | None = None) -> None:
    with get_conn() as c:
        c.execute("""UPDATE ingestion_runs SET finished_at=now(), status=%s, rows_read=%s,
                     rows_accepted=%s, rows_rejected=%s, warnings=%s, error_message=%s
                     WHERE run_id=%s""",
                  (status, read, accepted, rejected, json.dumps(warnings), error, run_id))
        c.commit()


def persist(run_id: int, source_dataset: str, result: ValidationResult,
            events: list[dict[str, Any]] | None = None) -> None:
    """One transaction: either the whole run's rows land, or none of them do."""
    with get_conn() as c:
        with c.transaction():
            for row in result.accepted:
                c.execute(UPSERT_ASSET, {**row, "src": source_dataset, "run_id": run_id})
                c.execute(CLOSE_OPEN_SCHEDULES, {"src": source_dataset,
                                                 "asset_id": row["asset_id"]})
                c.execute(INSERT_SCHEDULE, {"src": source_dataset, **row})
            for ev in (events or []):
                c.execute(INSERT_EVENT, {"src": source_dataset, **ev})
            for r in result.rejections:
                c.execute("""INSERT INTO rejected_records
                             (run_id, source_row_no, source_key, reason_code, reason_message,
                              field_name, offending_value)
                             VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                          (run_id, r.row_no, r.source_key, r.reason_code, r.reason_message,
                           r.field_name, (r.offending_value or "")[:200]))
```

**Rerun policy (document it in `docs/DATA-QUALITY.md`):** assets are **upserted** on
`(source_dataset, asset_id)`; the previously open schedule is closed and a new open
schedule is inserted, so schedule changes are visible while only one open row exists;
events are deduplicated by their natural key. Therefore *ingesting the same file twice
never changes the asset count* and never duplicates events.

### 5.4 `src/assetops/cli.py`

```python
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

import typer

from assetops.ingestion import loader
from assetops.ingestion.excel_reader import read_original
from assetops.ingestion.validation import validate_rows
from assetops.scenario.generate import ScenarioConfig, generate

app = typer.Typer(add_completion=False, help="AssetOps ingestion and data tools")


@app.command()
def ingest(
    source: str = typer.Option(..., help="original | scenario"),
    file: Path = typer.Option(None, help="Excel file (original mode)"),
    directory: Path = typer.Option(None, help="CSV directory (scenario mode)"),
    as_of: str = typer.Option(None, help="YYYY-MM-DD; defaults to today"),
):
    as_of_date = date.fromisoformat(as_of) if as_of else date.today()
    if source not in {"original", "scenario"}:
        raise typer.BadParameter("source must be 'original' or 'scenario'")

    src_name = str(file or directory)
    run_id = loader.start_run(source, src_name)
    try:
        events: list[dict] = []
        if source == "original":
            if not file:
                raise typer.BadParameter("--file is required for original mode")
            rows = read_original(file)
        else:
            if not directory:
                raise typer.BadParameter("--directory is required for scenario mode")
            rows = _read_scenario_assets(directory)
            events = _read_scenario_events(directory)

        result = validate_rows(rows, as_of=as_of_date)
        loader.persist(run_id, source, result, events)
        loader.finish_run(run_id, status="success", read=len(rows),
                          accepted=len(result.accepted), rejected=len(result.rejections),
                          warnings=result.warnings)
        typer.echo(f"run {run_id}: read={len(rows)} accepted={len(result.accepted)} "
                   f"rejected={len(result.rejections)} events={len(events)}")
        for w in result.warnings:
            typer.secho(f"WARNING [{w['code']}] {w['message']}", fg=typer.colors.YELLOW)
        for r in result.rejections[:10]:
            typer.echo(f"  reject row {r.row_no}: {r.reason_code} - {r.reason_message}")
    except Exception as exc:                      # noqa: BLE001 - recorded then re-raised
        loader.finish_run(run_id, status="failed", read=0, accepted=0, rejected=0,
                          warnings=[], error=str(exc)[:500])
        typer.secho(f"run {run_id} FAILED: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


@app.command("generate-scenario")
def generate_scenario(seed: int = 42, output: Path = Path("data/scenario"),
                      n_assets: int = 1200):
    counts = generate(ScenarioConfig(seed=seed, n_assets=n_assets), output)
    typer.echo(f"generated into {output}: {counts}")


def _read_scenario_assets(directory: Path) -> list[dict]:
    a = {r["asset_id"]: r for r in csv.DictReader((directory / "assets.csv").open())}
    for s in csv.DictReader((directory / "service_schedules.csv").open()):
        if s["asset_id"] in a:
            a[s["asset_id"]]["due_date"] = s["due_date"] or None
            a[s["asset_id"]]["last_service_date"] = s["last_service_date"] or None
    return list(a.values())


def _read_scenario_events(directory: Path) -> list[dict]:
    p = directory / "maintenance_events.csv"
    return list(csv.DictReader(p.open())) if p.exists() else []
```

### 5.5 Verification

```bash
pip install -e ".[dev]"
assetops generate-scenario --seed 42 --output data/scenario
assetops ingest --source original  --file "legacy/01_IT_ASSESMENT(raw data).xlsx"
assetops ingest --source original  --file "legacy/01_IT_ASSESMENT(raw data).xlsx"   # rerun
assetops ingest --source scenario  --directory data/scenario
assetops ingest --source original  --file "legacy/does-not-exist.xlsx"              # must exit 1
```

```sql
SELECT source_dataset, count(*) FROM assets GROUP BY 1;             -- original must be 10000 after BOTH runs
SELECT run_id, status, rows_read, rows_accepted, rows_rejected, warnings FROM ingestion_runs ORDER BY run_id;
SELECT reason_code, count(*) FROM rejected_records GROUP BY 1 ORDER BY 2 DESC;
SELECT count(*) FROM service_schedules WHERE schedule_status='open';  -- == number of assets
```

### 5.6 GATE 5 — pass criteria

- [ ] Original ingest reports `CONSTANT_DUE_DATE` **and** `CONSTANT_LAST_SERVICE` warnings.
- [ ] Rerunning the same file leaves the asset count **unchanged** (paste both counts).
- [ ] Missing-file run is recorded as `failed` with an error message and exits non-zero.
- [ ] `rejected_records` contains at least one row per reason code exercised by the
      scenario `invalid_rows.csv`.
- [ ] `pytest tests/test_validation.py tests/test_excel_reader.py -v` passes.

**STOP. Wait for approval.**

---

# MILESTONE 6 — Domain logic and SQL (single source of truth for the rules)

### 6.1 `src/assetops/domain/due_status.py`

```python
from __future__ import annotations

from datetime import date, timedelta
from enum import StrEnum

DUE_SOON_WINDOW_DAYS = 30


class DueStatus(StrEnum):
    UNKNOWN = "UNKNOWN"
    OVERDUE = "OVERDUE"
    DUE_WITHIN_30 = "DUE_WITHIN_30"
    LATER = "LATER"


def classify(due_date: date | None, as_of: date,
             window_days: int = DUE_SOON_WINDOW_DAYS) -> DueStatus:
    """See docs/METRICS.md section 4. Boundaries are INCLUSIVE at both ends."""
    if due_date is None:
        return DueStatus.UNKNOWN
    if due_date < as_of:
        return DueStatus.OVERDUE
    if due_date <= as_of + timedelta(days=window_days):
        return DueStatus.DUE_WITHIN_30
    return DueStatus.LATER


def days_until_due(due_date: date | None, as_of: date) -> int | None:
    return None if due_date is None else (due_date - as_of).days
```

### 6.2 `src/assetops/domain/priority.py`

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum

from assetops.domain.due_status import DueStatus, classify, days_until_due

ELIGIBLE_STATUSES = {"Working", "Under Repair"}


class Priority(StrEnum):
    P1_DATA_REVIEW = "P1_DATA_REVIEW"
    P2_URGENT_OPERATIONAL = "P2_URGENT_OPERATIONAL"
    P3_OVERDUE = "P3_OVERDUE"
    P4_DUE_SOON = "P4_DUE_SOON"
    P5_NO_ACTION = "P5_NO_ACTION"
    EXCLUDED = "EXCLUDED"


PRIORITY_RANK = {Priority.P1_DATA_REVIEW: 1, Priority.P2_URGENT_OPERATIONAL: 2,
                 Priority.P3_OVERDUE: 3, Priority.P4_DUE_SOON: 4,
                 Priority.P5_NO_ACTION: 5, Priority.EXCLUDED: 9}

SUGGESTED_ACTION = {
    Priority.P1_DATA_REVIEW: "Correct the service schedule record",
    Priority.P2_URGENT_OPERATIONAL: "Escalate: repair in progress and service overdue",
    Priority.P3_OVERDUE: "Schedule service now",
    Priority.P4_DUE_SOON: "Add to the next service batch",
    Priority.P5_NO_ACTION: "No action",
    Priority.EXCLUDED: "None — asset is decommissioned",
}


@dataclass(frozen=True)
class PriorityDecision:
    priority: Priority
    rank: int
    reason: str
    suggested_action: str
    due_status: DueStatus
    days_until_due: int | None


def decide(*, current_status: str, due_date: date | None, as_of: date) -> PriorityDecision:
    """Rule-based, deterministic, explainable. NOT a learned risk score."""
    ds = classify(due_date, as_of)
    n = days_until_due(due_date, as_of)

    if current_status not in ELIGIBLE_STATUSES:
        p, reason = Priority.EXCLUDED, "Decommissioned — excluded from service planning."
    elif ds is DueStatus.UNKNOWN:
        p = Priority.P1_DATA_REVIEW
        reason = ("No usable service schedule on record — this asset cannot be planned "
                  "until the schedule is corrected.")
    elif ds is DueStatus.OVERDUE and current_status == "Under Repair":
        p = Priority.P2_URGENT_OPERATIONAL
        reason = f"Overdue by {abs(n)} days and currently under repair."
    elif ds is DueStatus.OVERDUE:
        p, reason = Priority.P3_OVERDUE, f"Overdue by {abs(n)} days."
    elif ds is DueStatus.DUE_WITHIN_30:
        p, reason = Priority.P4_DUE_SOON, f"Due in {n} days."
    else:
        p = Priority.P5_NO_ACTION
        reason = f"Next service due in {n} days — no action required now."

    return PriorityDecision(p, PRIORITY_RANK[p], reason, SUGGESTED_ACTION[p], ds, n)
```

### 6.3 `sql/analytical_queries.sql` — the SQL must agree with the Python

```sql
-- =====================================================================
-- AssetOps analytical layer.
-- Every query takes :as_of (DATE) and :src (TEXT) as parameters.
-- The due-status CASE below is the SQL twin of assetops.domain.due_status.classify
-- and is covered by tests/test_sql_metrics.py.
-- =====================================================================

-- @query: governing_schedule  (reusable building block)
-- Q: which schedule row governs each asset?  (earliest open due date)
CREATE OR REPLACE VIEW v_governing_schedule AS
SELECT DISTINCT ON (source_dataset, asset_id)
       source_dataset, asset_id, due_date, last_service_date, schedule_id
FROM   service_schedules
WHERE  schedule_status = 'open'
ORDER  BY source_dataset, asset_id, due_date NULLS LAST, schedule_id;

-- @query: asset_due_status
-- Q: what is every asset's due category as of a given date?
SELECT a.source_dataset, a.asset_id, a.asset_type, a.location, a.current_status,
       g.due_date,
       (g.due_date - %(as_of)s::date) AS days_until_due,
       CASE
         WHEN a.current_status = 'Decommissioned'        THEN 'EXCLUDED'
         WHEN g.due_date IS NULL                          THEN 'UNKNOWN'
         WHEN g.due_date <  %(as_of)s::date               THEN 'OVERDUE'
         WHEN g.due_date <= %(as_of)s::date + 30          THEN 'DUE_WITHIN_30'
         ELSE 'LATER'
       END AS due_status
FROM assets a
LEFT JOIN v_governing_schedule g
       ON g.source_dataset = a.source_dataset AND g.asset_id = a.asset_id
WHERE a.source_dataset = %(src)s;

-- @query: kpi_summary
-- Q: the six headline numbers for the executive view.
WITH s AS ( /* paste asset_due_status body here or select from a view */
  SELECT a.current_status, g.due_date,
         CASE WHEN a.current_status='Decommissioned' THEN 'EXCLUDED'
              WHEN g.due_date IS NULL THEN 'UNKNOWN'
              WHEN g.due_date <  %(as_of)s::date THEN 'OVERDUE'
              WHEN g.due_date <= %(as_of)s::date + 30 THEN 'DUE_WITHIN_30'
              ELSE 'LATER' END AS due_status
  FROM assets a
  LEFT JOIN v_governing_schedule g
         ON g.source_dataset=a.source_dataset AND g.asset_id=a.asset_id
  WHERE a.source_dataset = %(src)s
)
SELECT
  count(*) FILTER (WHERE current_status <> 'Decommissioned')        AS active_assets,
  count(*) FILTER (WHERE current_status = 'Under Repair')           AS currently_under_repair,
  count(*) FILTER (WHERE due_status = 'OVERDUE')                    AS overdue_scheduled_service,
  count(*) FILTER (WHERE due_status = 'DUE_WITHIN_30')              AS due_within_30_days,
  count(*) FILTER (WHERE due_status = 'UNKNOWN')                    AS unknown_schedule,
  count(*) FILTER (WHERE current_status = 'Decommissioned')         AS decommissioned
FROM s;

-- @query: overdue_by_type_location
-- Q: where is the overdue work concentrated?
SELECT a.asset_type, a.location,
       count(*)                                            AS eligible_assets,
       count(*) FILTER (WHERE g.due_date < %(as_of)s::date) AS overdue,
       round(100.0 * count(*) FILTER (WHERE g.due_date < %(as_of)s::date)
             / nullif(count(*), 0), 1)                      AS overdue_pct
FROM assets a
LEFT JOIN v_governing_schedule g
       ON g.source_dataset=a.source_dataset AND g.asset_id=a.asset_id
WHERE a.source_dataset=%(src)s AND a.current_status <> 'Decommissioned'
GROUP BY a.asset_type, a.location
ORDER BY overdue DESC, a.asset_type;

-- @query: latest_event_per_asset
-- Q: when was each asset last serviced, and what happened? (window function)
SELECT asset_id, event_date, event_type, outcome
FROM (
  SELECT e.*, ROW_NUMBER() OVER (PARTITION BY e.asset_id ORDER BY e.event_date DESC,
                                                                  e.event_id DESC) AS rn
  FROM maintenance_events e
  WHERE e.source_dataset = %(src)s
) t
WHERE rn = 1
ORDER BY event_date DESC;

-- @query: repeat_corrective_events
-- Q: which assets needed corrective work more than twice in the last 365 days?
WITH recent AS (
  SELECT asset_id, count(*) AS corrective_events, max(event_date) AS last_event
  FROM maintenance_events
  WHERE source_dataset=%(src)s AND event_type='corrective'
    AND event_date > %(as_of)s::date - 365
  GROUP BY asset_id
)
SELECT r.asset_id, a.asset_type, a.location, a.current_status,
       r.corrective_events, r.last_event
FROM recent r JOIN assets a
  ON a.asset_id=r.asset_id AND a.source_dataset=%(src)s
WHERE r.corrective_events > 2
ORDER BY r.corrective_events DESC, r.last_event DESC;

-- @query: ingestion_problem_profile
-- Q: which validation problems occur most often, and in which run?
SELECT r.source_dataset, rr.reason_code, count(*) AS occurrences,
       min(rr.created_at) AS first_seen, max(rr.created_at) AS last_seen
FROM rejected_records rr
JOIN ingestion_runs r ON r.run_id = rr.run_id
GROUP BY r.source_dataset, rr.reason_code
ORDER BY occurrences DESC;

-- @query: data_freshness
-- Q: how current is what the dashboard is showing?
SELECT source_dataset, max(finished_at) AS last_successful_ingest
FROM ingestion_runs
WHERE status='success'
GROUP BY source_dataset;
```

### 6.4 Parity test (`tests/test_sql_metrics.py`) — the important one

```python
"""Prove the SQL CASE and the Python classifier cannot drift apart."""
import datetime as dt
import pytest

from assetops.domain.due_status import DueStatus, classify

pytestmark = pytest.mark.db

CASES = [
    (dt.date(2026, 1, 14), DueStatus.OVERDUE),
    (dt.date(2026, 1, 15), DueStatus.DUE_WITHIN_30),   # == as_of
    (dt.date(2026, 2, 14), DueStatus.DUE_WITHIN_30),   # as_of + 30
    (dt.date(2026, 2, 15), DueStatus.LATER),           # as_of + 31
    (None,                 DueStatus.UNKNOWN),
]
AS_OF = dt.date(2026, 1, 15)


def test_sql_matches_python(db_conn, seeded_assets):
    rows = db_conn.execute(
        """SELECT asset_id,
                  CASE WHEN due_date IS NULL THEN 'UNKNOWN'
                       WHEN due_date <  %(as_of)s::date THEN 'OVERDUE'
                       WHEN due_date <= %(as_of)s::date + 30 THEN 'DUE_WITHIN_30'
                       ELSE 'LATER' END AS sql_status,
                  due_date
             FROM v_governing_schedule
             WHERE source_dataset='test'""", {"as_of": AS_OF}).fetchall()
    for r in rows:
        assert r["sql_status"] == classify(r["due_date"], AS_OF).value, r["asset_id"]
```

### 6.5 GATE 6 — pass criteria

- [ ] `pytest tests/test_due_status.py tests/test_priority.py -v` → every boundary case in
      §12.1 passes.
- [ ] `pytest tests/test_sql_metrics.py -v` → SQL/Python parity passes on seeded fixtures.
- [ ] Running `kpi_summary` against the **original** dataset returns numbers that a human
      can reconcile by hand against a small `psql` count; paste both.
- [ ] No query uses string concatenation for parameters.

**STOP. Wait for approval.**

---

# MILESTONE 7 — Read-only API

### 7.1 `src/assetops/api/schemas.py`

```python
from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

SourceMode = Literal["original", "scenario"]


class HealthOut(BaseModel):
    status: Literal["ok", "degraded"]
    database: bool
    version: str


class DatasetWarning(BaseModel):
    code: str
    message: str
    share: float | None = None
    value: str | None = None


class MetricsOut(BaseModel):
    source: SourceMode
    as_of_date: date
    active_assets: int
    currently_under_repair: int
    currently_under_repair_pct: float
    overdue_scheduled_service: int
    due_within_30_days: int
    unknown_schedule: int
    decommissioned: int
    maintenance_events_90d: int | None
    data_freshness: datetime | None
    warnings: list[DatasetWarning]


class AssetOut(BaseModel):
    asset_id: str
    asset_type: str
    location: str
    current_status: str
    purchase_date: date
    due_date: date | None
    days_until_due: int | None
    due_status: str


class PageMeta(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total: int


class AssetPage(BaseModel):
    meta: PageMeta
    items: list[AssetOut]


class EventOut(BaseModel):
    event_date: date
    event_type: str
    outcome: str | None


class AssetDetailOut(AssetOut):
    source: SourceMode
    priority: str
    reason: str
    suggested_action: str
    events: list[EventOut]


class PriorityItem(AssetOut):
    priority: str
    rank: int
    reason: str
    suggested_action: str


class PriorityPage(BaseModel):
    meta: PageMeta
    as_of_date: date
    items: list[PriorityItem]


class RunOut(BaseModel):
    run_id: int
    source_dataset: str
    source_name: str
    started_at: datetime
    finished_at: datetime | None
    status: str
    rows_read: int
    rows_accepted: int
    rows_rejected: int
    warnings: list[DatasetWarning]
    error_message: str | None


class IssueOut(BaseModel):
    reason_code: str
    reason_message: str
    occurrences: int
    example_row_no: int | None
    example_field: str | None


class ErrorOut(BaseModel):
    detail: str
    code: str
```

### 7.2 `src/assetops/api/main.py`

```python
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from assetops.api.routes import assets, data_quality, health, metrics, priorities

logging.basicConfig(level="INFO",
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("assetops.api")

app = FastAPI(
    title="AssetOps API",
    version="0.1.0",
    description=("Read-only API for IT asset service planning. "
                 "All figures are rule-based; nothing here is a forecast."),
)

app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(assets.router)
app.include_router(priorities.router)
app.include_router(data_quality.router)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    log.exception("unhandled error on %s", request.url.path)
    return JSONResponse(status_code=500,
                        content={"detail": "internal server error", "code": "INTERNAL"})
```

### 7.3 `src/assetops/api/deps.py`

```python
from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException, Query

from assetops.config import get_settings


def as_of_param(as_of_date: date | None = Query(None, description="YYYY-MM-DD")) -> date:
    tz = ZoneInfo(get_settings().app_timezone)
    today = datetime.now(tz).date()
    d = as_of_date or today
    if d.year < 2000 or d.year > today.year + 5:
        raise HTTPException(422, detail=f"as_of_date {d} is outside the supported range")
    return d


def source_param(source: str = Query("original", pattern="^(original|scenario)$")) -> str:
    return source


def page_params(page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=200)):
    return page, page_size
```

### 7.4 Route contract (implement each in its own file)

| Method | Path | Query params | 200 body | Error cases |
|---|---|---|---|---|
| GET | `/health` | — | `HealthOut` | 200 with `database:false` if DB down (never 500) |
| GET | `/metrics` | `source`, `as_of_date` | `MetricsOut` | 422 bad date/source |
| GET | `/assets` | `source`, `as_of_date`, `asset_type`, `location`, `status`, `due_status`, `page`, `page_size` | `AssetPage` | 422 bad filter value, `page_size>200` |
| GET | `/assets/{asset_id}` | `source`, `as_of_date` | `AssetDetailOut` | 404 unknown asset |
| GET | `/priorities` | `source`, `as_of_date`, `priority`, `page`, `page_size` | `PriorityPage` | 422 unknown priority |
| GET | `/data-quality/runs` | `source`, `limit` | `list[RunOut]` | — |
| GET | `/data-quality/issues` | `source`, `run_id` | `list[IssueOut]` | 404 unknown run |

Rules:
- Every SQL call uses `%(name)s` parameters. No f-string SQL. Ever.
- `page_size` is clamped by Pydantic (`le=200`), not by hand.
- Priority is computed in **Python** (`domain.priority.decide`) from SQL-fetched rows, so
  there is exactly one implementation of the rules.
- Responses never include DB credentials, file system paths, or raw stack traces.
- `/data-quality/issues` returns counts + one example per reason code; it must **not**
  dump full rejected rows (they may contain unreviewed data).

### 7.5 `tests/test_api.py` must cover

```text
# happy paths
GET /health                                  -> 200, status ok
GET /metrics?source=original                 -> 200, currently_under_repair == known count
GET /metrics?source=original                 -> warnings contains CONSTANT_DUE_DATE
GET /assets?source=scenario&page_size=10     -> 200, len(items)==10, meta.total>10
GET /assets/{known_id}?source=scenario       -> 200, reason is a non-empty sentence
GET /priorities?source=scenario&priority=P1_DATA_REVIEW -> all items priority P1

# error paths
GET /assets?page_size=5000                   -> 422
GET /assets?source=nope                      -> 422
GET /assets/DOES_NOT_EXIST                   -> 404, body has code
GET /metrics?as_of_date=not-a-date           -> 422
GET /data-quality/issues?run_id=999999       -> 404
```

### 7.6 Verification

```bash
uvicorn assetops.api.main:app --reload --port 8000
curl -s localhost:8000/health | jq
curl -s "localhost:8000/metrics?source=original&as_of_date=2026-01-15" | jq
curl -s "localhost:8000/priorities?source=scenario&page_size=5" | jq '.items[0]'
open http://localhost:8000/docs
```

### 7.7 GATE 7 — pass criteria

- [ ] `/docs` lists exactly the seven endpoints, each with typed responses.
- [ ] `pytest tests/test_api.py -v` → all happy and error cases pass.
- [ ] `/metrics` for `original` shows `overdue_scheduled_service = 10000` (or whatever the
      real number is) **and** the constant-date warnings — proving the honest behaviour
      required in §11 of the plan.
- [ ] Stopping the DB container makes `/health` return `database:false` with HTTP 200, and
      other endpoints return a typed 503/500 body — not an HTML stack trace.

**STOP. Wait for approval.**

---

# MILESTONE 8 — Tableau-like dashboard (Streamlit + Plotly)

**Hard rule:** the dashboard calls the API. It never opens a database connection and never
re-implements a KPI. If a number is missing, add it to the API first.

### 8.1 `dashboard/api_client.py`

```python
from __future__ import annotations

import os
from datetime import date
from typing import Any

import requests
import streamlit as st

BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
TIMEOUT = 10


class ApiError(RuntimeError):
    pass


def _get(path: str, params: dict[str, Any] | None = None) -> Any:
    try:
        r = requests.get(f"{BASE}{path}", params=params, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise ApiError(f"Cannot reach the AssetOps API at {BASE}: {exc}") from exc
    if r.status_code == 404:
        raise ApiError("Not found")
    if r.status_code >= 400:
        raise ApiError(f"API error {r.status_code}: {r.text[:200]}")
    return r.json()


@st.cache_data(ttl=60)
def health() -> dict:               return _get("/health")
@st.cache_data(ttl=60)
def metrics(source: str, as_of: date) -> dict:
    return _get("/metrics", {"source": source, "as_of_date": as_of.isoformat()})
@st.cache_data(ttl=60)
def assets(**kw) -> dict:           return _get("/assets", kw)
@st.cache_data(ttl=60)
def asset_detail(asset_id: str, source: str, as_of: date) -> dict:
    return _get(f"/assets/{asset_id}", {"source": source, "as_of_date": as_of.isoformat()})
@st.cache_data(ttl=60)
def priorities(**kw) -> dict:       return _get("/priorities", kw)
@st.cache_data(ttl=60)
def runs(source: str) -> list:      return _get("/data-quality/runs", {"source": source})
@st.cache_data(ttl=60)
def issues(source: str) -> list:    return _get("/data-quality/issues", {"source": source})
```

### 8.2 `dashboard/app.py` — structure (implement exactly these sections)

```python
import datetime as dt
import pandas as pd
import plotly.express as px
import streamlit as st

from api_client import ApiError, asset_detail, assets, issues, metrics, priorities, runs

st.set_page_config(page_title="AssetOps — IT Asset Service Planning",
                   page_icon="🗂", layout="wide")

PALETTE = {"OVERDUE": "#c0392b", "DUE_WITHIN_30": "#e08a1e",
           "LATER": "#2d7f5e", "UNKNOWN": "#6b7280", "EXCLUDED": "#b0b6c0"}

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("AssetOps")
    source = st.radio("Dataset", ["original", "scenario"], index=0,
                      format_func=lambda s: {"original": "Original dataset (as supplied)",
                                             "scenario": "Synthetic demonstration data"}[s])
    as_of = st.date_input("Planning date (as_of_date)", value=dt.date.today())
    st.caption("All overdue / due-soon figures are calculated relative to this date.")
    section = st.radio("View", ["Executive overview", "Investigate by segment",
                                "Priority worklist", "Asset detail", "Data quality"])

# ---------------------------------------------------------------- banner (ALWAYS visible)
def banner(m: dict) -> None:
    if source == "original":
        st.warning(
            "**Original dataset (as supplied, unmodified).** "
            "This export contains a single distinct service-due date for every record, so it "
            "cannot rank which asset to service first. Figures below describe a historical "
            "state, not upcoming work. Switch to *Synthetic demonstration data* to see the "
            "full planning workflow.", icon="⚠️")
    else:
        st.info("**Synthetic demonstration data** — generated with seed 42 for demonstration "
                "only. It does not describe any real organisation.", icon="🧪")
    fresh = m.get("data_freshness")
    st.caption(f"Planning date: **{as_of}** · Data last refreshed: "
               f"**{fresh or 'no successful ingestion recorded'}**")
    for w in m.get("warnings", []):
        st.error(f"**{w['code']}** — {w['message']}", icon="🚩")
```

Then implement each section:

**A. Executive overview** — six `st.metric` cards in two rows:
`Active assets`, `Currently under repair` (+ % of active, label must read *“currently under
repair”*), `Overdue scheduled service`, `Due within 30 days`, `Unknown schedule`,
`Maintenance events (90d)` — the last one rendered as `—` with a caption
*“no event history in this dataset”* when the API returns `null`.

**B. Investigate by segment** — filters (location, asset type, status, due category) then
three Plotly charts:
1. `px.bar` assets by type, stacked by due category, colour map `PALETTE`.
2. `px.bar` overdue % by location — with the denominator printed in the subtitle.
3. Due-category donut (`px.pie(hole=0.55)`).
4. **Conditional:** monthly maintenance-event line chart, rendered **only** when
   `source == "scenario"`; otherwise show `st.info("This dataset contains no maintenance
   events, so no trend can be shown.")`

**C. Priority worklist** — `st.dataframe` with columns
`asset_id · asset_type · location · current_status · due_date · days_until_due ·
due_status · priority · Reason · Suggested action`.
Requirements: priority filter, sort by rank then `days_until_due`, CSV download button, and
a row-selection that stores `asset_id` in `st.session_state` and jumps to Asset detail.
Colour must never be the only signal — the `due_status` column shows a text label
(`🔴 OVERDUE`, `🟠 DUE IN 12 DAYS`, `⚪ UNKNOWN`).

**D. Asset detail** — text input or the selected id; shows all stored fields, the priority
decision with its **Reason** sentence verbatim from the API, the source dataset label, and
an event table (or “no events recorded for this dataset”).

**E. Data quality** — last 10 ingestion runs (status, rows read/accepted/rejected,
duration), a bar chart of rejection reason codes, the dataset warnings with the
*“what this means for your decision”* text, and the freshness timestamp.

**Error handling (required):** wrap every section body in
`try: ... except ApiError as e: st.error(f"Could not load this view: {e}"); st.stop()`.
Killing the API container must leave a readable message, not a traceback.

### 8.3 Visual standard checklist

- [ ] One accent colour + the semantic palette above; no rainbow defaults.
- [ ] Every chart title is a question the user asked (§1 target user).
- [ ] Every status conveyed by colour also carries text.
- [ ] Dates are ISO `YYYY-MM-DD` everywhere.
- [ ] Every screenshot shows the dataset-mode banner and `as_of_date`.
- [ ] No chart exists that cannot be tied to an action.

### 8.4 GATE 8 — pass criteria

- [ ] Journey works end to end: overview → filter to Bangalore laptops → open worklist →
      select an asset → read its reason → view data-quality page.
- [ ] Switching dataset mode changes every number **and** the banner.
- [ ] With `source=original`, no screen implies upcoming 2026 work.
- [ ] Dashboard KPI values equal the raw API JSON values (paste both for one date).
- [ ] Screenshots saved to `docs/screenshots/` (5 files, named in §15).

**STOP. Wait for approval.**

---

# MILESTONE 9 — Quality hardening

1. **Edge-case tests** — see §12; specifically add: empty dataset, dataset with only
   decommissioned assets, leap-day `as_of` (2028-02-29), asset with two open schedules
   (must be impossible — assert the unique index raises), and `as_of` far in the past.
2. **Logging** — one structured line per API request (`path`, `status`, `duration_ms`) and
   per ingestion run. No secrets, no full rows.
3. **Security pass** —
   - `grep -rn "f\"SELECT\|f'SELECT\|% (\|+ \" WHERE\"" src/` → must be empty.
   - `git log -p | grep -iE "password|secret|token|api[_-]key"` → must be empty.
   - Confirm `.env` is ignored: `git check-ignore -v .env`.
   - Confirm the API exposes no write verbs: `grep -rn "@router.post\|put\|delete" src/` → empty.
4. **Performance note** — if you report a response time, report the exact command:
   `for i in $(seq 20); do curl -so /dev/null -w "%{time_total}\n" "localhost:8000/priorities?source=scenario&page_size=50"; done | sort -n | awk '{a[NR]=$1} END{print "p50",a[int(NR/2)],"p95",a[int(NR*0.95)]}'`
   Report the median and p95 with the row count and hardware. Never round up into a claim.
5. **Coverage** — `pytest --cov=assetops --cov-report=term-missing`. Report the real number.
   Do not chase a percentage; ensure `domain/`, `ingestion/validation.py` are ≥90%.

**GATE 9:** all four checks pasted verbatim, no unexplained failures.

---

# MILESTONE 10 — Docker Compose and CI

### 10.1 `Dockerfile.api`

```dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir -e ".[dev]"
COPY migrations ./migrations
COPY scripts ./scripts
COPY sql ./sql
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --retries=5 \
  CMD curl -fsS http://localhost:8000/health || exit 1
CMD ["uvicorn", "assetops.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 10.2 `Dockerfile.dashboard`

```dockerfile
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir ".[dashboard]"
COPY dashboard ./dashboard
EXPOSE 8501
HEALTHCHECK --interval=15s --timeout=3s --retries=5 \
  CMD curl -fsS http://localhost:8501/_stcore/health || exit 1
CMD ["streamlit", "run", "dashboard/app.py", \
     "--server.address=0.0.0.0", "--server.port=8501", \
     "--server.headless=true", "--browser.gatherUsageStats=false"]
```

### 10.3 `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports: ["5432:5432"]          # remove this line before any public deployment
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 3s
      retries: 10

  api:
    build: { context: ., dockerfile: Dockerfile.api }
    env_file: .env
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
    depends_on:
      db: { condition: service_healthy }
    ports: ["8000:8000"]
    volumes:
      - ./legacy:/app/legacy:ro
      - ./data:/app/data

  dashboard:
    build: { context: ., dockerfile: Dockerfile.dashboard }
    environment:
      API_BASE_URL: http://api:8000
    depends_on:
      api: { condition: service_healthy }
    ports: ["8501:8501"]

volumes:
  pgdata:
```

> **Never** put migrations or ingestion in the container `CMD`. Data loading is an explicit
> operator command so a restart cannot silently wipe or duplicate a database.

### 10.4 First-run sequence (put this verbatim in README)

```bash
cp .env.example .env            # then edit POSTGRES_PASSWORD
docker compose up -d --build
docker compose exec api python -m scripts.migrate
docker compose exec api assetops generate-scenario --seed 42 --output data/scenario
docker compose exec api assetops ingest --source original --file "legacy/01_IT_ASSESMENT(raw data).xlsx"
docker compose exec api assetops ingest --source scenario --directory data/scenario
# API   -> http://localhost:8000/docs
# Board -> http://localhost:8501
docker compose exec api python scripts/smoke_test.py
```

### 10.5 `scripts/smoke_test.py`

```python
"""Fails loudly if the running stack is not usable. Exit 0 = green."""
from __future__ import annotations
import os, sys, requests

BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
CHECKS = [
    ("health",        "/health",                                      lambda j: j["database"] is True),
    ("metrics orig",  "/metrics?source=original",                     lambda j: j["active_assets"] > 0),
    ("warn present",  "/metrics?source=original",                     lambda j: any(w["code"] == "CONSTANT_DUE_DATE" for w in j["warnings"])),
    ("assets page",   "/assets?source=scenario&page_size=5",          lambda j: len(j["items"]) == 5),
    ("priorities",    "/priorities?source=scenario&page_size=5",      lambda j: all(i["reason"] for i in j["items"])),
    ("runs",          "/data-quality/runs?source=original",           lambda j: len(j) >= 1),
]
fail = 0
for name, path, ok in CHECKS:
    try:
        j = requests.get(BASE + path, timeout=10).json()
        good = ok(j)
    except Exception as exc:                       # noqa: BLE001
        good, j = False, str(exc)
    print(f"{'PASS' if good else 'FAIL'}  {name}")
    fail += 0 if good else 1
sys.exit(1 if fail else 0)
```

### 10.6 `.github/workflows/ci.yml`

```yaml
name: CI
on:
  push: { branches: [main, "m*"] }
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: assetops
          POSTGRES_PASSWORD: ci_password
          POSTGRES_DB: assetops
        ports: ["5432:5432"]
        options: >-
          --health-cmd "pg_isready -U assetops"
          --health-interval 5s --health-timeout 3s --health-retries 10
    env:
      DATABASE_URL: postgresql://assetops:ci_password@localhost:5432/assetops
      TEST_DATABASE_URL: postgresql://assetops:ci_password@localhost:5432/assetops
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11", cache: pip }
      - run: pip install -e ".[dev,dashboard]"
      - name: Lint
        run: |
          ruff check src dashboard tests scripts
          black --check src dashboard tests scripts
      - name: Honesty check (no forecasting language)
        run: |
          ! grep -rniE "\b(forecast|predictive|prediction|failure rate|machine learning)\b" \
              README.md docs src dashboard --include="*.md" --include="*.py" \
            | grep -v "DECISIONS.md" | grep -v "legacy" | grep -v "does not" \
            | grep -v "was renamed"
      - name: Migrate
        run: python -m scripts.migrate
      - name: Tests
        run: pytest --cov=assetops --cov-report=term-missing
      - name: Build images
        run: |
          docker build -f Dockerfile.api -t assetops-api:ci .
          docker build -f Dockerfile.dashboard -t assetops-dash:ci .
```

### 10.7 GATE 10 — pass criteria

- [ ] On a **clean** machine/directory (`docker compose down -v` first), the §10.4
      sequence works verbatim with no manual fixes. Paste the terminal transcript.
- [ ] `docker compose restart` does not change row counts (no silent re-seed).
- [ ] `scripts/smoke_test.py` prints six PASS lines and exits 0.
- [ ] CI is green on GitHub; paste the run URL.

**STOP. Wait for approval.**

---

# MILESTONE 11 — Hosted demo (only if Milestone 10 is green)

1. **Research current options at deployment time** (prices and free tiers change). Compare
   at least three that can host *API + dashboard + persistent Postgres*, e.g. Render,
   Railway, Fly.io, Koyeb, Neon/Supabase (DB) + Streamlit Community Cloud (UI).
2. Present **one recommendation** with: monthly cost at the expected usage, free-tier
   limits, cold-start behaviour, whether the DB persists, and one named alternative.
   **Wait for approval before deploying.**
3. Deployment rules:
   - Remove the `ports: 5432` mapping; the database must not be reachable publicly.
   - Environment variables set in the host's secret store, never in the repo.
   - Public demo uses **scenario mode by default**. Only expose the original dataset if
     Milestone 2 confirmed redistribution rights.
   - Run migrations as an explicit release step, not on container boot.
   - After deploying, run `scripts/smoke_test.py` against the public URL and paste output.
4. Wording rule: if only Compose works, the README says **“deployment-ready (Docker
   Compose)”**. The word **“deployed”** may only appear next to a URL you have loaded in a
   browser and smoke-tested.

**GATE 11:** URL + smoke-test output + a statement of what data is exposed and why that is
permitted.

---

# MILESTONE 12 — Portfolio packaging

### 12.1 Artefacts

| Artefact | Where | Notes |
|---|---|---|
| Architecture diagram | `docs/ARCHITECTURE.md` (Mermaid) + PNG | must match what is built |
| 5 screenshots | `docs/screenshots/` | `01-overview.png`, `02-segments.png`, `03-worklist.png`, `04-asset-detail.png`, `05-data-quality.png` — each showing the banner and as_of_date |
| 60–90 s screen recording | link in README | one full journey, no narration needed |
| CI badge | README top | links to the real workflow |
| Demo URL | README | only if Milestone 11 passed |

### 12.2 Resume bullets (only these claims are supported by this build)

> **AssetOps — IT Asset Service Planning** · *Python · PostgreSQL · FastAPI · Streamlit · Docker · GitHub Actions*
>
> * Audited an inherited 10,000-record IT asset dataset and found its two service-date
>   columns each held a **single distinct value**, making the existing “due in 30 days”
>   KPI and the project's forecasting claim unsupportable; rebuilt the project around
>   validated, explicitly-defined service-planning metrics instead.
> * Built an ingestion CLI with row-level validation (9 rejection codes) and
>   dataset-level anomaly warnings, recording every run's read/accepted/rejected counts;
>   re-ingesting the same file is idempotent via `ON CONFLICT` upserts.
> * Modelled a 5-table PostgreSQL schema with foreign keys, check constraints and a
>   partial unique index enforcing one open schedule per asset; exposed it through a typed,
>   read-only FastAPI service with pagination and parameterised SQL.
> * Delivered a Streamlit + Plotly decision dashboard whose priority worklist shows a
>   plain-English **reason** for every listed asset, plus a data-quality view that tells the
>   user when the data cannot support a decision; whole stack runs from one
>   `docker compose up`, with tests and linting enforced in GitHub Actions.

**Do not add:** downtime reduction, cost savings, accuracy, or any percentage improvement.
None of those are measurable from this data.

### 12.3 Interview talking points

- *“The first deliverable was a retraction.”* — explaining why you renamed the project.
- *“One definition, two implementations, one test.”* — the SQL/Python parity test.
- *“The dashboard's job is sometimes to say ‘you cannot decide from this data’.”*
- *“No ML here on purpose: there is no target variable and no event history. Adding a model
  would have been decoration.”*

**GATE 12:** every row of §16's claim-to-proof matrix has a link to real evidence.

---

# 12-A. Test specification (full list)

### 12.1 `tests/test_due_status.py` — boundaries (all must exist)

| as_of | due_date | expected |
|---|---|---|
| 2026-01-15 | 2026-01-14 | OVERDUE |
| 2026-01-15 | 2026-01-15 | DUE_WITHIN_30 |
| 2026-01-15 | 2026-02-14 (+30) | DUE_WITHIN_30 |
| 2026-01-15 | 2026-02-15 (+31) | LATER |
| 2026-01-15 | None | UNKNOWN |
| 2028-02-29 | 2028-03-30 (+30) | DUE_WITHIN_30 |
| 2026-01-31 | 2026-03-02 (+30, month rollover) | DUE_WITHIN_30 |
| 2020-01-01 | 2026-01-01 | LATER |

Also: `days_until_due` is negative for overdue, 0 on the day, `None` when unknown, and
`classify` is total (property test: any date returns exactly one category).

### 12.2 `tests/test_priority.py`

| status | due | expected priority |
|---|---|---|
| Working | None | P1_DATA_REVIEW |
| Under Repair | None | P1_DATA_REVIEW (data review outranks operational) |
| Under Repair | overdue | P2_URGENT_OPERATIONAL |
| Working | overdue | P3_OVERDUE |
| Working | today | P4_DUE_SOON |
| Working | +30 | P4_DUE_SOON |
| Working | +31 | P5_NO_ACTION |
| Decommissioned | overdue | EXCLUDED |

Plus: reason text contains the day count; `rank` ordering is strictly increasing P1→P5;
`decide()` is pure (same inputs → identical dataclass).

### 12.3 `tests/test_validation.py`
One test per rejection code: `MISSING_ASSET_ID`, `DUPLICATE_ASSET_ID`, `UNKNOWN_ASSET_TYPE`,
`UNKNOWN_LOCATION`, `UNKNOWN_STATUS`, `UNPARSEABLE_DATE`, `FUTURE_PURCHASE_DATE`,
`DUE_BEFORE_LAST_SERVICE`. Plus: valid rows survive untouched; warnings fire at exactly
90% dominance and not at 89%; `ALL_DATES_IN_PAST` fires only when *every* due date is past.

### 12.4 `tests/test_excel_reader.py`
Missing file → `FileNotFoundError`; renamed column → `SchemaMismatch` naming the column;
happy path on a 5-row fixture xlsx in `tests/fixtures/`.

### 12.5 `tests/test_ingestion_db.py` (marked `db`)
- ingest fixture → counts land in `ingestion_runs`;
- **re-ingest the same fixture → asset count unchanged, one extra run row, old schedule
  closed, exactly one open schedule**;
- a row that violates a DB constraint aborts the whole transaction (no partial rows);
- rejected rows are written with reason codes;
- events are deduplicated on re-ingest.

### 12.6 `tests/conftest.py` essentials

```python
import os
import pytest
import psycopg
from psycopg.rows import dict_row

DSN = os.getenv("TEST_DATABASE_URL", "postgresql://assetops:change_me_locally@localhost:5432/assetops")


@pytest.fixture(scope="session")
def db_conn():
    with psycopg.connect(DSN, row_factory=dict_row, autocommit=True) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_test_rows(db_conn, request):
    if "db" not in request.keywords:
        yield; return
    db_conn.execute("DELETE FROM assets WHERE source_dataset='test'")
    db_conn.execute("DELETE FROM ingestion_runs WHERE source_dataset='test'")
    yield
    db_conn.execute("DELETE FROM assets WHERE source_dataset='test'")
```

Run DB tests only when a database exists: `pytest -m "not db"` must also pass offline.

---

# 13. Troubleshooting (pre-empted failures)

| Symptom | Cause | Fix |
|---|---|---|
| `psycopg.OperationalError: connection refused` | API started before DB was ready | `depends_on: condition: service_healthy` is already in the compose file; check `docker compose ps` health |
| `relation "assets" does not exist` | migrations not run | `docker compose exec api python -m scripts.migrate` |
| `ModuleNotFoundError: assetops` | package not installed in editable mode | `pip install -e .` from repo root; ensure `src/` layout + `[tool.setuptools.packages.find] where=["src"]` |
| Dashboard shows "Cannot reach the AssetOps API" | dashboard pointed at `localhost` inside a container | `API_BASE_URL=http://api:8000` (service name, not localhost) |
| `purchase_not_future` violation on ingest | a row has a future purchase date | it should have been rejected by validation first — check the validator ran before `persist` |
| `duplicate key value violates unique constraint "uq_open_schedule_per_asset"` | schedule inserted without closing the old one | `CLOSE_OPEN_SCHEDULES` must run inside the same transaction, before `INSERT_SCHEDULE` |
| Excel dates read as `Timestamp` not `date` | pandas | `parse_date()` already handles `datetime`; do not cast with `str()` first |
| `pytest` DB tests fail in CI but pass locally | different DSN | CI sets `TEST_DATABASE_URL`; conftest must read it |
| Streamlit shows stale numbers | `st.cache_data` TTL | press "Rerun" or lower TTL; note caching in the README |
| CI honesty grep fails on a legitimate sentence | the word appears in an explanation | keep explanations in `docs/DECISIONS.md` / `legacy/`, which the grep excludes |

---

# 14. Claim-to-proof matrix (fill the Evidence column with real links)

| Claim in README | Required proof | Evidence |
|---|---|---|
| Validated ingestion | command + run row + rejected example + rerun test | |
| Data-quality monitoring | `/data-quality/runs` JSON + screenshot | |
| Relational database with integrity | migration file + failing constraint output + ER diagram | |
| Meaningful SQL | `sql/analytical_queries.sql` + parity test | |
| Explainable prioritisation | `docs/METRICS.md` §6 + `test_priority.py` + worklist screenshot | |
| Read-only API | `/docs` screenshot + `test_api.py` results | |
| Interactive dashboard | 5 screenshots + recording | |
| Deployment-ready | clean-machine transcript of §10.4 | |
| Deployed | live URL + smoke-test output | |
| Idempotent re-ingestion | two counts, before and after | |
| *Anything about downtime, savings, accuracy, forecasting* | **NOT CLAIMABLE — omit** | — |

---

# Appendix A — `README.md` skeleton (fill, do not embellish)

```markdown
# AssetOps — IT Asset Service Planning

[![CI](badge-url)](workflow-url)

A database-backed application that validates IT asset records, tracks service schedules,
and gives IT operations an explainable queue of assets and data-quality issues to review.

> AssetOps does not forecast failures. Every figure it shows is a rule-based calculation
> over recorded dates, defined in [docs/METRICS.md](docs/METRICS.md).

## The problem
An IT operations lead needs to answer six questions ... (list them)

## What this repository was before
v1 was titled "IT Asset Maintenance Forecasting" ... (state the four findings honestly,
link legacy/README.md)

## Data
| Mode | What it is | Contains events |
|---|---|---|
| original | the supplied 10,000-row export, unmodified | no |
| scenario | generated demonstration data, seed 42 | yes |
Provenance and generation rules: docs/DATA-PROVENANCE.md

## Architecture
(Mermaid diagram) — details in docs/ARCHITECTURE.md

## Quickstart
(the exact §10.4 block)

## Tests
`pytest` / `pytest -m "not db"` — what each suite covers

## Screenshots
(5 images)

## What I verified vs. what I did not
(bulleted, honest)

## Limitations
- the original dataset cannot rank service priority (single distinct due date)
- scenario data is synthetic and describes no real organisation
- no outcome data exists, so no downtime or cost impact is claimed
```

# Appendix B — ADR template for `docs/DECISIONS.md`

```markdown
## ADR-00X: <decision>
- **Date:**
- **Status:** accepted | superseded by ADR-00Y
- **Context:** what forced a choice
- **Options considered:** A / B / C with one line each
- **Decision:**
- **Consequences:** what becomes easy, what becomes hard, what we gave up
```

Minimum ADRs required: rename & removal of forecasting claims · no ML · PostgreSQL over
SQLite · plain SQL migrations over Alembic · Streamlit over Tableau Public for the new UI ·
composite key `(source_dataset, asset_id)` · storing only the current schedule ·
computing `days_until_due` at query time.

# Appendix C — Milestone tracker (agent updates this table in the README)

| # | Milestone | Status | Approved by human | Date |
|---|---|---|---|---|
| 0 | Re-audit | ☐ | ☐ | |
| 1 | Correct claims | ☐ | ☐ | |
| 2 | Contracts | ☐ | ☐ | |
| 3 | Data strategy | ☐ | ☐ | |
| 4 | Database | ☐ | ☐ | |
| 5 | Ingestion | ☐ | ☐ | |
| 6 | Domain + SQL | ☐ | ☐ | |
| 7 | API | ☐ | ☐ | |
| 8 | Dashboard | ☐ | ☐ | |
| 9 | Hardening | ☐ | ☐ | |
| 10 | Compose + CI | ☐ | ☐ | |
| 11 | Hosted demo | ☐ | ☐ | |
| 12 | Packaging | ☐ | ☐ | |

**End of specification.** An agent that reaches the end of a milestone must produce the
§0.3 report and stop. It may not begin the next milestone without written approval.
