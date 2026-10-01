# Copy-paste prompts for Antigravity (one per milestone)

Put `ASSETOPS_BUILD_PLAN.md` in the repository root first, then paste these **one at a
time**. Never paste the next one until you have reviewed the previous report against that
milestone's GATE checklist.

---

### Session opener (paste once at the start of every new session)

```text
Read ASSETOPS_BUILD_PLAN.md in this repository completely before doing anything.
Use the highest-capability reasoning/coding model available in this environment. Do not
claim which model is active unless your tooling verifiably reports it.
Follow §0.2 RULES exactly. Report in the §0.3 format. Implement ONE milestone, then stop.
```

### M0
```text
Execute MILESTONE 0 (Re-audit) from ASSETOPS_BUILD_PLAN.md. Change ZERO files.
Run the audit script in §0.2 of that milestone and paste its real output. Give a verdict
(Confirmed / Refuted / Cannot determine) for findings F1-F7 in §2 with literal evidence,
plus the SHA-256 of the raw workbook and the secret-scan result. Then stop at GATE 0.
```

### M1
```text
MILESTONE 0 is approved. Execute MILESTONE 1 (Correct the project's claims).
Use `git mv` for the legacy files, write legacy/README.md, the honest root README.md,
docs/DECISIONS.md and .gitignore. Run the vocabulary grep in §1.2 and paste the result and
the SHA-256 comparison. Do not write any application code. Stop at GATE 1.
```

### M2
```text
MILESTONE 1 approved. Execute MILESTONE 2 (Contracts). Write docs/METRICS.md exactly as
specified, plus docs/DATA-PROVENANCE.md. Documentation only, no code. List every rule you
need me to approve as an explicit question. Stop at GATE 2.
```

### M3
```text
MILESTONE 2 approved. Execute MILESTONE 3 (Data strategy). Create pyproject.toml,
.env.example, src/assetops/config.py, the scenario generator and tests/test_scenario.py.
Run pytest and paste the real output. Prove the original workbook hash is unchanged.
Stop at GATE 3.
```

### M4
```text
MILESTONE 3 approved. Execute MILESTONE 4 (Database). Create both migration files, the
migration runner and the connection module. Run the migration twice and paste both
outputs. Run all four constraint-violation statements and paste the real Postgres errors.
Write docs/DATABASE.md with the ER diagram. Stop at GATE 4.
```

### M5
```text
MILESTONE 4 approved. Execute MILESTONE 5 (Ingestion). Implement validation.py,
excel_reader.py, loader.py, cli.py and the matching tests. Run every command in §5.5,
including the double-ingest and the missing-file case, and paste the SQL verification
output showing the asset count is unchanged after the rerun. Stop at GATE 5.
```

### M6
```text
MILESTONE 5 approved. Execute MILESTONE 6 (Domain + SQL). Implement due_status.py,
priority.py, metrics.py and sql/analytical_queries.sql. Add all boundary tests from §12.1
and §12.2 and the SQL/Python parity test. Paste full pytest output. Stop at GATE 6.
```

### M7
```text
MILESTONE 6 approved. Execute MILESTONE 7 (API). Implement schemas, deps, main and the
five route modules exactly to the table in §7.4. Priority must be computed by
domain.priority.decide, not re-implemented in SQL. Add tests/test_api.py covering every
happy and error case listed. Paste pytest output and the /docs endpoint list.
Stop at GATE 7.
```

### M8
```text
MILESTONE 7 approved. Execute MILESTONE 8 (Dashboard). Build the five sections exactly as
specified. The dashboard must call the API only. With source=original it must never imply
upcoming work. Save the five screenshots to docs/screenshots/. Paste one API JSON response
next to the matching dashboard numbers to prove they agree. Stop at GATE 8.
```

### M9
```text
MILESTONE 8 approved. Execute MILESTONE 9 (Hardening). Add the edge-case tests, request
logging, and run all four security checks in §9 pasting verbatim output. Report real
coverage numbers. Do not report a performance number unless you ran the exact command
given. Stop at GATE 9.
```

### M10
```text
MILESTONE 9 approved. Execute MILESTONE 10 (Compose + CI). Create both Dockerfiles,
docker-compose.yml, scripts/smoke_test.py and .github/workflows/ci.yml. Then run
`docker compose down -v` and execute the §10.4 sequence from scratch, pasting the full
terminal transcript and the smoke-test output. Push and paste the CI run URL.
Stop at GATE 10.
```

### M11
```text
MILESTONE 10 approved. Execute MILESTONE 11 step 1 and 2 ONLY: research current hosting
options that support API + dashboard + persistent Postgres, and present ONE recommendation
with cost, free-tier limits, cold-start behaviour, persistence and one alternative.
Do NOT deploy anything yet. Stop and wait.
```

### M12
```text
MILESTONE 11 approved. Execute MILESTONE 12 (Packaging). Finalise README, architecture
diagram, screenshots, the milestone tracker table and the claim-to-proof matrix in §14 with
real evidence links. Remove any claim you cannot link to evidence. Stop at GATE 12.
```

---

### If the agent drifts

```text
Stop. You violated the spec: <quote the rule from ASSETOPS_BUILD_PLAN.md §0.2>.
Revert the out-of-scope changes, re-read that section, and report what you actually did
versus what the milestone permitted. Do not continue until I approve.
```

### If the agent says "done, everything works"

```text
That is not an acceptable report. Re-submit in the §0.3 delivery format with: exact files
changed, verbatim commands with exit codes, verbatim test output, and an explicit list of
what you did NOT verify.
```
