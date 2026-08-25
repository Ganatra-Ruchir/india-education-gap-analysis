"""
India Education & Literacy Gap Analysis
=======================================

Loads real 2015-16 UDISE state-level data, cleans it, runs a set of analyses,
and writes chart images + a findings summary to the outputs/ folder.

This is a single-year cross-section (2015-16), not a multi-year trend --
see docs/DATA_SOURCES.md and docs/METHODOLOGY.md for what that does and
does not support.

Run:
    python src/analysis.py
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from data import load_states

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

# ---- shared style --------------------------------------------------------
# A validated categorical palette (CVD-safe adjacent pairs) rather than a
# default seaborn cycle. See docs/METHODOLOGY.md for why these two charts
# are dumbbell/emphasis forms instead of plain bars.
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
SURFACE = "#fcfcfb"
BLUE = "#2a78d6"     # series slot 1 -- primary accent
RED = "#e34948"      # series slot 8 -- "needs attention" accent
MAGENTA = "#e87ba4"  # series slot 5 -- second dumbbell series

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": AXIS,
    "axes.labelcolor": INK_SECONDARY,
    "axes.grid": True,
    "axes.axisbelow": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": INK_SECONDARY,
    "font.family": "sans-serif",
    "figure.dpi": 130,
})


def _finish(fig, path, title, subtitle=None):
    # Fixed inch-based offsets from the top so title/subtitle spacing stays
    # consistent across figures of different heights (a figure-fraction
    # offset would overlap on shorter figures).
    h = fig.get_size_inches()[1]
    fig.text(0.02, 1 - 0.3 / h, title, fontsize=14, fontweight="bold", color=INK, ha="left", va="top")
    if subtitle:
        fig.text(0.02, 1 - 0.58 / h, subtitle, fontsize=9.5, color=MUTED, ha="left", va="top")
    top_margin = 1 - 0.85 / h
    fig.tight_layout(rect=[0, 0, 1, top_margin])
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)


def chart_literacy_ranking(df) -> None:
    """Emphasis bar chart: states ranked by literacy, top/bottom 3 highlighted."""
    d = df.sort_values("literacy_rate", ascending=True).reset_index(drop=True)
    mean = d["literacy_rate"].mean()

    top3 = set(d.nlargest(3, "literacy_rate")["state"])
    bottom3 = set(d.nsmallest(3, "literacy_rate")["state"])
    colors = [BLUE if s in top3 else RED if s in bottom3 else "#c7c6bf" for s in d["state"]]

    fig, ax = plt.subplots(figsize=(9, 10.5))
    bars = ax.barh(d["state"], d["literacy_rate"], color=colors, height=0.62, zorder=3)
    ax.axvline(mean, color=MUTED, linewidth=1, zorder=2)
    ax.text(mean, len(d) - 0.3, f" national avg {mean:.0f}%", fontsize=8.5,
            color=MUTED, va="bottom")

    for bar, state, val in zip(bars, d["state"], d["literacy_rate"]):
        if state in top3 or state in bottom3:
            ax.text(val + 0.6, bar.get_y() + bar.get_height() / 2, f"{val:.0f}%",
                    va="center", fontsize=9, color=INK, fontweight="bold")

    ax.set_xlabel("Overall literacy rate (%)")
    ax.set_xlim(0, 105)
    ax.tick_params(axis="y", labelsize=8.5)
    ax.grid(axis="y", visible=False)
    _finish(fig, OUT / "01_literacy_ranking.png",
            "Literacy rate by state",
            "2011 Census figures, via UDISE 2015-16  ·  highest and lowest 3 states highlighted")


def chart_gender_gap(df) -> None:
    """Dumbbell chart: male vs. female literacy per state, sorted by gap."""
    d = df.sort_values("gender_gap", ascending=True).reset_index(drop=True)
    y = np.arange(len(d))

    fig, ax = plt.subplots(figsize=(9, 11))
    ax.hlines(y, d["female_literacy_rate"], d["male_literacy_rate"],
              color=AXIS, linewidth=1.6, zorder=2)
    ax.scatter(d["female_literacy_rate"], y, s=55, color=MAGENTA,
               edgecolor=SURFACE, linewidth=1.5, zorder=3, label="Female")
    ax.scatter(d["male_literacy_rate"], y, s=55, color=BLUE,
               edgecolor=SURFACE, linewidth=1.5, zorder=3, label="Male")

    widest = d.nlargest(3, "gender_gap")["state"]
    for state, gap, male in zip(d["state"], d["gender_gap"], d["male_literacy_rate"]):
        if state in set(widest):
            yi = d.index[d["state"] == state][0]
            ax.text(male + 1.5, yi, f"+{gap:.0f} pts", fontsize=8.5,
                    color=INK, fontweight="bold", va="center")

    ax.set_yticks(y)
    ax.set_yticklabels(d["state"], fontsize=8.5)
    ax.set_xlabel("Literacy rate (%)")
    ax.set_xlim(45, 105)
    ax.legend(loc="lower right", frameon=False, fontsize=9.5)
    _finish(fig, OUT / "02_gender_gap.png",
            "Male vs. female literacy, by state",
            "Sorted by gap, narrowest to widest  ·  widest 3 gaps labeled")


def chart_literacy_vs_gender_gap(df) -> None:
    """Scatter: does higher overall literacy track a smaller gender gap?"""
    corr = df["literacy_rate"].corr(df["gender_gap"])
    slope, intercept = np.polyfit(df["literacy_rate"], df["gender_gap"], 1)
    xs = np.array([df["literacy_rate"].min(), df["literacy_rate"].max()])

    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    ax.scatter(df["literacy_rate"], df["gender_gap"], s=60, color=BLUE,
               alpha=0.85, edgecolor=SURFACE, linewidth=1, zorder=3)
    ax.plot(xs, slope * xs + intercept, color=RED, linewidth=2, zorder=2)

    callouts = set(df.nlargest(2, "gender_gap")["state"]) | set(df.nsmallest(2, "literacy_rate")["state"]) \
        | set(df.nlargest(2, "literacy_rate")["state"])
    for _, r in df[df["state"].isin(callouts)].iterrows():
        ax.annotate(r["state"], (r["literacy_rate"], r["gender_gap"]),
                    fontsize=8.5, color=INK, xytext=(5, 4), textcoords="offset points")

    ax.text(0.03, 0.05, f"r = {corr:.2f}", transform=ax.transAxes,
            fontsize=11, fontweight="bold", color=RED)
    ax.set_xlabel("Overall literacy rate (%)")
    ax.set_ylabel("Gender gap (percentage points)")
    _finish(fig, OUT / "03_literacy_vs_gender_gap.png",
            "Higher-literacy states have smaller gender gaps",
            "Each point is one state  ·  labeled: widest gaps and literacy extremes")


def chart_ptr_vs_pass_rate(df) -> None:
    """Scatter: does a higher pupil-teacher ratio track a lower pass rate?"""
    d = df.dropna(subset=["class10_pass_rate"])
    corr = d["pupil_teacher_ratio"].corr(d["class10_pass_rate"])
    slope, intercept = np.polyfit(d["pupil_teacher_ratio"], d["class10_pass_rate"], 1)
    xs = np.array([d["pupil_teacher_ratio"].min(), d["pupil_teacher_ratio"].max()])

    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    ax.scatter(d["pupil_teacher_ratio"], d["class10_pass_rate"], s=60, color=BLUE,
               alpha=0.85, edgecolor=SURFACE, linewidth=1, zorder=3)
    ax.plot(xs, slope * xs + intercept, color=MUTED, linewidth=2, zorder=2)

    callouts = set(d.nlargest(2, "pupil_teacher_ratio")["state"]) \
        | set(d.nsmallest(2, "class10_pass_rate")["state"]) \
        | set(d.nlargest(2, "class10_pass_rate")["state"])
    for _, r in d[d["state"].isin(callouts)].iterrows():
        ax.annotate(r["state"], (r["pupil_teacher_ratio"], r["class10_pass_rate"]),
                    fontsize=8.5, color=INK, xytext=(5, 4), textcoords="offset points")

    ax.text(0.97, 0.93, f"r = {corr:.2f}  (no meaningful relationship)",
            transform=ax.transAxes, fontsize=10.5, fontweight="bold", color=MUTED,
            ha="right")
    ax.set_xlabel("Pupil-teacher ratio (secondary)")
    ax.set_ylabel("Class 10 board exam pass rate (%)")
    _finish(fig, OUT / "04_ptr_vs_pass_rate.png",
            "Classroom crowding vs. exam pass rate",
            "Each point is one state  ·  flat trend line — reported as a genuine null result")


def write_findings(df) -> None:
    """Compute headline numbers and save a short findings file."""
    top = df.nlargest(3, "literacy_rate")[["state", "literacy_rate"]]
    bottom = df.nsmallest(3, "literacy_rate")[["state", "literacy_rate"]]
    widest_gap = df.nlargest(3, "gender_gap")[["state", "gender_gap"]]

    lit_gap_corr = df["literacy_rate"].corr(df["gender_gap"])
    ptr_pass_corr = df["pupil_teacher_ratio"].corr(df["class10_pass_rate"])

    lines = [
        "# Key findings",
        "",
        "Data: 2015-16 UDISE state-level school census (literacy figures are "
        "from Census 2011, as reported in this release). See "
        "docs/DATA_SOURCES.md. Single-year cross-section, not a trend.",
        "",
        "## Highest literacy",
        top.to_string(index=False),
        "",
        "## Lowest literacy",
        bottom.to_string(index=False),
        "",
        "## Widest gender gap",
        widest_gap.to_string(index=False),
        "",
        "## Literacy vs. gender gap",
        f"Correlation (literacy rate vs. gender gap): {lit_gap_corr:.2f}",
        "Higher-literacy states tend to have meaningfully smaller male-female "
        "gaps -- literacy gains and gender parity move together in this data, "
        "they are not independent problems.",
        "",
        "## Classroom crowding vs. exam pass rate",
        f"Correlation (pupil-teacher ratio vs. Class 10 pass rate): {ptr_pass_corr:.2f}",
        "This is a weak/near-zero correlation. Unlike a popular assumption, "
        "this cross-section does not show crowded secondary classrooms "
        "tracking lower board-exam pass rates -- reported honestly as a null "
        "result rather than dropped or reframed to fit a stronger story.",
        "",
        "## Data notes",
        "- Telangana's literacy figures are missing in this release -- it "
        "split from Andhra Pradesh in 2014 and Census literacy was not yet "
        "separately reported for it here. Andhra Pradesh's exam figures in "
        "this file reflect only the post-bifurcation state.",
        "- Delhi shows zero students appeared for the Class 10 exam this "
        "cycle in the source data; its pass rate is reported as missing, "
        "not 0%.",
        f"- {len(df)} of India's 36 states/UTs are included after cleaning.",
    ]
    (OUT / "findings.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


def main() -> None:
    df = load_states()
    print(f"Loaded {len(df)} states/UTs\n")
    chart_literacy_ranking(df)
    chart_gender_gap(df)
    chart_literacy_vs_gender_gap(df)
    chart_ptr_vs_pass_rate(df)
    write_findings(df)
    print(f"\nCharts and findings written to {OUT}/")


if __name__ == "__main__":
    main()
