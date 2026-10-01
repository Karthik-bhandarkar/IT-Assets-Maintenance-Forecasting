# Paste-ready README block (3 dashboards)

Put the three PNGs in `docs/screenshots/` and the two scripts in `scripts/`, then paste
the block below into your repository `README.md`.

---

```markdown
## Dashboards

### 1 · Fleet overview

![Fleet overview](docs/screenshots/dashboard_fleet_overview.png)

KPI row, hardware mix, volume by delivery centre, status mix per site, procurement
profile — and a data-quality panel that states what these figures *cannot* answer.
Every number is computed from the register at render time by
[`scripts/make_dashboard.py`](scripts/make_dashboard.py).

### 2 · Service priority worklist

![Service priority worklist](docs/screenshots/dashboard_priority_worklist.png)

The operational view: a rule-based review queue where **every row states the rule that
put it there** — P1 missing schedule, P2 overdue *and* under repair, P3 overdue, P4 due
within 30 days. No score, no model, no black box. Runs on the seeded synthetic scenario
(labelled on the canvas) because the original register has no per-asset due dates.

### 3 · Data quality & ingestion monitor

![Data quality and ingestion monitor](docs/screenshots/dashboard_data_quality.png)

Validation results for the original register (5 checks pass, both service-schedule checks
warn), rejection reasons from the scenario load, the full ingestion run history including
a failed run, and an explicit list of which figures are **publishable** and which are
**blocked** by the data quality issues.

<sub>Dashboards 1 is rendered from the real register; 2 and 3 use the seeded scenario
dataset where the original data cannot support the view, and say so on the canvas.
Reproduce: `python scripts/make_dashboard.py` and `python scripts/make_dashboards_2_3.py`.</sub>
```

---

## Quick table for your own reference

| Image | Data behind it | Safe as README proof |
|---|---|---|
| `dashboard_fleet_overview.png` | the real 10,000-row register | yes |
| `dashboard_priority_worklist.png` | seeded scenario (labelled on canvas) | yes |
| `dashboard_data_quality.png` | real audit results + scenario run | yes |
| `tableau_dashboard_mockup.png` | AI-generated imagery | **no** — concept slides only |
