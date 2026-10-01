# karthik — working folder

Everything produced for the AssetOps rebuild, in one place.

| File | What it is | Use it for |
|---|---|---|
| `ASSETOPS_BUILD_PLAN.md` | The full 2,655-line implementation specification: 12 milestones, approval gates, and complete ready-to-use contents for ~25 files (schema, migrations, validation, CLI, domain rules, SQL, FastAPI, dashboard, Docker, CI, tests) | Drop this in the repo root and point Antigravity at it |
| `PASTE_TO_ANTIGRAVITY.md` | 14 copy-paste prompts — session opener, one per milestone, plus two drift-correction prompts | Paste one at a time, never two |
| `HANDOFF.md` | What is already done, what you must do first, the 12-milestone table with time estimates and gate checks, the 6 rules to enforce | Your control sheet while the agent works |
| `dashboard_fleet_overview.png` / `.svg` | Fleet overview dashboard, rendered from the real register | README, portfolio, slides |
| `dashboard_priority_worklist.png` / `.svg` | Service priority worklist with a Reason column on every row | README, portfolio, slides |
| `dashboard_data_quality.png` / `.svg` | Data quality + ingestion monitor | README, portfolio, slides |
| `make_dashboard.py`, `make_dashboards_2_3.py` | Scripts that generate the three dashboards | ship them with the repo so the images are verifiable |
| `README_SNIPPET.md` | Paste-ready markdown for all three images | your GitHub README |
| `tableau_dashboard_mockup.png` | AI-generated Tableau-style concept image | concept slides only — never as README proof |

## Important note on the image

`tableau_dashboard_mockup.png` is an **AI-generated concept mockup**, not a capture of
real software and not output from your data. Treat it as a design reference only.

- OK: using it as a visual target when building the Streamlit dashboard in Milestone 8, or
  as a header image in a presentation that says "concept".
- Not OK: putting it in `docs/screenshots/` or a README as proof that something works.
  The spec requires those to be real captures of the running application, and the
  claim-to-proof matrix (§14) would fail on a generated image.

The KPI values shown (10,000 / 8,470 / 1,028 and the per-type counts) do match the real
figures in the source workbook, so the mockup is accurate as a layout study.

## Related, kept outside this folder

- `/home/user/repo/` — clone of the original GitHub repository, unmodified.
- `/home/user/assetpulse/` — earlier ML experiment. **Superseded.** Do not merge it into
  AssetOps; it makes predictive claims on a simulated event history, which the plan forbids.
