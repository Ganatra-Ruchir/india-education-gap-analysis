"""
India Education & Literacy Gap Analysis
=======================================

Loads the education dataset, cleans it, runs a set of analyses, and writes
chart images + a findings summary to the outputs/ folder.

Run:
    python src/generate_sample_data.py   # first, to create the sample CSV
    python src/analysis.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "india_education_sample.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 120


def load_and_clean() -> pd.DataFrame:
    """Load the CSV and apply basic cleaning / validation."""
    df = pd.read_csv(DATA)

    # Standardise text
    df["state"] = df["state"].str.strip().str.title()

    # Drop impossible values (defensive cleaning even on clean-ish data)
    df = df[(df["literacy_overall"].between(0, 100))]
    df = df[(df["dropout_rate_secondary"].between(0, 100))]

    # Ensure correct dtypes
    df["year"] = df["year"].astype(int)

    return df.reset_index(drop=True)


def latest_year(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["year"] == df["year"].max()].copy()


def chart_literacy_ranking(df: pd.DataFrame) -> None:
    """Bar chart: states ranked by overall literacy (latest year)."""
    latest = latest_year(df).sort_values("literacy_overall", ascending=True)
    plt.figure(figsize=(9, 8))
    plt.barh(latest["state"], latest["literacy_overall"], color=sns.color_palette("crest", len(latest)))
    plt.xlabel("Overall literacy rate (%)")
    plt.title(f"Literacy rate by state — {int(df['year'].max())}", fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT / "01_literacy_ranking.png")
    plt.close()


def chart_gender_gap(df: pd.DataFrame) -> None:
    """Bar chart: male-female literacy gap by state (latest year)."""
    latest = latest_year(df).sort_values("gender_gap", ascending=False)
    plt.figure(figsize=(9, 8))
    colors = ["#c0392b" if g > latest["gender_gap"].median() else "#e67e22"
              for g in latest["gender_gap"]]
    plt.barh(latest["state"][::-1], latest["gender_gap"][::-1], color=colors[::-1])
    plt.xlabel("Male minus female literacy (percentage points)")
    plt.title(f"Gender gap in literacy — {int(df['year'].max())}", fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT / "02_gender_gap.png")
    plt.close()


def chart_dropout_vs_ptr(df: pd.DataFrame) -> None:
    """Scatter: does a higher pupil-teacher ratio track higher dropout?"""
    latest = latest_year(df)
    plt.figure(figsize=(8, 6))
    sns.regplot(data=latest, x="pupil_teacher_ratio", y="dropout_rate_secondary",
                scatter_kws={"s": 60}, line_kws={"color": "#c0392b"})
    for _, r in latest.iterrows():
        plt.annotate(r["state"], (r["pupil_teacher_ratio"], r["dropout_rate_secondary"]),
                     fontsize=7, alpha=0.7)
    plt.xlabel("Pupil-teacher ratio")
    plt.ylabel("Secondary dropout rate (%)")
    plt.title("Crowded classrooms vs dropout", fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT / "03_dropout_vs_ptr.png")
    plt.close()


def chart_literacy_trend(df: pd.DataFrame) -> None:
    """Line chart: literacy trend over time for a few contrasting states."""
    focus = ["Kerala", "Bihar", "Rajasthan", "Tamil Nadu", "Uttar Pradesh"]
    sub = df[df["state"].isin(focus)]
    plt.figure(figsize=(9, 6))
    for state, g in sub.groupby("state"):
        g = g.sort_values("year")
        plt.plot(g["year"], g["literacy_overall"], marker="o", label=state)
    plt.xlabel("Year")
    plt.ylabel("Overall literacy rate (%)")
    plt.title("Literacy trajectory, selected states", fontweight="bold")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "04_literacy_trend.png")
    plt.close()


def write_findings(df: pd.DataFrame) -> None:
    """Compute headline numbers and save a short findings file."""
    latest = latest_year(df)
    yr = int(df["year"].max())

    top = latest.nlargest(3, "literacy_overall")[["state", "literacy_overall"]]
    bottom = latest.nsmallest(3, "literacy_overall")[["state", "literacy_overall"]]
    widest_gap = latest.nlargest(3, "gender_gap")[["state", "gender_gap"]]
    corr = latest["pupil_teacher_ratio"].corr(latest["dropout_rate_secondary"])

    lines = [
        f"# Key findings ({yr})",
        "",
        "> Numbers below come from the SYNTHETIC sample dataset. Replace the data",
        "> with official sources before citing any figure publicly.",
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
        "## Classroom crowding vs dropout",
        f"Correlation (pupil-teacher ratio vs secondary dropout): {corr:.2f}",
        "A positive value suggests more crowded classrooms tend to coincide with",
        "higher dropout — a lever policymakers can act on by hiring teachers.",
        "",
        f"## National snapshot",
        f"Mean literacy across states: {latest['literacy_overall'].mean():.1f}%",
        f"Mean gender gap: {latest['gender_gap'].mean():.1f} points",
        f"Mean secondary dropout: {latest['dropout_rate_secondary'].mean():.1f}%",
    ]
    (OUT / "findings.md").write_text("\n".join(lines))
    print("\n".join(lines))


def main() -> None:
    df = load_and_clean()
    print(f"Loaded {len(df)} rows across {df['state'].nunique()} states "
          f"and years {sorted(df['year'].unique())}\n")
    chart_literacy_ranking(df)
    chart_gender_gap(df)
    chart_dropout_vs_ptr(df)
    chart_literacy_trend(df)
    write_findings(df)
    print(f"\nCharts and findings written to {OUT}/")


if __name__ == "__main__":
    main()
