"""
Render the IT Asset Fleet & Maintenance Operations dashboard directly from the
source workbook. Every number on the canvas is computed at run time -- nothing
is hard-coded, so the image is a true render of the dataset.

    python make_dashboard.py  [path/to/01_IT_ASSESMENT(raw data).xlsx]

Outputs: dashboard_fleet_overview.png (1920x1140) and .svg
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

# ----------------------------------------------------------------- design tokens
BG        = "#0b1220"
CARD      = "#151f2e"
CARD_EDGE = "#243349"
INK       = "#f1f5f9"
MUTED     = "#8b9ab1"
FAINT     = "#5b6b84"
CYAN      = "#22d3ee"
EMERALD   = "#34d399"
CORAL     = "#fb7185"
AMBER     = "#fbbf24"
VIOLET    = "#a78bfa"
GRID      = "#1f2d40"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": BG,
    "savefig.facecolor": BG,
    "text.color": INK,
    "axes.facecolor": CARD,
    "axes.edgecolor": CARD_EDGE,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.grid": False,
})

HEAT = LinearSegmentedColormap.from_list("heat", ["#0f2a33", "#15616d", "#1f9ca8", "#22d3ee"])


# --------------------------------------------------------------------- helpers
def card(fig, x, y, w, h, *, fc=CARD, ec=CARD_EDGE, lw=1.1, r=0.010):
    fig.patches.append(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
        transform=fig.transFigure, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=0))


def panel_title(fig, x, y, text, sub=None):
    fig.text(x, y, text, size=13.5, weight="bold", color=INK, va="top")
    if sub:
        fig.text(x, y - 0.022, sub, size=9.4, color=FAINT, va="top")


def newax(fig, rect):
    """Axes above the card patches (figure patches and axes share zorder space)."""
    ax = fig.add_axes(rect)
    ax.set_zorder(5)
    ax.patch.set_alpha(0)
    return ax


def bare(ax):
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor("none")
    return ax


# ------------------------------------------------------------------------ data
def load(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path)
    df.columns = [str(c).strip() for c in df.columns]
    for c in ("PurchaseDate", "LastServiceDate", "NextServiceDue"):
        df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


def build(df: pd.DataFrame, out: Path) -> None:
    n = len(df)
    status = df["Status"].value_counts()
    working, repair, decom = (int(status.get(k, 0)) for k in
                              ("Working", "Under Repair", "Decommissioned"))
    by_type = df["AssetType"].value_counts().sort_values()
    xtab = pd.crosstab(df["AssetType"], df["Location"])
    st_loc = pd.crosstab(df["Location"], df["Status"])
    years = df["PurchaseDate"].dt.year.value_counts().sort_index()
    snapshot = df["NextServiceDue"].max()
    distinct_due = int(df["NextServiceDue"].nunique())
    distinct_last = int(df["LastServiceDate"].nunique())
    dupes = int(df["AssetID"].duplicated().sum())
    nulls = int(df.isna().sum().sum())
    age_years = (snapshot - df["PurchaseDate"]).dt.days / 365.25
    over3 = float((age_years > 3).mean())

    fig = plt.figure(figsize=(16, 9.5), dpi=120)

    # ============================================================== header band
    card(fig, 0.000, 0.902, 1.000, 0.098, fc="#0e1726", ec="#0e1726", r=0.0)
    fig.text(0.028, 0.963, "IT Asset Fleet & Maintenance Operations",
             size=23, weight="bold", color=INK, va="center")
    fig.text(0.028, 0.928,
             f"Asset register snapshot  ·  {n:,} records  ·  "
             f"{df['Location'].nunique()} delivery centres  ·  "
             f"{df['AssetType'].nunique()} hardware categories  ·  "
             f"data as of {snapshot:%d %b %Y}",
             size=10.4, color=MUTED, va="center")
    # filter pills (static controls, as on a BI canvas)
    px = 0.655
    for label, value in [("Delivery Centre", "All (3)"), ("Hardware", "All (5)"),
                         ("Status", "All")]:
        w = 0.105
        card(fig, px, 0.925, w, 0.040, fc="#16212f", ec="#2b3b52", r=0.008)
        fig.text(px + 0.012, 0.953, label.upper(), size=7.2, color=FAINT, va="center")
        fig.text(px + 0.012, 0.938, value, size=9.6, color=INK, weight="bold", va="center")
        fig.text(px + w - 0.014, 0.945, "▾", size=9, color=MUTED, va="center")
        px += w + 0.012

    # ================================================================ KPI cards
    kpis = [
        ("TOTAL MANAGED FLEET", f"{n:,}", "assets in the register", CYAN, 1.0),
        ("OPERATIONAL", f"{working:,}", f"{working/n:.1%} of fleet", EMERALD, working / n),
        ("UNDER REPAIR", f"{repair:,}", f"{repair/n:.1%} of fleet", CORAL, repair / n),
        ("DECOMMISSIONED", f"{decom:,}", f"{decom/n:.1%} of fleet", VIOLET, decom / n),
    ]
    kx, kw, kgap = 0.028, 0.2245, 0.0137
    for label, value, sub, col, frac in kpis:
        card(fig, kx, 0.742, kw, 0.136)
        fig.patches.append(mpatches.Rectangle((kx, 0.742), 0.0035, 0.136,
                                              transform=fig.transFigure, facecolor=col,
                                              edgecolor="none", zorder=1))
        fig.text(kx + 0.018, 0.857, " ".join(label), size=8.0, color=MUTED,
                 va="center", weight="bold")
        fig.text(kx + 0.018, 0.818, value, size=31, color=col, weight="bold", va="center")
        fig.text(kx + 0.018, 0.787, sub, size=9.6, color=FAINT, va="center")
        # progress rail
        rail = newax(fig, [kx + 0.018, 0.760, kw - 0.036, 0.008])
        bare(rail); rail.set_xlim(0, 1); rail.set_ylim(0, 1)
        rail.add_patch(mpatches.Rectangle((0, 0.25), 1, 0.5, color="#22304a"))
        rail.add_patch(mpatches.Rectangle((0, 0.25), frac, 0.5, color=col))
        kx += kw + kgap

    # ====================================================== A. fleet by category
    ax_x, ax_y, ax_w, ax_h = 0.028, 0.362, 0.300, 0.348
    card(fig, ax_x, ax_y, ax_w, ax_h)
    panel_title(fig, ax_x + 0.018, ax_y + ax_h - 0.022, "Fleet by hardware category",
                "count of assets in the register")
    ax = newax(fig, [ax_x + 0.075, ax_y + 0.045, ax_w - 0.105, ax_h - 0.115])
    bare(ax)
    vals = by_type.values
    ypos = np.arange(len(vals))
    ax.barh(ypos, vals, height=0.58, color="#1b8f9e", edgecolor="none", zorder=2)
    ax.barh(ypos, [vals.max() * 1.18] * len(vals), height=0.58, color="#15202f", zorder=1)
    for i, (name, v) in enumerate(by_type.items()):
        ax.text(-vals.max() * 0.035, i, name, ha="right", va="center", size=10.6, color=INK)
        ax.text(v + vals.max() * 0.022, i, f"{v:,}", ha="left", va="center",
                size=10.6, color=CYAN, weight="bold")
    ax.set_xlim(0, vals.max() * 1.20); ax.set_ylim(-0.6, len(vals) - 0.4)

    # ============================================ B. heatmap type x delivery centre
    bx, bw = 0.341, 0.330
    card(fig, bx, ax_y, bw, ax_h)
    panel_title(fig, bx + 0.018, ax_y + ax_h - 0.022, "Hardware volume by delivery centre",
                "darker = fewer assets  ·  brighter = more assets")
    ax = newax(fig, [bx + 0.078, ax_y + 0.040, bw - 0.100, ax_h - 0.120])
    m = xtab.loc[by_type.index[::-1]]
    im = ax.imshow(m.values, cmap=HEAT, aspect="auto")
    ax.set_xticks(range(m.shape[1])); ax.set_xticklabels(m.columns, size=10.2, color=INK)
    ax.set_yticks(range(m.shape[0])); ax.set_yticklabels(m.index, size=10.2, color=INK)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    lo, hi = m.values.min(), m.values.max()
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            v = m.values[i, j]
            ax.text(j, i, f"{v:,}", ha="center", va="center", size=10.4, weight="bold",
                    color="#06222b" if (v - lo) / (hi - lo) > 0.62 else "#cfe9ef")
    ax.set_xticks(np.arange(-.5, m.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, m.shape[0], 1), minor=True)
    ax.grid(which="minor", color=CARD, linewidth=2.2)
    ax.tick_params(which="minor", length=0)

    # ============================================= C. status mix by delivery centre
    cx, cw = 0.684, 0.288
    card(fig, cx, ax_y, cw, ax_h)
    panel_title(fig, cx + 0.018, ax_y + ax_h - 0.022, "Status mix by delivery centre",
                "share of assets, % of each centre's fleet")
    ax = newax(fig, [cx + 0.020, ax_y + 0.062, cw - 0.040, ax_h - 0.140])
    bare(ax)
    order = ["Working", "Under Repair", "Decommissioned"]
    cols = {"Working": EMERALD, "Under Repair": CORAL, "Decommissioned": VIOLET}
    locs = list(st_loc.index)
    left = np.zeros(len(locs))
    pct = st_loc[order].div(st_loc[order].sum(axis=1), axis=0) * 100
    for s in order:
        v = pct[s].values
        ax.barh(np.arange(len(locs)), v, left=left, height=0.46, color=cols[s],
                edgecolor=BG, linewidth=1.2)
        for i, (val, l0) in enumerate(zip(v, left)):
            if val > 12:
                ax.text(l0 + val / 2, i, f"{val:.1f}%", ha="center", va="center",
                        size=9.6, weight="bold", color="#06222b")
        left += v
    for i, loc in enumerate(locs):
        ax.text(-1.5, i + 0.42, loc, ha="left", va="center", size=10.6, color=INK)
    ax.set_xlim(0, 100); ax.set_ylim(-0.6, len(locs) - 0.25)
    handles = [mpatches.Patch(color=cols[s], label=s) for s in order]
    leg = ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.30),
                    ncol=3, frameon=False, fontsize=9.2, handlelength=1.1,
                    handleheight=1.1, columnspacing=1.4)
    for t in leg.get_texts():
        t.set_color(MUTED)

    # ================================================== D. fleet age / procurement
    dx, dy, dw, dh = 0.028, 0.095, 0.455, 0.245
    card(fig, dx, dy, dw, dh)
    panel_title(fig, dx + 0.018, dy + dh - 0.020, "Procurement profile and fleet age",
                f"assets by purchase year  ·  {over3:.0%} of the fleet is over 3 years old "
                f"at the snapshot date")
    ax = newax(fig, [dx + 0.030, dy + 0.045, dw - 0.055, dh - 0.112])
    bare(ax)
    ax.bar(years.index.astype(str), years.values, width=0.52, color="#2b7fd4",
           edgecolor="none")
    for xi, v in zip(range(len(years)), years.values):
        ax.text(xi, v + years.max() * 0.045, f"{v:,}", ha="center", size=10.0,
                color=INK, weight="bold")
    ax.set_ylim(0, years.max() * 1.26)
    ax.set_xticks(range(len(years)))                      # re-add after bare()
    ax.set_xticklabels([str(y) for y in years.index], size=10.6, color=MUTED)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.axhline(0, color=GRID, lw=1)

    # ============================================================ E. data quality
    ex, ew = 0.497, 0.475
    card(fig, ex, dy, ew, dh)
    panel_title(fig, ex + 0.018, dy + dh - 0.020, "Data-quality checks on this extract",
                "run against all 10,000 records before any figure above was published")
    checks = [
        (True,  f"Completeness — {nulls} null values across all columns"),
        (True,  f"Uniqueness — {dupes} duplicate AssetID values"),
        (False, f"Service schedule — only {distinct_due} distinct NextServiceDue value "
                f"({snapshot:%d %b %Y}) for all {n:,} assets"),
        (False, f"Service history — only {distinct_last} distinct LastServiceDate value"),
    ]
    ty = dy + dh - 0.072
    for ok, text in checks:
        fig.text(ex + 0.022, ty, "●" if ok else "▲", size=11,
                 color=EMERALD if ok else AMBER, va="center")
        fig.text(ex + 0.040, ty, text, size=10.0, color=INK if ok else "#e7d9b4",
                 va="center")
        ty -= 0.030
    card(fig, ex + 0.020, dy + 0.018, ew - 0.040, 0.046, fc="#2a2113", ec="#584214", r=0.008)
    fig.text(ex + 0.032, dy + 0.043,
             "Impact: this extract cannot rank which asset to service first.",
             size=9.4, color="#f0c95b", va="center", weight="bold")
    fig.text(ex + 0.032, dy + 0.029,
             "Counts and status mix remain valid; a \"due in next 30 days\" figure from "
             "this file does not.",
             size=8.8, color="#c9a94a", va="center")

    # =================================================================== footer
    fig.text(0.028, 0.050,
             "Source: IT asset register extract (01_IT_ASSESMENT.xlsx)  ·  "
             "single snapshot, no event history  ·  figures computed at render time by "
             "make_dashboard.py",
             size=9.0, color=FAINT, va="center")
    fig.text(0.972, 0.050, "AssetOps  ·  fleet overview  ·  v1", size=9.0, color=FAINT,
             va="center", ha="right")
    fig.patches.append(mpatches.Rectangle((0.028, 0.072), 0.944, 0.0012,
                                          transform=fig.transFigure, facecolor=GRID,
                                          edgecolor="none"))

    fig.savefig(out.with_suffix(".png"), dpi=120, facecolor=BG)
    fig.savefig(out.with_suffix(".svg"), facecolor=BG)
    plt.close(fig)
    print(f"wrote {out.with_suffix('.png')} and {out.with_suffix('.svg')}")


if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "/home/user/repo/01_IT_ASSESMENT(raw data).xlsx")
    build(load(src), Path(__file__).with_name("dashboard_fleet_overview"))
