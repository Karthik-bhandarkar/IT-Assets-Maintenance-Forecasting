# Existing Project Upgrade Plan: IT Hardware Reliability Analytics

Yes. We can **upgrade your existing GitHub repository** into a strong **data-analytics-first portfolio project** using Backblaze drive data as the primary analytical source.

But we must be precise about what “upgrade” means:

- Your **original IT asset spreadsheet and work remain in the repository** as the starting point and documented data-quality case study.
- Backblaze becomes the **primary dataset for new reliability analysis**, **only after the agent verifies a specific usable subset**.
- We do **not** combine the two datasets into one fictional fleet.
- The finished project is presented primarily as **SQL + Python analysis + BI decision support**, not as an API or software-engineering showcase.

> **Current status:** This is a build plan, not a claim that we have downloaded or analyzed Backblaze data. I cannot verify a specific Backblaze release, Kaggle mirror, license, row count, or finding from this chat.

---

## 1. Project identity

### Recommended name

**IT Hardware Reliability Analytics**

Keep the existing GitHub repository for now. Change its displayed project name and README when the new analytical question and dataset subset are approved. A repository URL rename can happen later; it is not necessary to begin the work.

### Portfolio one-liner

> An SQL- and Python-led analysis of longitudinal hard-drive health observations, examining reliability differences across drive cohorts and communicating defensible findings through an interactive dashboard.

### Why the original project led here

The original inventory reportedly has 10,000 asset rows, but all rows share the same last-service and next-service dates. It cannot substantiate the original forecasting claim. That is a legitimate part of the project history:

> “I audited the initial IT asset analysis, found that its service-date structure could not support meaningful forecasting, and rebuilt the project around a dataset with observed hardware outcomes.”

**Do not say:** “I combined our company’s asset inventory with Backblaze failures.” They are unrelated populations.

---

# 2. The real analytical problem

A hardware operations team has limited time to investigate devices. Aggregate failure counts alone can mislead because some models have many more drives or longer observation periods than others.

### Primary business question

> **How does observed hard-drive failure incidence differ across models and time periods, after accounting for the number of drives and their observed time in service?**

### Secondary analytical question

> **Which available SMART indicators show differences before recorded failures, and are those differences consistent enough to warrant further investigation?**

### Optional decision-support question

> **At a fixed review capacity, does a transparent health-signal ranking identify more subsequent failures than an appropriate simple baseline?**

The third question is **conditional**. It must not be promised until we confirm the selected data supports a valid future outcome window.

---

# 3. Dataset-selection gate: approve data before building

## Proposed primary source

**Backblaze Drive Stats**, preferably downloaded from the original publisher:

- [Backblaze Hard Drive Test Data](https://www.backblaze.com/cloud-storage/resources/hard-drive-test-data)

A Kaggle copy is acceptable **only if** the agent identifies its exact URL, publisher attribution, dates, completeness, and usage terms. “Found on Kaggle” does not by itself establish provenance or permission.

## Agent must verify

| Check | Why it matters |
|---|---|
| Exact files and covered dates | Defines what period the findings apply to |
| File sizes and extraction cost | Keeps reproduction practical |
| One-row grain | Prevents incorrect counting |
| Stable drive identifier | Needed to connect observations over time |
| Meaning of `failure` | Needed to define the outcome |
| Drive model and SMART fields | Needed for segmentation and signal analysis |
| Missingness by **model and period** | SMART fields are not uniformly available |
| Duplicate drive-date records | Can inflate exposure or outcomes |
| Number of observed failures | Determines whether comparisons are meaningful |
| Source and redistribution terms | Determines what can be committed or hosted |

**Subset rule:** Choose a documented, **contiguous observation period**, not a random selection of drive-day rows. If further limiting data is necessary, define the drive/model selection rule *before* looking at the results and preserve each selected drive’s time sequence.

### Gate outcome

The agent presents a short feasibility report. We approve:

1. Exact source files.
2. Dates.
3. Inclusion/exclusion rules.
4. Estimated local resource requirements.
5. Supported questions.
6. Unsupported questions.

**No dashboard, model, or database work before this gate.**

---

# 4. Analytics methodology

## A. Define the population

Document:

- Included dates.
- Included drive types/models.
- Whether models require a minimum number of drives, drive-days, or failures to appear in comparisons.
- How records before/after a failure are handled.
- What happens when a drive disappears from the observations.
- Whether the first observation is the drive’s first day in service—**do not assume it is**.

This is important because “first seen in this dataset” is not necessarily “new drive.”

## B. Define defensible metrics

| Metric | Proposed meaning | Important caution |
|---|---|---|
| **Observed drives** | Distinct drive IDs in the selected population | Does not mean all drives were observed for equally long |
| **Drive-days observed** | Valid drive-date observations | Check coverage and duplicate days |
| **Recorded failures** | Failures under the publisher’s documented definition | Do not treat every disappearance as failure |
| **Failure incidence per drive-time** | Recorded failures divided by observed drive-time, reported with explicit units | Requires an agreed exposure method and its limitations |
| **Model comparison** | Incidence alongside exposure and failure counts | Never rank a tiny cohort solely by a high rate |
| **SMART-field coverage** | Share of eligible observations with a usable value, by model/period | Missingness may make cross-model comparisons invalid |

An annualized rate may be useful, but it must be labeled as an **observed incidence rate based on the selected dataset and exposure rules**—not an unconditional probability that a particular drive will fail this year.

## C. Analysis sequence

```text
Source and grain
→ data profile
→ quality and coverage assessment
→ cohort definition
→ SQL metric calculations
→ model/time comparisons
→ SMART-field investigation
→ sensitivity checks
→ documented findings
→ dashboard
→ cautious recommendations
```

### Statistical reasoning

Use it where it answers a question:

- Show denominators and failure counts with every rate.
- Show uncertainty or suppress unstable comparisons when cohorts are small.
- Test whether findings change under reasonable alternative inclusion rules.
- Avoid interpreting a SMART association as proof of causation.
- If multiple model comparisons are explored, explain that this is exploratory analysis rather than a causal experiment.

**Do not add hypothesis tests merely to make the project look advanced.**

## D. Optional review-queue evaluation

Only after core analytics works:

1. Pick an explicit decision date and future outcome window.
2. Use signals available **on or before** the decision date.
3. Prevent the same future event from leaking into features.
4. Train or define ranking rules using earlier time periods.
5. Evaluate on later periods.
6. Compare at the **same review capacity** as a simple justified baseline.
7. Report identified failures, missed failures, false alarms, and cohort coverage.

Do not use an “oldest drive” baseline unless actual age is supportable. First-observed date may be a poor proxy.

If that evaluation is not credible, **leave it out**. The descriptive and diagnostic analysis can still be a strong Data Analyst project.

---

# 5. SQL and Python division of work

## SQL should be a headline skill

Build queries around questions, not syntax demonstrations:

| Question | SQL proof |
|---|---|
| Are observations duplicated or outside the approved period? | Validation queries |
| How does fleet composition change? | Grouping by period/model |
| How much observed drive-time does each model contribute? | Date analysis and aggregations |
| Which cohorts have more recorded failures relative to exposure? | Cohort views and joins |
| Which SMART fields are usable for which models? | Conditional counts and coverage |
| What did a drive’s observed history look like before failure? | Window functions, with careful time conditions |

Use CTEs and windows when they simplify those analyses. Document the question and interpretation above each important query.

## Python should add analytical depth

Use Pandas/NumPy for:

- Source profiling.
- Cleaning diagnostics.
- Cohort and missingness exploration.
- Distribution comparisons.
- Sensitivity analysis.
- Appropriate uncertainty calculations.
- Charts used in the written analytical report.

Tests should verify critical calculations against small hand-checked fixtures. **Python and SQL must not produce conflicting definitions of the same KPI.**

---

# 6. Proposed analytical data model

Finalize this only after inspecting the selected files.

| Layer | Possible content | Purpose |
|---|---|---|
| **Raw** | Retrieved source files, or download manifest/checksums if too large to commit | Trace provenance |
| **Validated observations** | Drive ID, observation date, model, failure indicator, selected SMART values | Consistent analytical input |
| **Quality results** | Rejected/flagged records, reason, source file | Explain exclusions |
| **Cohort/metric views** | Exposure and failures by approved dimensions | Consistent SQL-backed KPIs |
| **Dashboard extract** | Small, versioned aggregate outputs | Affordable, reproducible deployment |

A PostgreSQL database is useful if it genuinely supports the SQL analysis and reproducible cohort queries. **Do not put an entire huge raw dataset into a hosted database solely to make the deployment look sophisticated.** A local analytical database plus a documented, generated dashboard extract may be the more responsible choice.

---

# 7. Dashboard: analytics product, not a chart collection

A **Tableau-like interactive dashboard** is the main visible deliverable. Choose the tool after the data feasibility gate: Tableau/Power BI if publication and refresh are practical, or a lightweight web BI dashboard if that gives a more accessible live demo.

## Suggested dashboard story

| Section | Stakeholder question | Display |
|---|---|---|
| **Data confidence** | What period and population am I looking at? | Source, dates, model coverage, missingness warnings |
| **Fleet overview** | What was observed? | Drives, drive-time, recorded failures, model mix |
| **Reliability comparison** | Which cohorts differ? | Model-level failures, exposure, rate, uncertainty/low-volume warning |
| **Health-signal investigation** | Which fields show potentially useful patterns? | Coverage and pre-failure distributions, with model filter |
| **Findings and actions** | What merits investigation? | Finding → evidence → limitation → recommended next analysis/action |
| **Evaluation** *(conditional)* | Does a review ranking outperform a baseline? | Capacity-matched comparison and error trade-offs |

The dashboard must show **the observation period and data source**. It must not imply live monitoring of a real company’s fleet.

A useful dashboard can have **three excellent pages**, not necessarily five. Do not force a page with unsupported metrics.

---

# 8. Deployment plan

The deployed artifact should make the **analysis accessible**, not turn this into an infrastructure project.

## Recommended deployment pattern

```text
Backblaze source files
→ reproducible local data preparation
→ SQL + Python analytical outputs
→ versioned, documented dashboard extract
→ hosted interactive dashboard
```

Show on the dashboard:

- Source.
- Observation window.
- Date the extract was generated.
- Cohort exclusions.
- Link to methodology.

This is more affordable and reliable than requiring a public, always-on database containing a large drive-day dataset.

**Local proof:** A documented command sequence regenerates the analytical tables and dashboard extract from approved files.

**Deployment proof:** A tested public dashboard URL, screenshots, and the deployed extract version. If public hosting is not feasible, provide a runnable local dashboard and recorded walkthrough, and call it **deployment-ready**, not deployed.

Docker/CI may be added to improve reproducibility, but they are **supporting proof**. FastAPI is optional; it should not become the centre of the project.

---

# 9. Keep and restructure the existing repository

```text
IT-Assets-Maintenance-Forecasting/
├── README.md                     # New analytics-first project story
├── legacy/
│   ├── README.md                 # What the original project did and its limitations
│   └── ...                       # Original workbook, SQL, notebook, and docs
├── data/
│   ├── README.md                 # Download instructions and redistribution policy
│   ├── manifests/                # Source files, periods, checksums
│   └── samples/                  # Small permitted test samples
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

This is a **target structure**, not an instruction to create empty folders. Also, check the original spreadsheet’s redistribution rights before retaining or republishing it.

---

# 10. Proof-of-work requirements

| Claim you want to make | Proof required |
|---|---|
| “Analyzed real hardware observations” | Publisher attribution, exact files/period, inclusion rules |
| “Cleaned and validated data” | Actual before/after counts and documented exclusions |
| “Built SQL analysis” | Queries, results, hand-checked tests for core KPIs |
| “Compared reliability across models” | Failure counts **and** exposure denominators, not rates alone |
| “Investigated SMART signals” | Timing, missingness by model, distributions, limitations |
| “Identified a finding” | Reproducible query/analysis and exact reported value |
| **“Built an interactive dashboard”** | Live URL or runnable demo, screenshots, user journey |
| “Evaluated a review strategy” | Future-window definition, time split, baseline, capacity-matched results |
| “Improved reliability/reduced downtime” | **Do not claim** without measured real-world intervention outcomes |

## Cold-email proof package

A hiring manager should reach the substance quickly:

1. **GitHub README:** question and two or three verified findings at the top.
2. **Live dashboard:** immediately shows the analytical story.
3. **One-page findings brief:** numbers, denominators, interpretation, limitations.
4. **SQL evidence:** links to the queries behind each finding.
5. **Methodology:** explains why the conclusions are credible.

Your eventual cold email should lead with **one actual reproducible finding**, not a long list of tools. We will write it after the analysis produces a finding.

---

# 11. Revised milestone plan for Antigravity

**The earlier AssetOps service-planning specification is now superseded for new development.** Do not ask an agent to implement its `service_schedules`, synthetic maintenance events, or service-priority dashboard unchanged.

| Milestone | Deliverable | Approval gate |
|---|---|---|
| **0. Existing-repo audit** | Confirm original findings; identify files and claims to preserve/correct | Evidence references actual files; no edits |
| **1. Backblaze feasibility** | Exact source, subset, terms, grain, fields, sizes, preliminary quality counts | You approve dataset and question; no app code |
| **2. Analytical contract** | Population, metrics, exposure, exclusions, limitations | Definitions are understandable and testable |
| **3. Ingestion and profiling** | Reproducible selected-period load and actual quality report | Counts reconcile with inputs |
| **4. SQL model and analysis** | Schema/views and question-led SQL | Critical KPIs match hand-checked fixtures |
| **5. Python EDA** | Focused investigations, sensitivity checks | Charts support documented questions |
| **6. Findings brief** | Evidence, interpretation, limitations, recommended investigation | Every number is reproducible |
| **7. Dashboard** | Interactive BI story with source/period visible | Dashboard figures match approved analytical outputs |
| **8. Reproducibility and deployment** | Clean-run instructions, tests, optional CI, hosted demo if feasible | Commands work; URL tested if claimed |
| **9. Optional review-queue evaluation** | Baseline and future-window evaluation | Add only if the data and methodology permit it |
| **10. Portfolio package** | README, screenshots, case study, resume and cold-email drafts | Every public claim points to proof |

**Stop after every milestone for review.** “The agent says done” is not an approval gate.

---

# 12. Instruction to give the agent now

Use this **instead of** the old full-build prompt:

```text
We are upgrading the EXISTING IT-Assets-Maintenance-Forecasting repository
into a DATA-ANALYTICS-FIRST hardware reliability project.

The original repository remains as documented legacy work. Do not delete
its files or join its IT inventory to Backblaze drive observations.

The previous AssetOps service-planning build specification is superseded
for new development. Do not implement its synthetic maintenance events,
service-schedule schema, FastAPI endpoints, or priority rules by default.

WORK ON MILESTONE 0 AND MILESTONE 1 RESEARCH ONLY. MAKE NO FILE EDITS.

1. Independently confirm the old repository's data and analytical limits.
2. Investigate Backblaze Drive Stats at the original publisher.
3. If considering Kaggle, provide the exact mirror URL and compare its
   coverage, attribution, and usage terms with the publisher.
4. Propose a specific contiguous, laptop-manageable observation window.
5. Inspect identified files and report actual row counts, unique drives,
   recorded failures, duplicates, model distribution, SMART coverage,
   date coverage, and estimated compute/storage requirements.
6. Explain the proposed failure-incidence denominator and how disappearing
   drives or incomplete observation could bias it.
7. Recommend one primary business question and what the data cannot answer.
8. Provide exact source links and reproducible download/inspection commands.
9. Clearly separate verified facts, assumptions, and unknowns.

Do not build a database, model, dashboard, or API yet.
Do not invent findings. Stop for human approval.
```

## Final positioning

The project you want a Data Analyst recruiter to see is:

> **“I recognized that my original IT asset dataset could not support its forecasting claim. I sourced longitudinal hardware observations, defined reliable cohorts and KPIs, investigated failure patterns using SQL and Python, and built a dashboard that communicates evidence, uncertainty, and decisions.”**

That becomes a strong resume and cold-email story **only when the dataset is verified and the analysis produces reproducible results**. Our immediate next step is therefore **dataset feasibility**, not code generation.
