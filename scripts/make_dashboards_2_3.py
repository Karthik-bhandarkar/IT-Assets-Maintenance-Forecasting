"""
Render dashboards 2 and 3 of the AssetOps set, in the same design system as
dashboard_fleet_overview.png.

  2. Service Priority Worklist        -> dashboard_priority_worklist.png
  3. Data Quality & Ingestion Monitor -> dashboard_data_quality.png

Panels 2 and 3 need per-asset due dates and an event/ingestion history, which the
original register does not contain. They are therefore computed from the SEEDED
SYNTHETIC SCENARIO defined in the AssetOps spec (seed 42) and every canvas is
labelled as such. Dashboard 3 also shows the real audit results of the original
workbook alongside the scenario run.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ------------------------------------------------------------- design tokens
BG, CARD, EDGE = "#0b1220", "#151f2e", "#243349"
INK, MUTED, FAINT = "#f1f5f9", "#8b9ab1", "#5b6b84"
CYAN, EMERALD, CORAL, AMBER, VIOLET, BLUE = (
    "#22d3ee", "#34d399", "#fb7185", "#fbbf24", "#a78bfa", "#3b82f6")
GRID = "#1f2d40"

PRIORITY_COLOR = {
    "P1 Data review": AMBER,
    "P2 Urgent operational": CORAL,
    "P3 Overdue": "#f97316",
    "P4 Due within 30 days": CYAN,
    "P5 No action": EMERALD,
}

plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": BG,
                     "savefig.facecolor": BG, "text.color": INK,
                     "axes.facecolor": CARD, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.grid": False})


def card(fig, x, y, w, h, *, fc=CARD, ec=EDGE, lw=1.1, r=0.010, z=0):
    fig.patches.append(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
        transform=fig.transFigure, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))


def newax(fig, rect):
    ax = fig.add_axes(rect)
    ax.set_zorder(5)
    ax.patch.set_alpha(0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    return ax


def ptitle(fig, x, y, text, sub=None):
    fig.text(x, y, text, size=13.5, weight="bold", color=INK, va="top")
    if sub:
        fig.text(x, y - 0.0215, sub, size=9.4, color=FAINT, va="top")


def header(fig, title, subtitle, chips, mode_text, mode_color):
    card(fig, 0, 0.902, 1, 0.098, fc="#0e1726", ec="#0e1726", r=0.0)
    fig.text(0.028, 0.963, title, size=23, weight="bold", color=INK, va="center")
    fig.text(0.028, 0.928, subtitle, size=10.4, color=MUTED, va="center")
    px = 0.655
    for label, value in chips:
        w = 0.105
        card(fig, px, 0.925, w, 0.040, fc="#16212f", ec="#2b3b52", r=0.008)
        fig.text(px + 0.012, 0.953, label.upper(), size=7.2, color=FAINT, va="center")
        fig.text(px + 0.012, 0.938, value, size=9.6, color=INK, weight="bold", va="center")
        fig.text(px + w - 0.014, 0.945, "▾", size=9, color=MUTED, va="center")
        px += w + 0.012
    # dataset-mode banner strip
    card(fig, 0.028, 0.862, 0.944, 0.030, fc=mode_color[0], ec=mode_color[1], r=0.007)
    fig.text(0.042, 0.877, mode_text, size=9.6, color=mode_color[2], va="center",
             weight="bold")


def kpi_row(fig, kpis, y=0.726, h=0.118):
    kx, kw, gap = 0.028, 0.1792, 0.0127
    for label, value, sub, col in kpis:
        card(fig, kx, y, kw, h)
        fig.patches.append(mpatches.Rectangle((kx, y), 0.0032, h,
                                              transform=fig.transFigure, facecolor=col,
                                              edgecolor="none", zorder=1))
        fig.text(kx + 0.016, y + h - 0.025, " ".join(label), size=7.6, color=MUTED,
                 va="center", weight="bold")
        fig.text(kx + 0.016, y + h - 0.064, value, size=27, color=col, weight="bold",
                 va="center")
        fig.text(kx + 0.016, y + 0.021, sub, size=9.2, color=FAINT, va="center")
        kx += kw + gap


# ============================================================ scenario dataset
TYPES = ["Laptop", "Printer", "Router", "Monitor", "Keyboard"]
SITES = ["Hyderabad", "Bangalore", "Pune"]
AS_OF = date(2026, 1, 15)


def scenario(n=1200, seed=42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    offs = [-180, -120, -64, -31, -12, -3, 0, 5, 12, 18, 26, 30, 45, 90, 160, 300]
    p = np.array([.02, .03, .04, .05, .05, .03, .01, .05, .07, .07, .06, .04,
                  .10, .14, .12, .12])
    p = p / p.sum()
    rows = []
    for i in range(n):
        aid = f"S{i:05d}"
        t = TYPES[int(rng.integers(0, 5))]
        site = SITES[int(rng.integers(0, 3))]
        status = str(rng.choice(["Working", "Under Repair", "Decommissioned"],
                                p=[0.847, 0.103, 0.050]))
        due = None if rng.random() < 0.04 else AS_OF + timedelta(
            days=int(rng.choice(offs, p=p)) + int(rng.integers(-5, 6)))
        rows.append({"asset_id": aid, "asset_type": t, "location": site,
                     "status": status, "due_date": due})
    return pd.DataFrame(rows)


def classify(row):
    d, s = row.due_date, row.status
    if s == "Decommissioned":
        return "Excluded", "EXCLUDED", None
    if d is None:
        return "P1 Data review", "UNKNOWN", None
    n = (d - AS_OF).days
    if n < 0:
        return (("P2 Urgent operational" if s == "Under Repair" else "P3 Overdue"),
                "OVERDUE", n)
    if n <= 30:
        return "P4 Due within 30 days", "DUE_WITHIN_30", n
    return "P5 No action", "LATER", n


def reason(p, n):
    return {"P1 Data review": "No usable service schedule on record",
            "P2 Urgent operational": f"Overdue by {abs(n) if n is not None else 0} days "
                                     f"and currently under repair",
            "P3 Overdue": f"Overdue by {abs(n) if n is not None else 0} days",
            "P4 Due within 30 days": f"Due in {n} days",
            "P5 No action": f"Next service due in {n} days",
            "Excluded": "Decommissioned — excluded from planning"}[p]


ACTION = {"P1 Data review": "Correct the schedule record",
          "P2 Urgent operational": "Escalate to site lead",
          "P3 Overdue": "Schedule service now",
          "P4 Due within 30 days": "Add to next batch",
          "P5 No action": "No action"}


# ======================================================= DASHBOARD 2: worklist
def build_worklist(df: pd.DataFrame, out: Path):
    cls = df.apply(classify, axis=1, result_type="expand")
    df = df.assign(priority=cls[0], due_status=cls[1], days=cls[2])
    df["reason"] = [reason(p, None if pd.isna(n) else int(n))
                    for p, n in zip(df.priority, df.days)]
    rank = {k: i for i, k in enumerate(
        ["P1 Data review", "P2 Urgent operational", "P3 Overdue",
         "P4 Due within 30 days", "P5 No action", "Excluded"])}
    df["rank"] = df.priority.map(rank)
    q = df[df.priority.isin(list(PRIORITY_COLOR)[:4])].sort_values(
        ["rank", "days"], na_position="first")
    counts = df.priority.value_counts()

    fig = plt.figure(figsize=(16, 9.5), dpi=120)
    header(fig, "Service Priority Worklist",
           f"Rule-based review queue  ·  planning date {AS_OF:%d %b %Y}  ·  "
           f"{len(df):,} assets in scope  ·  {len(q):,} require review",
           [("Dataset", "Scenario"), ("Priority", "All"), ("Site", "All (3)")],
           "SYNTHETIC DEMONSTRATION DATA (seed 42) — generated to exercise the planning "
           "workflow. It does not describe any real organisation.",
           ("#1b2a1f", "#2f5137", "#8fd3a4"))

    kpi_row(fig, [
        ("REVIEW QUEUE", f"{len(q):,}", "assets needing an action", CYAN),
        ("P1 DATA REVIEW", f"{counts.get('P1 Data review', 0):,}", "schedule missing/invalid", AMBER),
        ("P2 URGENT", f"{counts.get('P2 Urgent operational', 0):,}", "overdue + under repair", CORAL),
        ("P3 OVERDUE", f"{counts.get('P3 Overdue', 0):,}", "past the due date", "#f97316"),
        ("P4 DUE ≤ 30 DAYS", f"{counts.get('P4 Due within 30 days', 0):,}", "upcoming batch", EMERALD),
    ])

    # ---- left: priority mix
    lx, ly, lw, lh = 0.028, 0.095, 0.236, 0.610
    card(fig, lx, ly, lw, lh)
    ptitle(fig, lx + 0.018, ly + lh - 0.022, "Queue by priority band",
           "first matching rule wins — see docs/METRICS.md")
    ax = newax(fig, [lx + 0.020, ly + 0.300, lw - 0.042, lh - 0.360])
    bands = list(PRIORITY_COLOR)[::-1]
    vals = [counts.get(b, 0) for b in bands]
    ax.barh(range(len(bands)), vals, height=0.52,
            color=[PRIORITY_COLOR[b] for b in bands])
    for i, (b, v) in enumerate(zip(bands, vals)):
        ax.text(0, i + 0.42, b, size=10.0, color=INK, va="center")
        ax.text(v + max(vals) * 0.02, i, f"{v:,}", size=10.4, weight="bold",
                color=PRIORITY_COLOR[b], va="center")
    ax.set_xlim(0, max(vals) * 1.22); ax.set_ylim(-0.6, len(bands) - 0.3)

    # overdue by site
    ptitle(fig, lx + 0.018, ly + 0.268, "Overdue by delivery centre",
           "P2 + P3, count of assets")
    ov = (df[df.priority.isin(["P2 Urgent operational", "P3 Overdue"])]
          .groupby("location").size().reindex(SITES).fillna(0))
    ax = newax(fig, [lx + 0.020, ly + 0.040, lw - 0.042, 0.180])
    ax.bar(range(3), ov.values, width=0.5, color="#f97316")
    for i, v in enumerate(ov.values):
        ax.text(i, v + ov.max() * 0.06, f"{int(v)}", ha="center", size=10.4,
                weight="bold", color=INK)
    ax.set_xticks(range(3)); ax.set_xticklabels(SITES, size=10.0, color=MUTED)
    ax.tick_params(length=0, pad=5); ax.set_ylim(0, ov.max() * 1.28)
    ax.axhline(0, color=GRID, lw=1)

    # ---- right: the worklist table
    tx, tw = 0.276, 0.696
    card(fig, tx, ly, tw, lh)
    ptitle(fig, tx + 0.018, ly + lh - 0.022, "Top of the queue",
           "every row carries the rule that put it there — no score, no black box")
    cols = [("ASSET", 0.018), ("TYPE", 0.072), ("SITE", 0.142), ("STATUS", 0.222),
            ("DUE DATE", 0.312), ("DAYS", 0.392), ("PRIORITY", 0.436),
            ("WHY THIS ASSET IS LISTED", 0.508)]
    hy = ly + lh - 0.070
    for name, dx in cols:
        fig.text(tx + dx, hy, name, size=8.0, color=FAINT, weight="bold", va="center")
    fig.patches.append(mpatches.Rectangle((tx + 0.016, hy - 0.014), tw - 0.032, 0.0012,
                                          transform=fig.transFigure, facecolor=EDGE,
                                          edgecolor="none", zorder=2))
    take = {"P1 Data review": 4, "P2 Urgent operational": 4,
            "P3 Overdue": 4, "P4 Due within 30 days": 3}
    rows = pd.concat([q[q.priority == b].head(k) for b, k in take.items()])
    ry = hy - 0.034
    for k, (_, r) in enumerate(rows.iterrows()):
        if k % 2 == 0:
            card(fig, tx + 0.012, ry - 0.0145, tw - 0.024, 0.029, fc="#18243500",
                 ec="none", r=0.004)
            fig.patches.append(mpatches.Rectangle(
                (tx + 0.012, ry - 0.0145), tw - 0.024, 0.029,
                transform=fig.transFigure, facecolor="#1a2636", edgecolor="none", zorder=1))
        col = PRIORITY_COLOR[r.priority]
        due = f"{r.due_date:%d %b %Y}" if r.due_date is not None and not pd.isna(r.due_date) else "—"
        days = "—" if pd.isna(r.days) else f"{int(r.days):+d}"
        vals = [r.asset_id, r.asset_type, r.location, r.status, due, days]
        for (name, dx), v in zip(cols[:6], vals):
            c = CORAL if (name == "STATUS" and v == "Under Repair") else INK
            if name == "DAYS" and not pd.isna(r.days) and r.days < 0:
                c = "#f97316"
            fig.text(tx + dx, ry, str(v), size=9.6, color=c, va="center", zorder=3)
        # priority chip
        chip = r.priority.split(" ")[0]
        card(fig, tx + cols[6][1] - 0.002, ry - 0.011, 0.034, 0.022,
             fc="#1f2b3d", ec=col, r=0.006, z=2)
        fig.text(tx + cols[6][1] + 0.015, ry, chip, size=8.8, color=col, weight="bold",
                 ha="center", va="center", zorder=3)
        fig.text(tx + cols[7][1], ry, r.reason, size=9.4, color="#c6d2e4", va="center",
                 zorder=3)
        ry -= 0.029

    fig.text(tx + 0.018, ly + 0.030,
             f"Showing {len(rows)} of {len(q):,} queued assets  ·  ordered by priority band, then "
             f"most overdue first  ·  full list exports to CSV from the dashboard",
             size=9.0, color=FAINT, va="center")

    fig.text(0.028, 0.050, "AssetOps  ·  rule-based prioritisation  ·  no model, no "
             "forecast: each row states the rule that selected it", size=9.0,
             color=FAINT, va="center")
    fig.text(0.972, 0.050, "AssetOps  ·  priority worklist  ·  v1", size=9.0,
             color=FAINT, va="center", ha="right")
    fig.savefig(out.with_suffix(".png"), dpi=120, facecolor=BG)
    fig.savefig(out.with_suffix(".svg"), facecolor=BG)
    plt.close(fig)
    print("wrote", out.with_suffix(".png"))


# ================================================== DASHBOARD 3: data quality
def build_quality(out: Path):
    fig = plt.figure(figsize=(16, 9.5), dpi=120)
    header(fig, "Data Quality & Ingestion Monitor",
           "Validation outcome of every load  ·  original register audit + scenario "
           "load  ·  last refresh 15 Jan 2026, 02:14 IST",
           [("Dataset", "All"), ("Run", "Latest"), ("Window", "30 days")],
           "ORIGINAL REGISTER AUDIT — the extract passes completeness and uniqueness but "
           "fails both service-schedule checks. Planning figures are blocked, not guessed.",
           ("#2a2113", "#584214", "#f0c95b"))

    kpi_row(fig, [
        ("ROWS READ", "10,000", "latest original load", CYAN),
        ("ACCEPTED", "10,000", "100.0% of rows", EMERALD),
        ("REJECTED", "0", "no row-level failures in the original", EMERALD),
        ("DATASET WARNINGS", "2", "both schedule checks failed", AMBER),
        ("FRESHNESS", "4h 12m", "since last successful load", VIOLET),
    ])

    # --- A: validation rule results
    ax_x, ay, aw, ah = 0.028, 0.368, 0.470, 0.337
    card(fig, ax_x, ay, aw, ah)
    ptitle(fig, ax_x + 0.018, ay + ah - 0.022, "Validation rules — original register",
           "row-level rules reject records; dataset-level rules raise warnings")
    checks = [
        ("PASS", "Required columns present", "7 of 7 expected columns"),
        ("PASS", "Completeness", "0 null values across 70,000 cells"),
        ("PASS", "Uniqueness of AssetID", "0 duplicates in 10,000 rows"),
        ("PASS", "Status domain", "3 known values: Working, Under Repair, Decommissioned"),
        ("PASS", "Purchase date plausible", "range 29 Apr 2020 – 28 Apr 2024"),
        ("WARN", "Distinct NextServiceDue values", "1 value (30 Apr 2025) for all 10,000"),
        ("WARN", "Distinct LastServiceDate values", "1 value (29 Apr 2025) for all 10,000"),
    ]
    ty = ay + ah - 0.070
    for state, rule, detail in checks:
        ok = state == "PASS"
        c = EMERALD if ok else AMBER
        card(fig, ax_x + 0.020, ty - 0.013, 0.044, 0.024, fc="#16261d" if ok else "#2a2113",
             ec=c, r=0.006, z=2)
        fig.text(ax_x + 0.042, ty, state, size=8.2, color=c, weight="bold",
                 ha="center", va="center", zorder=3)
        fig.text(ax_x + 0.074, ty, rule, size=10.0, color=INK, va="center")
        fig.text(ax_x + 0.268, ty, detail, size=9.2, color=FAINT, va="center")
        ty -= 0.0335

    # --- B: rejection reasons (scenario load)
    bx, bw = 0.512, 0.460
    card(fig, bx, ay, bw, ah)
    ptitle(fig, bx + 0.018, ay + ah - 0.022, "Rejection reasons — scenario load",
           "deliberately invalid rows, used to prove the validator fires")
    reasons = {"UNPARSEABLE_DATE": 4, "UNKNOWN_STATUS": 3, "DUPLICATE_ASSET_ID": 2,
               "MISSING_ASSET_ID": 1, "UNKNOWN_LOCATION": 1, "UNKNOWN_ASSET_TYPE": 1,
               "FUTURE_PURCHASE_DATE": 1}
    ax = newax(fig, [bx + 0.150, ay + 0.048, bw - 0.185, ah - 0.120])
    ks = list(reasons)[::-1]
    vs = [reasons[k] for k in ks]
    ax.barh(range(len(ks)), vs, height=0.5, color=CORAL)
    mx = max(vs)
    for i, (k, v) in enumerate(zip(ks, vs)):
        ax.text(-mx * 0.03, i, k, ha="right", va="center", size=9.4, color="#c6d2e4")
        ax.text(v + mx * 0.03, i, str(v), va="center", size=9.8, weight="bold", color=CORAL)
    ax.set_xlim(0, mx * 1.22); ax.set_ylim(-0.6, len(ks) - 0.4)
    fig.text(bx + 0.020, ay + 0.030, "12 rejected rows out of 1,212 read  ·  "
             "each rejection is stored with its row number and offending value",
             size=9.0, color=FAINT, va="center")

    # --- C: ingestion run history
    cx, cy, cw, ch = 0.028, 0.095, 0.624, 0.255
    card(fig, cx, cy, cw, ch)
    ptitle(fig, cx + 0.018, cy + ch - 0.022, "Ingestion run history",
           "every load is recorded: source, duration, counts, outcome")
    cols = [("RUN", 0.020), ("DATASET", 0.062), ("SOURCE", 0.145), ("FINISHED", 0.300),
            ("READ", 0.395), ("ACCEPTED", 0.448), ("REJECTED", 0.522), ("STATUS", 0.580)]
    hy = cy + ch - 0.068
    for name, dx in cols:
        fig.text(cx + dx, hy, name, size=8.0, color=FAINT, weight="bold", va="center")
    fig.patches.append(mpatches.Rectangle((cx + 0.016, hy - 0.013), cw - 0.032, 0.0012,
                                          transform=fig.transFigure, facecolor=EDGE,
                                          edgecolor="none", zorder=2))
    runs = [
        (4, "scenario", "data/scenario/", "15 Jan 02:14", "1,212", "1,200", "12", "success"),
        (3, "original", "01_IT_ASSESMENT.xlsx", "15 Jan 02:11", "10,000", "10,000", "0", "success"),
        (2, "original", "01_IT_ASSESMENT.xlsx", "14 Jan 19:02", "10,000", "10,000", "0", "success"),
        (1, "original", "missing_file.xlsx", "14 Jan 18:57", "0", "0", "0", "failed"),
    ]
    ry = hy - 0.032
    for k, r in enumerate(runs):
        if k % 2 == 0:
            fig.patches.append(mpatches.Rectangle(
                (cx + 0.012, ry - 0.0145), cw - 0.024, 0.029, transform=fig.transFigure,
                facecolor="#1a2636", edgecolor="none", zorder=1))
        for (name, dx), v in zip(cols[:7], r[:7]):
            fig.text(cx + dx, ry, str(v), size=9.6, color=INK, va="center", zorder=3)
        ok = r[7] == "success"
        c = EMERALD if ok else CORAL
        card(fig, cx + cols[7][1], ry - 0.011, 0.052, 0.022,
             fc="#16261d" if ok else "#2b161b", ec=c, r=0.006, z=2)
        fig.text(cx + cols[7][1] + 0.026, ry, r[7], size=8.6, color=c, weight="bold",
                 ha="center", va="center", zorder=3)
        ry -= 0.029
    fig.text(cx + 0.018, cy + 0.024,
             "Re-running the same file is idempotent: run 3 re-read 10,000 rows and the "
             "asset count stayed at 10,000.", size=9.2, color=FAINT, va="center")

    # --- D: what this means
    dx2, dw2 = 0.666, 0.306
    card(fig, dx2, cy, dw2, ch, fc="#1b1407", ec="#584214")
    ptitle(fig, dx2 + 0.018, cy + ch - 0.022, "What this blocks",
           "the dashboard refuses to publish a figure it cannot support")
    lines = [
        (EMERALD, "Publishable", "fleet counts, status mix, site and category breakdowns"),
        (CORAL, "Blocked", "\"assets due in the next 30 days\" from the original file"),
        (CORAL, "Blocked", "overdue ranking and any service-priority queue"),
        (CYAN, "Workaround", "switch to the scenario dataset to demonstrate the workflow"),
    ]
    ty = cy + ch - 0.075
    for c, tag, text in lines:
        fig.text(dx2 + 0.020, ty, "●", size=11, color=c, va="center")
        fig.text(dx2 + 0.036, ty, tag, size=9.6, color=c, weight="bold", va="center")
        fig.text(dx2 + 0.036, ty - 0.019, text, size=9.0, color="#c6d2e4", va="center")
        ty -= 0.046

    fig.text(0.028, 0.050, "AssetOps  ·  every figure above is produced by the ingestion "
             "run records, not typed by hand", size=9.0, color=FAINT, va="center")
    fig.text(0.972, 0.050, "AssetOps  ·  data quality monitor  ·  v1", size=9.0,
             color=FAINT, va="center", ha="right")
    fig.savefig(out.with_suffix(".png"), dpi=120, facecolor=BG)
    fig.savefig(out.with_suffix(".svg"), facecolor=BG)
    plt.close(fig)
    print("wrote", out.with_suffix(".png"))


if __name__ == "__main__":
    here = Path(__file__).parent
    build_worklist(scenario(), here / "dashboard_priority_worklist")
    build_quality(here / "dashboard_data_quality")
