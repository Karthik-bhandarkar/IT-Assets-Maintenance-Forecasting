# Handoff — what is done, what Antigravity must do

**Date:** 2026-09-29 · **Owner:** Swati · **Spec:** `ASSETOPS_BUILD_PLAN.md`

---

## PART 1 — What is already done (by me, in this workspace)

| # | Item | Path | Status |
|---|---|---|---|
| 1 | Audited the real GitHub repo (cloned, opened the xlsx, the SQL, the README) | `/home/user/repo/` | Done |
| 2 | Confirmed the two killer data facts: `LastServiceDate` and `NextServiceDue` each have **1 distinct value** across 10,000 rows; status mix 84.70 / 10.28 / 5.02 | — | Verified with pandas |
| 3 | **Complete implementation specification** — 2,655 lines, 12 milestones, full file contents for ~25 files | `AssetOps-Plan/ASSETOPS_BUILD_PLAN.md` | Done |
| 4 | **Copy-paste prompts** for Antigravity, one per milestone + drift correction | `AssetOps-Plan/PASTE_TO_ANTIGRAVITY.md` | Done |
| 5 | Validated every code block in the spec (21 Python blocks parse, TOML + 2 YAML parse, 98 fences balanced) | — | Done |
| 6 | Earlier ML experiment (superseded, do **not** merge into AssetOps) | `/home/user/assetpulse/` | Archived |

### What the spec already contains, written out in full (Antigravity does not have to invent these)

- `docs/METRICS.md` — every KPI, the 4 due categories, every date boundary, the 6 priority rules with their exact user-facing sentences
- `migrations/0001_initial_schema.sql` + `0002_indexes.sql` — 5 tables, FKs, check constraints, partial unique index
- `scripts/migrate.py`, `scripts/smoke_test.py`
- `src/assetops/config.py`, `scenario/generate.py`, `ingestion/validation.py`, `ingestion/excel_reader.py`, `ingestion/loader.py`, `cli.py`, `domain/due_status.py`, `domain/priority.py`, `database/connection.py`, `api/schemas.py`, `api/main.py`, `api/deps.py`
- `sql/analytical_queries.sql` — 8 parameterised queries
- `dashboard/api_client.py` + full dashboard section spec
- `pyproject.toml`, `.env.example`, `.gitignore`, `Dockerfile.api`, `Dockerfile.dashboard`, `docker-compose.yml`, `.github/workflows/ci.yml`
- Full test matrix (every boundary row), troubleshooting table, README skeleton, ADR list

---

## PART 2 — What YOU must do before starting Antigravity (15 minutes)

1. **Install:** Docker Desktop, Python 3.11, Git. (WSL2 Ubuntu if on Windows.)
2. **Clone the repo** and copy both plan files into its root:
   ```bash
   git clone https://github.com/Swati-Devas/IT-Assets-Maintenance-Forecasting.git AssetOps
   cd AssetOps
   # copy ASSETOPS_BUILD_PLAN.md and PASTE_TO_ANTIGRAVITY.md here
   git checkout -b assetops-rebuild
   ```
3. **Open the folder in Antigravity**, select its strongest available model.
4. Decide one thing in advance (Milestone 2 will ask you): **do you know where the
   original spreadsheet came from?** If not, the answer in `docs/DATA-PROVENANCE.md` is
   *"origin undocumented; redistribution rights unverified"* — which is fine and honest.

---

## PART 3 — What Antigravity must do (12 milestones, one at a time)

Paste the **session opener** from `PASTE_TO_ANTIGRAVITY.md`, then one milestone prompt at a
time. After each, check the GATE in the spec before sending the next prompt.

| M | What it does | Est. time | Your job at the gate |
|---|---|---|---|
| **0** | Re-audit the repo. **Zero file edits.** | 20 min | Check it reports F1–F7 with real values + the workbook SHA-256 |
| **1** | Rename/reframe: move 6 files into `legacy/`, honest README, kill all forecasting language | 40 min | Confirm the SHA-256 is unchanged and the vocabulary grep returns nothing |
| **2** | Write `docs/METRICS.md` + `DATA-PROVENANCE.md`. Docs only. | 30 min | **You must approve the rules** (eligibility, 30-day inclusive boundary, priority order) |
| **3** | `pyproject.toml`, config, deterministic scenario generator, 3 tests | 45 min | `pytest tests/test_scenario.py` → 3 passed |
| **4** | PostgreSQL schema + migration runner + ER diagram | 45 min | Migration runs twice (2nd = all "skip"); 4 constraint violations fail with real errors |
| **5** | Ingestion CLI, validation (8 reject codes), dataset warnings, safe reruns | 1.5 h | Double-ingest → asset count **unchanged**; constant-date warnings fire |
| **6** | `due_status.py`, `priority.py`, 8 SQL queries, **SQL↔Python parity test** | 1.5 h | All boundary tests pass (D=A, D=A+30, D=A+31, leap day) |
| **7** | 7 read-only FastAPI endpoints, typed schemas, error handling | 2 h | `/docs` works; every error case returns a typed body, not a stack trace |
| **8** | Streamlit + Plotly dashboard, 5 sections, explainable worklist | 3 h | Dashboard numbers == API JSON; original mode never implies future work; 5 screenshots saved |
| **9** | Edge cases, logging, 4 security greps, real coverage | 1 h | Security greps empty; no invented performance numbers |
| **10** | Dockerfiles, compose, smoke test, GitHub Actions CI | 1.5 h | `docker compose down -v` then the 6-command quickstart works **verbatim**; CI green |
| **11** | Research hosting → recommend ONE → deploy only after your approval | 1 h | Do not let it deploy before showing costs/limits |
| **12** | README, diagrams, screenshots, claim-to-proof matrix, resume bullets | 1 h | Every claim links to real evidence; delete anything that doesn't |

**Realistic total: 15–18 hours of agent work spread over 3–5 sessions.** Do not try to do
it in one sitting; the gates are the whole point.

---

## PART 4 — The 6 rules you must enforce on the agent

1. **One milestone per prompt.** If it starts Milestone 5 while you approved 4, stop it.
2. **No "done, everything works."** Demand the §0.3 report format: files changed, verbatim
   commands with exit codes, verbatim test output, and *what it did not verify*.
3. **No forecasting words.** `forecast`, `predict`, `risk score`, `failure rate`, `ML`, `AI`
   describing AssetOps behaviour = instant rejection.
4. **No invented numbers.** No downtime saved, no cost saved, no accuracy, no response
   time it didn't measure with the exact command in §9.
5. **Nothing deleted.** Legacy files move with `git mv`, never `rm`.
6. **No new technology** without asking you (no Kafka, no Kubernetes, no ORM swap, no LLM).

---

## PART 5 — What "finished" looks like

A stranger clones the repo and runs:

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec api python -m scripts.migrate
docker compose exec api assetops generate-scenario --seed 42 --output data/scenario
docker compose exec api assetops ingest --source original --file "legacy/01_IT_ASSESMENT(raw data).xlsx"
docker compose exec api assetops ingest --source scenario --directory data/scenario
docker compose exec api python scripts/smoke_test.py    # 6 PASS lines
```

…and gets a working API at `:8000/docs` and a dashboard at `:8501` that shows an
explainable service queue and honestly says when the data can't support a decision.

---

## PART 6 — Open questions for me (ask when you're ready)

- Convert all 13 GATEs into an exact command-by-command verification checklist with
  pass/fail criteria and required screenshots (you said you'd send this procedure).
- Tailor the Milestone 12 resume bullets to a specific job description.
- Review Antigravity's Milestone 0 audit output against what I found, so you can catch it
  if it fabricates a finding.
