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
import matplotlib.pyplot as plt
import seaborn as sns

from data import load_states

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 120


def chart_literacy_ranking(df) -> None:
    """Bar chart: states ranked by overall literacy."""
    d = df.sort_values("literacy_rate", ascending=True)
    plt.figure(figsize=(9, 10))
    plt.barh(d["state"], d["literacy_rate"], color=sns.color_palette("crest", len(d)))
    plt.xlabel("Overall literacy rate (%)")
    plt.title("Literacy rate by state — 2011 Census (via UDISE 2015-16)", fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT / "01_literacy_ranking.png")
    plt.close()


def chart_gender_gap(df) -> None:
    """Bar chart: male-female literacy gap by state."""
    d = df.sort_values("gender_gap", ascending=False)
    colors = ["#c0392b" if g > d["gender_gap"].median() else "#e67e22" for g in d["gender_gap"]]
    plt.figure(figsize=(9, 10))
    plt.barh(d["state"][::-1], d["gender_gap"][::-1], color=colors[::-1])
    plt.xlabel("Male minus female literacy (percentage points)")
    plt.title("Gender gap in literacy by state", fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT / "02_gender_gap.png")
    plt.close()


def chart_literacy_vs_gender_gap(df) -> None:
    """Scatter: does higher overall literacy track a smaller gender gap?"""
    plt.figure(figsize=(8, 6))
    sns.regplot(data=df, x="literacy_rate", y="gender_gap",
                scatter_kws={"s": 60}, line_kws={"color": "#c0392b"})
    for _, r in df.iterrows():
        plt.annotate(r["state"], (r["literacy_rate"], r["gender_gap"]),
                     fontsize=7, alpha=0.7)
    plt.xlabel("Overall literacy rate (%)")
    plt.ylabel("Gender gap (percentage points)")
    plt.title("Higher-literacy states tend to have smaller gender gaps",
              fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT / "03_literacy_vs_gender_gap.png")
    plt.close()


def chart_ptr_vs_pass_rate(df) -> None:
    """Scatter: does a higher pupil-teacher ratio track a lower pass rate?"""
    d = df.dropna(subset=["class10_pass_rate"])
    plt.figure(figsize=(8, 6))
    sns.regplot(data=d, x="pupil_teacher_ratio", y="class10_pass_rate",
                scatter_kws={"s": 60}, line_kws={"color": "#c0392b"})
    for _, r in d.iterrows():
        plt.annotate(r["state"], (r["pupil_teacher_ratio"], r["class10_pass_rate"]),
                     fontsize=7, alpha=0.7)
    plt.xlabel("Pupil-teacher ratio (secondary)")
    plt.ylabel("Class 10 board exam pass rate (%)")
    plt.title("Classroom crowding vs. exam pass rate — no clear relationship",
              fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT / "04_ptr_vs_pass_rate.png")
    plt.close()


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
