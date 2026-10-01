# Autonomous Master Execution Instruction: Analytics-First Upgrade

> **Purpose:** Master autonomous instructions for upgrading the IT-Assets-Maintenance-Forecasting project into a credible, defensible Data Analyst / BI Analyst portfolio project.

```text
You are the primary implementation agent for an ANALYTICS-FIRST upgrade of
this existing IT asset project. Work autonomously through the project, but
never confuse autonomous work with permission to invent evidence or bypass
verification.

PRIMARY GOAL
Build a credible, reproducible Data Analyst / BI Analyst portfolio project:
business question → documented data → quality assessment → SQL and Python
analysis → defensible findings → interactive dashboard → recommendations
→ verifiable proof.

This is NOT primarily a backend-engineering or machine-learning project.

PROJECT CONTEXT TO VERIFY, NOT ASSUME
A prior audit reported that the existing repository contains an approximately
10,000-row IT asset inventory with identical last-service and next-due dates,
a notebook that mislabels current "Under Repair" share as failure rate, and
a Tableau workbook that reads an Excel extract rather than live SQL. Verify
all claims directly from files. Preserve the original work as an honest
legacy/data-quality case study.

Backblaze Drive Stats is a CANDIDATE primary source for new hardware
reliability analysis. It has NOT yet been approved as suitable for any
particular analytical claim. The original inventory and Backblaze observations
are unrelated populations: never merge or portray them as one fleet.

The earlier AssetOps service-planning build plan, if present, is SUPERSEDED
for new development. Do not automatically implement its service-schedule
schema, synthetic maintenance events, priority rules, FastAPI application,
or forecasting claims.

NON-NEGOTIABLE RULES
1. Inspect the entire existing repository before editing. List inspected
   files, uninspected files, existing behavior, contradictions, and risks.
2. Do not delete or rewrite original artifacts. Record SHA-256 hashes before
   any approved moves and confirm hashes afterward. Check provenance and
   redistribution rights; moving a file does not erase it from Git history.
3. Verify the official source, file coverage, field meanings, usage terms,
   download sizes, and feasible subset before building around Backblaze.
   Cite exact URLs and distinguish documented facts from inference.
4. Do not choose a random sample of drive-day rows for longitudinal analysis.
   Select a documented, contiguous period and define any model/drive
   selection before inspecting comparative results.
5. Never fabricate dataset counts, missingness, failures, findings, rates,
   confidence intervals, test results, screenshots, URLs, deployment
   status, performance, business savings, or resume claims.
6. A command exiting successfully is not enough: validate the output against
   a defined expected result or an independently checked fixture.
7. Distinguish observed failure incidence from individual future failure
   probability. Distinguish association from causation. Do not assume
   "first observed" means "drive installed" or that a disappearing drive failed.
8. Do not add a predictive model or review-ranking feature unless the
   longitudinal outcome window, leakage controls, baseline, and temporal
   evaluation can be defended. Strong descriptive analytics is preferable
   to weak prediction.
9. Favor meaningful SQL, data quality, analytical reasoning, findings, and
   dashboard clarity over extra infrastructure. An API is optional.
10. Do not commit large raw downloads, credentials, database files, or data
    whose redistribution permission has not been established.
11. Continue automatically from one internally VERIFIED phase to the next.
    Stop for me only for credentials, external authorization, payment,
    public publication, destructive actions, genuinely ambiguous
    methodological choices, or other decisions requiring human judgment.
    If blocked on an optional task, document it and continue with safe,
    independent work. Do not call blocked work complete.

CREATE AND MAINTAIN THESE CONTROL FILES
After the initial read-only audit, create:

IMPLEMENTATION_PLAN.md
- Project question and scope.
- Every phase, dependencies, tasks, expected artifacts, validation method,
  pass/fail criterion, and definition of done.
- Explicit decisions about data source, SQL storage, dashboard, and deployment
  only after their feasibility has been assessed.
- A change log when the plan changes.

VALIDATION.md
- Continuous source of truth; update after EVERY meaningful step.
- For each requirement record:
  ID | phase | requirement | files changed | exact validation command/method |
  expected result | actual result | evidence path/output | status |
  remaining issue.
- Use only: NOT STARTED, IN PROGRESS, PASS, FAIL, BLOCKED,
  NEEDS HUMAN VERIFICATION, or NOT APPLICABLE.
- Never initialize an untested requirement as PASS.
- A file merely existing is not proof its contents are correct.
- Redact secrets and avoid committing enormous logs.

MANUAL-VERIFICATION.md
- Exact, numbered human checks: prerequisites, command or UI action,
  expected observable result, what failure looks like, and what to report.
- Include business interpretation, visual dashboard review, rights/terms
  decisions, and hosted URL checks where applicable.

FINAL-VALIDATION-REPORT.md
- Create at the end from actual VALIDATION.md evidence.
- Summarize PASS/FAIL/BLOCKED/NEEDS HUMAN VERIFICATION separately.
- Cover data, analytical methods, SQL, Python, dashboard, security,
  reproducibility, documentation, deployment, and public claims.
- Provide exact commands to run and test the project.
- If work remains, say "PARTIALLY COMPLETE", not "finished".

PHASE 0 — READ-ONLY REPOSITORY AUDIT
Inspect source files, spreadsheets, notebooks, SQL, workbook connection,
dependencies, README, documentation, configuration, and Git status.
Report actual dataset profile and important contradictions with file evidence.
Record hashes of original artifacts. Identify whether existing files may be
redistributed. Do not edit until this audit is complete. Then write the
initial implementation plan and validation register, using audit evidence.

PHASE 1 — SOURCE AND FEASIBILITY
Investigate Backblaze at its original publisher. If using Kaggle, identify
the exact mirror and compare its period, attribution, completeness, and terms
with the publisher. Inspect specifically identified files; report actual
file sizes, periods, row grain, stable ID, failure-field definition, models,
SMART availability, duplicates, missingness, failures, and resources needed.
Choose a reproducible, laptop-manageable subset only after evaluating these
facts. Record exact download steps and checksums when feasible.

If Backblaze is unsuitable, do not secretly substitute a dataset. Document
the failure and a justified alternative proposal. Seek human judgment if the
primary business question must materially change.

PHASE 2 — ANALYTICAL CONTRACT
Before charts or findings, document in docs/ANALYTICAL-QUESTION.md and
docs/METRICS.md:
- stakeholder question and decision;
- source files and observation window;
- population, cohort exclusions, raw and analytical grain;
- what counts as an observed failure;
- exposure denominator and units;
- treatment of duplicate days, missing days, first/last observations,
  disappearing drives, and incomplete follow-up;
- minimum support and warnings for model comparisons;
- SMART coverage and cross-model comparability limitations.
Build small hand-checkable example fixtures for central calculations.

The initial primary question is:
"How does observed hard-drive failure incidence differ across drive models
and observation periods, accounting for observed drive-time and coverage?"
Revise it if the verified dataset cannot support it; record why.

PHASE 3 — REPRODUCIBLE INGESTION AND QUALITY
Implement only the ingestion and storage necessary for analysis. Maintain
a source manifest and actual before/after counts. Detect invalid dates,
IDs, failure flags, duplicate drive-date records, and relevant schema
differences. Document exclusions, warnings, and rerun behavior. Test with
small deliberately corrupted fixtures. Avoid silently dropping data.

PHASE 4 — SQL ANALYTICAL LAYER
Choose a practical SQL database for the approved subset and explain why.
Build only justified tables/views. Write question-led SQL for source quality,
cohort composition, observation coverage, exposure, failures, model/time
comparisons, and SMART availability. Use joins, CTEs, and window functions
where useful, not for decoration. Test critical SQL calculations against
hand-worked fixtures and reconcile important outputs with Python.

PHASE 5 — PYTHON EDA AND STATISTICAL REASONING
Investigate defined questions, not random charts. Examine changing fleet
composition, model-level missingness, exposure, small denominators, and
sensitivity to defensible cohort rules. If uncertainty intervals are used,
document their assumptions. Do not assert root causes or causal effects
from observational comparisons.

PHASE 6 — FINDINGS BEFORE DASHBOARD
Write docs/FINDINGS.md. For every finding include:
finding; exact evidence and reproduction command/query; denominator;
interpretation; limitation; and recommended investigation or action.
Remove any finding that cannot be reproduced. Do not invent a finding just
to make the dashboard attractive.

PHASE 7 — BI DASHBOARD
Build a professional interactive dashboard using a tool selected for
analytical suitability and practical sharing. A web dashboard is acceptable;
Tableau/Power BI is acceptable if publication and reproducibility work.
Display source, observation period, extract/build date, filters, coverage,
failure counts, exposure, rates, low-volume caveats, findings, and limitations.
Only include SMART or temporal views supported by approved data.
Every chart must answer a stated stakeholder question. Reconcile displayed
figures with the approved analytical outputs. Capture genuine screenshots;
if visual verification cannot be performed, mark NEEDS HUMAN VERIFICATION.

PHASE 8 — REPRODUCIBILITY, TESTS, AND DEPLOYMENT
Provide a clean-run path for obtaining permitted source files, building
analytical outputs, running tests, and launching the dashboard. Add CI and
containers only when they improve reproducibility. For a large source, a
versioned aggregate/dashboard extract may be deployed instead of hosting
all raw drive-days. Document how the extract was produced and its limitations.
A public demo requires my approval before external publication or spending.
Call a project "deployed" only after a working URL was actually tested;
otherwise call it "deployment-ready".

PHASE 9 — OPTIONAL FORWARD-LOOKING EVALUATION
Only if independently justified and documented: define decision dates,
future outcome window, eligibility, sufficient follow-up, signals available
at decision time, earlier development period, later evaluation period, and
a capacity-matched baseline. Test leakage and report errors and limitations.
Otherwise mark this phase NOT APPLICABLE, explain why, and do not imply that
prediction was completed.

PHASE 10 — PORTFOLIO AND FINAL AUDIT
Update README to lead with the business question, verified results, source,
method, dashboard, limitations, and reproducibility. Explain the original
project's evolution without conflating the two datasets. Include a concise
claim-to-proof map. Draft resume bullets and cold-email wording using only
completed, verified findings; label drafts pending my personal approval.
Run a final clean-state test where feasible. Audit data correctness, SQL,
Python, visual clarity, accessibility, security, performance claims,
documentation, deployment claims, and broken links. Complete
FINAL-VALIDATION-REPORT.md and MANUAL-VERIFICATION.md.

OPERATING CYCLE FOR EVERY PHASE
UNDERSTAND → AUDIT → PLAN → IMPLEMENT → TEST → VERIFY →
CAPTURE EVIDENCE → UPDATE VALIDATION.md → DOCUMENT → CONTINUE.

After each phase, write a brief checkpoint in VALIDATION.md:
- what changed;
- exact commands run and exit codes;
- expected and actual results;
- evidence paths;
- failures, limitations, and next phase.
Do not proceed past a FAILED foundational data or metric check. Fix it first,
or mark the dependent work BLOCKED.

FINAL RESPONSE TO ME
Report:
1. What is actually complete and what is not.
2. Exact data source, subset, dates, and usage/rights status.
3. Verified analytical findings and where each is reproduced.
4. Files created/changed and legacy handling.
5. Tests run, results, and evidence paths.
6. Dashboard launch command and actual public URL, if one exists.
7. Clean reproduction commands.
8. Security and deployment status.
9. Remaining blockers and limitations.
10. The exact steps I must personally perform from MANUAL-VERIFICATION.md.

Do not claim "fully finished" if any essential item is FAIL, BLOCKED, or
NEEDS HUMAN VERIFICATION. Make the status unmistakable.
```
