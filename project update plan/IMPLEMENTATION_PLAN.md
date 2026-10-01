# IT Hardware Reliability Analytics — Implementation Plan

**Status:** Proposed. No Backblaze dataset, analytical result, dashboard, or deployment is considered verified merely because it appears in this plan.

**Repository:** Existing `IT-Assets-Maintenance-Forecasting` repository  
**Primary target roles:** Data Analyst, BI Analyst, Junior Data Analyst, Analytics Engineer  
**Project priority:** Business question → data quality → SQL → Python analysis → defensible findings → dashboard → recommendations → reproducibility

---

## 1. Project objective

Upgrade the existing repository into a **data-analytics-first hardware reliability case study**.

### Proposed analytical question

> How does observed hard-drive failure incidence differ across drive models and observation periods, after accounting for observed drive-time and data coverage?

### Secondary question

> Which available drive-health indicators merit further investigation, considering their timing, missingness, and differences between drive models?

### Conditional question

> At a fixed review capacity, can an evaluated health-signal ranking identify more *subsequent observed failures* than a justified simple baseline?

The conditional question must be dropped if the approved data cannot support a credible future-outcome evaluation.

### Intended audience

A hardware operations or reliability analyst evaluating fleet-level patterns and deciding which models or signals deserve closer investigation.

This project **does not claim** to operate Backblaze's fleet, prevent failures, reduce downtime, or make replacement decisions for an actual organization.

---

## 2. Existing repository: starting evidence and limitations

A previous agent reported the following. **Recheck these findings against the files before editing anything.**

- The original Excel inventory has approximately 10,000 asset records.
- `LastServiceDate` reportedly has one distinct value across all records.
- `NextServiceDue` reportedly has one distinct value across all records.
- The notebook's `DaysUntilDue < 30` logic includes overdue records.
- `Under Repair / all assets` is described as a failure rate, although it measures a current status share.
- The existing Tableau workbook reportedly uses an Excel extract, not a live SQL Server connection.
- No evaluated failure-forecasting model was found.
- The origin and redistribution rights of the original spreadsheet are undocumented.

### Treatment of original work

1. Preserve original files and their contents.
2. Document what the original dataset can and cannot support.
3. Do not describe the original project as a validated failure-forecasting system.
4. Do not join original asset IDs to Backblaze drive IDs.
5. Do not imply both datasets describe the same fleet.
6. Before moving original artifacts, record filenames and SHA-256 hashes.
7. Investigate redistribution rights before republishing the original spreadsheet elsewhere. Moving a file within the same public repository does **not** remove it from Git history.

The original work becomes a short, honest **legacy data-quality case study** explaining why the analytical question and primary dataset changed.

---

## 3. Dataset selection: mandatory feasibility gate

### Preferred candidate

Backblaze Drive Stats, with the **original publisher** used as the provenance authority:

https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data

A Kaggle mirror is acceptable only if its **exact listing URL**, attribution, covered period, completeness, and usage terms are checked. Do not assume that appearing on Kaggle establishes the dataset's origin, quality, or redistribution permission.

### Do not approve the dataset until the agent reports

| Item | Required evidence |
|---|---|
| Source | Exact publisher page and file URLs |
| Usage | What the published terms actually say; unresolved rights clearly marked unknown |
| Files | Exact filenames, periods, download sizes, and checksums where available |
| Grain | What one row represents, verified against documentation and inspected files |
| Identifier | Drive identifier and whether it is stable within the selected files |
| Outcome | Publisher-documented meaning and timing of the failure indicator |
| Time coverage | Actual minimum/maximum dates and missing dates in inspected files |
| Variation | Unique drives, models, failures, and observation counts |
| Quality | Duplicate drive-date rows, invalid values, missingness by model and period |
| SMART fields | Which candidate fields are sufficiently populated and comparable |
| Resources | Approximate download, disk, memory, and runtime requirements |
| Reproduction | Commands needed to obtain and inspect exactly the proposed files |

### Subset-selection rules

- Choose a **documented contiguous time window** appropriate to the question.
- Do not take a random sample of individual drive-day rows for longitudinal analysis.
- If selecting models or drives to reduce size, specify the selection rule **before examining comparative results**.
- Retain the full available observation sequence for selected drives within the approved window.
- Record all exclusions and their effects on counts.
- Prefer a subset a reviewer can reproduce on an ordinary laptop.

### Feasibility decision

The agent must recommend **approve, revise, or reject** Backblaze as the primary source.

If rejected, propose alternatives with provenance and feasibility evidence. **Do not automatically pivot to another dataset or write application code.**

---

## 4. Analytical contract

Create `docs/ANALYTICAL-QUESTION.md` and `docs/METRICS.md` **before producing findings or dashboard charts**.

The contract must define:

- Observation window.
- Source files.
- Population and exclusions.
- Grain of raw observations.
- Drive identifier.
- Definition of an observed failure.
- Exposure/denominator calculation.
- Treatment of duplicate observations.
- Treatment of drives disappearing without a recorded failure.
- Treatment of drives already present at the start of the selected window.
- Treatment of drives still observed at the end of the window.
- Minimum cohort size for displayed comparisons.
- Date and timezone conventions where applicable.
- Whether comparisons are descriptive, exploratory, or evaluated forward-looking claims.

### Candidate metrics — finalize after inspecting data

| Metric | Proposed interpretation | Required caution |
|---|---|---|
| Distinct observed drives | Unique included drive identifiers | Does not imply equal observation duration |
| Observed drive-days | Eligible, deduplicated drive-date observations | Coverage gaps affect exposure estimates |
| Recorded failures | Publisher-defined failure indicators in eligible records | Disappearance is not automatically failure |
| Observed failures per drive-time | Failures divided by defined observed exposure | Not an unconditional future failure probability |
| Model-level comparison | Failure count, exposure, and rate together | Small cohorts can produce unstable rankings |
| SMART coverage | Usable observations per field, model, and period | Fields may not be comparable across models |

**Important:** A count of drive-day rows is only a valid exposure measure under documented assumptions. Investigate missing observation days, duplicate drive-date rows, and observation-window boundaries. State the limitations of the chosen denominator.

Do not call a model difference a causal effect. Do not claim a drive's actual age based solely on its first appearance in the selected dataset.

---

## 5. Analysis workflow

```text
Original publisher and documented source files
                    ↓
File manifest and reproducible download
                    ↓
Raw-data profiling
                    ↓
Validation and exclusion log
                    ↓
Approved analytical cohort
                    ↓
SQL metrics and cohort comparisons
                    ↓
Python EDA and sensitivity checks
                    ↓
Findings with limitations
                    ↓
Interactive BI dashboard
                    ↓
Cautious investigation recommendations
```

### Data-quality questions

- Are there duplicate drive-date observations?
- Are dates and failure indicators valid?
- Is observation coverage continuous enough for the proposed metrics?
- How does model mix change across the chosen period?
- Which SMART fields are missing by model and date?
- Are fields comparable across models, or are units/definitions model-dependent?
- How many records are excluded, and why?
- Does a conclusion change materially under a reasonable alternative cohort definition?

Report **actual counts**, not a generic statement that the data was cleaned.

### SQL questions

Every substantial SQL query must state the business question it answers. Appropriate queries may investigate:

1. Row and identifier validity.
2. Duplicate drive-date observations.
3. Fleet composition over time.
4. Observation exposure by model and period.
5. Recorded failures alongside their denominators.
6. Missing SMART coverage by model and period.
7. Pre-failure observed history, if timing permits.
8. Sensitivity to cohort restrictions.

Use joins, CTEs, conditional aggregation, and window functions where they serve these questions. Do not add SQL syntax merely to make a skills list longer.

### Python questions

Use Python for profiling, focused EDA, distributions, uncertainty where justified, visual investigation, and sensitivity analyses.

SQL and Python must use **the same approved definitions** for shared metrics. Validate critical figures with hand-checked fixtures.

---

## 6. Statistical and interpretation rules

- Show failure counts and exposure beside any rate.
- Flag or suppress unstable small-cohort comparisons according to a documented threshold.
- Distinguish **association** from **cause**.
- Examine whether a model comparison changes when the observation period or cohort rule changes.
- Discuss incomplete follow-up and drives disappearing without a recorded failure.
- Avoid decorative hypothesis tests or confidence intervals without a clear estimand and assumptions.
- Never turn an exploratory SMART-field difference into a claim that the field predicts failure.

### Conditional review-queue evaluation

Only implement after core descriptive analysis and a separate approval.

Required design:

1. Explicit decision date and future outcome window.
2. Features available no later than the decision date.
3. Defined eligibility and enough follow-up to observe the outcome.
4. Earlier-period development and later-period evaluation.
5. Appropriate baseline; use age only if age is defensibly available.
6. Same fixed review capacity for baseline and candidate.
7. Actual failures identified, missed failures, and false positives reported.
8. Missingness, model coverage, and leakage checks documented.

If these requirements cannot be satisfied, **omit the review queue**.

---

## 7. Dashboard specification

The dashboard is the main visible deliverable. It should look and function like a professional BI analysis, not a general-purpose CRUD application.

Choose Tableau, Power BI, or a lightweight interactive web dashboard **after** the source and deployment feasibility decisions. Do not maintain two inconsistent dashboards.

### Required story

| Section | Question answered | Evidence displayed |
|---|---|---|
| Data confidence | What data am I looking at, and how complete is it? | Publisher, source period, last build date, included cohort, quality notes |
| Fleet overview | What was observed? | Drives, observed drive-time, recorded failures, model mix |
| Cohort comparison | Which models or periods differ? | Counts, exposure, rates, small-cohort cautions |
| Signal investigation | Which health fields merit investigation? | Coverage and appropriately timed comparisons |
| Findings | What should a stakeholder investigate next? | Finding, evidence, interpretation, limitation, recommendation |
| Optional evaluation | Does a review ranking outperform a baseline? | Capacity-matched results, only if methodologically approved |

Dashboard requirements:

- Display source and observation dates prominently.
- Give every rate a visible denominator or accessible definition.
- Apply useful model/time filters consistently.
- Make low-coverage warnings visible.
- Do not represent a historical public-data extract as live fleet monitoring.
- Do not create trend, signal, or evaluation charts without the underlying data.
- Prefer three excellent sections/pages over five weak ones.

---

## 8. Deployment and reproducibility

### Preferred low-cost pattern

```text
Documented public source files
→ reproducible local ingestion
→ SQL and Python analysis
→ versioned dashboard aggregates/extract
→ hosted interactive dashboard
```

A hosted database or API is **optional**. Add one only if it materially improves the analytical workflow. A large raw drive-day dataset does not need to live in a continuously running public database to prove analytical skill.

### Local proof

A reviewer should be able to:

1. Obtain the approved source files using documented instructions.
2. Run profiling and validation.
3. Build the approved cohort and SQL tables/views.
4. Reproduce key numbers in `docs/FINDINGS.md`.
5. Generate the dashboard extract.
6. Run the dashboard locally.

If the full download is substantial, provide an honestly labeled smaller reproducibility path and document how the published full-subset figures were generated. Do not imply a sample reproduces full-subset results if it does not.

### Public-demo proof

Only call the dashboard **deployed** after testing the actual URL. Display:

- Source.
- Observation window.
- Extract generation date.
- Included population.
- Methodology link.

If hosting is not feasible, provide a runnable local dashboard and screen recording; call it **deployment-ready**, not deployed.

---

## 9. Repository structure

This is a target structure. Create folders only when they contain real work.

```text
IT-Assets-Maintenance-Forecasting/
├── README.md
├── IMPLEMENTATION_PLAN.md
├── legacy/
│   └── README.md
├── data/
│   ├── README.md
│   ├── manifests/
│   └── samples/
├── sql/
│   ├── 01_quality.sql
│   ├── 02_cohorts.sql
│   ├── 03_reliability.sql
│   └── 04_dashboard_metrics.sql
├── notebooks/
│   ├── 01_profile.ipynb
│   ├── 02_eda.ipynb
│   └── 03_investigation.ipynb
├── src/
│   └── hardware_reliability/
│       ├── ingest.py
│       ├── validate.py
│       ├── cohorts.py
│       └── analysis.py
├── dashboard/
├── tests/
├── docs/
│   ├── DATA-PROVENANCE.md
│   ├── ANALYTICAL-QUESTION.md
│   ├── DATA-QUALITY.md
│   ├── METRICS.md
│   ├── METHODOLOGY.md
│   ├── FINDINGS.md
│   ├── LIMITATIONS.md
│   ├── DEPLOYMENT.md
│   └── proof-of-work/
├── .github/workflows/
└── pyproject.toml
```

### Legacy handling

Preserve original workbook, notebook, SQL script, Tableau file, spreadsheet, and PDF unless a separately approved rights/security issue requires a different action.

Before moving files:

- List every proposed move.
- Record each file's SHA-256.
- Obtain approval.
- Prefer `git mv`.
- Verify hashes after moving.

---

## 10. Documentation and analytical proof

### Root README: analyst-first order

1. Business question.
2. Executive summary with **only measured, verified findings**.
3. Data source and observation window.
4. Population and methodology.
5. Key SQL/Python analysis.
6. Dashboard screenshot and demo.
7. Recommendations and limitations.
8. Reproduction instructions.
9. Brief explanation of the original project's audit and evolution.
10. Supporting technical architecture.

Do not lead with Docker, API design, or an extended tech-stack table.

### Findings format

For each important finding:

```text
Finding:
Exact observed result.

Evidence:
Source files, inclusion rules, query/notebook, and calculated values.

Interpretation:
What the result may mean.

Limitation:
What cannot be concluded.

Recommended investigation:
A reasonable next step—not a fabricated operational impact.
```

### Claim-to-proof table

| Public claim | Required proof |
|---|---|
| Analyzed real drive observations | Publisher attribution, exact files, dates, population |
| Validated data | Actual quality counts, validation rules, exclusions |
| Wrote meaningful SQL | Question-led queries and reproducible outputs |
| Compared reliability | Failure counts, exposure, definitions, caveats |
| Investigated SMART signals | Timing, missingness, model coverage, limitations |
| Built a dashboard | Tested demo or runnable instructions and real screenshots |
| Evaluated a review strategy | Approved future-window design, baseline, later-period results |
| Reduced downtime or cost | Do **not** claim without measured intervention outcomes |

### Cold-email package

The final portfolio should make it easy to send:

- One GitHub link.
- One dashboard/demo link if live.
- A one-page findings summary.
- One specific, reproducible analytical observation.
- A short explanation of its limitation.

Write resume bullets and cold emails **after findings are verified**.

---

## 11. Implementation milestones

**Work one milestone at a time. Stop for owner approval after every milestone.**

| Milestone | Work | Deliverable | Approval gate |
|---|---|---|---|
| **0. Repository re-audit** | Inspect existing files independently; no edits | Evidence-based audit and original-file hashes | Findings trace to actual files |
| **1. Dataset feasibility** | Investigate and inspect exact Backblaze source files; no edits unless approved | Source/subset/resource/quality report | Owner approves exact dataset and question |
| **2. Analytical contract** | Define population, outcome, exposure, exclusions, limitations | Question and metric documents | Definitions are testable and understandable |
| **3. Ingestion and profiling** | Build reproducible selected-period load and quality report | Code, manifest, actual counts, tests | Input/output counts reconcile |
| **4. SQL analytical model** | Create justified tables/views and question-led SQL | Schema, SQL, fixture tests | Critical KPI outputs are hand-checked |
| **5. Python investigation** | EDA, missingness, cohort and sensitivity analysis | Focused notebooks/scripts | Every chart answers an approved question |
| **6. Findings brief** | Write actual results and limitations | `docs/FINDINGS.md` | Every reported number can be regenerated |
| **7. Dashboard** | Build interactive analytical story | Working dashboard and screenshots | Dashboard equals approved analytical outputs |
| **8. Reproducibility** | Clean-run instructions, tests, optional CI | Tested reproduction path | Commands work on a clean setup |
| **9. Deployment** | Choose proportionate hosting; deploy after approval | Tested URL or deployment-ready demo | Claim matches actual deployment state |
| **10. Optional evaluation** | Future-window ranking versus baseline | Evaluation report and tests | Separate methodological approval first |
| **11. Portfolio packaging** | README, case study, resume/cold-email drafts | Claim-to-proof mapping | No unsupported public claim |

Milestone 10 may be omitted entirely.

### Important sequencing rule

Do not produce a dashboard first and invent analytical findings to fill it. Complete the analytical contract, data-quality assessment, SQL analysis, and findings review first.

---

## 12. Required report from Antigravity after each milestone

Antigravity must use this format:

```text
MILESTONE:
STATUS: Complete / Blocked / Partially complete

FILES INSPECTED:
SOURCE LINKS AND EVIDENCE:
FILES CREATED:
FILES MODIFIED:
FILES MOVED OR DELETED:

COMMANDS ACTUALLY RUN:
- exact command
- exit code
- relevant unedited output

COUNTS / FINDINGS:
- exact calculation method and source

TESTS RUN:
- exact command
- pass/fail result

WHAT WAS NOT VERIFIED:
RISKS AND LIMITATIONS:
DECISIONS REQUIRING OWNER APPROVAL:
NEXT MILESTONE PROPOSAL:
```

“Done, everything works” is not an acceptable report. A file existing is not proof that its analysis or application works.

The agent **cannot approve its own gate**.

---

## 13. Stop conditions

Stop and request approval if:

- Source documentation conflicts with the proposed dataset interpretation.
- The selected subset has too few failures for the proposed comparison.
- The download or processing requirement is impractical.
- Missing SMART coverage makes a comparison misleading.
- The intended denominator cannot be defended.
- A Kaggle mirror differs materially from publisher data.
- Redistribution terms are uncertain for an artifact proposed for public hosting.
- The agent proposes changing the primary analytical question.
- The agent wants to add a model, API, second database, or major technology.
- A critical test fails.
- A result depends on silently excluding substantial data.
- The agent proposes deleting or rewriting original files.
- Deployment requires payment or public credentials.

---

## 14. Definition of done

The upgraded project is complete only when:

### Business and data

- [ ] Primary question is specific and supported by selected data.
- [ ] Source and usage terms are documented.
- [ ] Exact files and observation window are documented.
- [ ] Original inventory and Backblaze observations are not conflated.
- [ ] Population, exclusions, and data-quality effects are reproducible.

### Analytics

- [ ] Failure counts and denominators are defined and displayed.
- [ ] SQL answers real questions and reproduces key figures.
- [ ] Python EDA investigates defined hypotheses or anomalies.
- [ ] Coverage, changing fleet composition, and missingness are addressed.
- [ ] Findings distinguish observation from interpretation.
- [ ] Recommendations acknowledge limitations.

### Dashboard

- [ ] Source and observation period are prominent.
- [ ] Filters and chart values match the approved metric definitions.
- [ ] Cohort comparisons include count/exposure context.
- [ ] Low-quality or low-volume results are flagged.
- [ ] Screenshots show the actual finished dashboard.

### Proof and operations

- [ ] Key findings can be regenerated.
- [ ] Critical metric and data-quality tests pass.
- [ ] README leads with the business question and results.
- [ ] Public URL works if deployment is claimed.
- [ ] Resume and cold-email claims link to real evidence.
- [ ] Owner can explain the methods and limitations in an interview.

---

## 15. Session opener to paste into Antigravity

Use the strongest available model suitable for repository-wide data analysis,
SQL, coding, and review. If the tool exposes model selection, report which
model is actually active; do not claim a model you cannot verify.

Read `IMPLEMENTATION_PLAN.md` completely before doing anything else.

This is an ANALYTICS-FIRST upgrade of the EXISTING repository. The original
IT asset work is retained as a documented legacy/data-quality case study.
Backblaze is only a candidate primary analytical source until feasibility
is approved. Never merge these unrelated populations.

Work on ONE milestone at a time. Begin with Milestone 0 only:
- inspect all original project files independently;
- make zero file edits;
- cite filenames and actual findings;
- calculate SHA-256 hashes of original artifacts;
- identify contradictions between the repository and this plan;
- report what is verified, inferred, and unknown.

Return the Section 12 milestone report. Stop and wait for my approval.
Do not proceed to dataset download, coding, migration, or dashboard work.

After I approve Milestone 0, I will explicitly authorize Milestone 1.
Do not treat the whole implementation plan as permission to implement
every milestone at once.
