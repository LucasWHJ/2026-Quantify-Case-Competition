"""Publication figures from aggregate tables and explicit pilot assumptions."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from .pilot import Pilot

NAVY = "#13273B"
TEAL = "#087F8C"
CORAL = "#CB5652"
MUTED = "#687786"


def _style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.labelcolor": NAVY, "text.color": NAVY,
                         "axes.titleweight": "bold", "axes.titlepad": 15,
                         "savefig.facecolor": "white"})


def _save(fig, output, name, source):
    fig.text(0.02, 0.015, source, fontsize=8, color=MUTED)
    fig.tight_layout(rect=(0, .055, 1, 1))
    for suffix in ("png", "svg"):
        fig.savefig(output / f"{name}.{suffix}", dpi=180)
    plt.close(fig)


def generate_figures(tables, output):
    _style()
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    annual = tables["company_annual"]
    lines = tables["line_metrics"]
    cyber = lines[lines.line == "Cyber Liability"]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(annual.year, annual.combined_ratio, marker="o", color=TEAL, lw=2.5, label="Company")
    ax.plot(cyber.year, cyber.combined_ratio, marker="o", color=CORAL, lw=2.5, label="Cyber")
    ax.axhline(1, color=MUTED, ls="--", lw=1)
    ax.set(ylim=(.75, 1.04), xticks=annual.year, title="Profitable company, narrowing Cyber cushion",
           ylabel="Combined ratio", xlabel="Fiscal year")
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", alpha=.15)
    _save(fig, output, "underwriting-performance", "Source: Quantify 2026, Exhibit A. Amount-weighted company ratio. Investment income excluded.")

    severity = tables["severity_by_failure"].sort_values("mean_cad")
    labels = {"Autonomous System Failure": "Autonomous failure", "Privacy and Security": "Privacy / security",
              "Cyber Exploitation via AI": "AI cyber exploitation", "Algorithmic Bias": "Algorithmic bias",
              "Misinformation": "Misinformation", "Hallucinated Output": "Hallucinated output"}
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh([f"{labels[r.failure_type]} (n={r.n})" for r in severity.itertuples()],
                   severity.mean_cad / 1e6,
                   color=[CORAL if f == "Autonomous System Failure" else TEAL for f in severity.failure_type])
    ax.bar_label(bars, labels=[f"{v/1e6:.2f}" for v in severity.mean_cad], padding=7)
    ax.set(xlim=(0, 24), xlabel="Mean estimated insured loss (CAD millions)",
           title="Failure mechanisms have different estimated severity")
    ax.grid(axis="x", alpha=.12)
    ax.set_axisbelow(True)
    _save(fig, output, "severity-by-failure-type", "Source: Quantify 2026, Exhibit B, n=135 external incidents. Not TSI claims or incident frequencies.")

    a = tables["anova_order_sensitivity"]
    orders = list(a.order.unique())
    fig, ax = plt.subplots(figsize=(10, 4.8))
    palette = {"industry": "#86B5C0", "failure_type": TEAL, "human_oversight": "#DEA341", "Residual": "#DCE2E6"}
    titles = {"industry": "Industry", "failure_type": "Failure type", "human_oversight": "Oversight", "Residual": "Residual"}
    for j, order in enumerate(orders):
        left = 0
        for row in a[a.order == order].itertuples():
            value = row.share_of_total_log_variance
            ax.barh(j, value, left=left, color=palette[row.term], height=.5,
                    label=titles[row.term] if j == 0 else None)
            if value > .08:
                ax.text(left + value / 2, j, f"{value:.1%}", ha="center", va="center", color="white" if row.term == "failure_type" else NAVY)
            left += value
    ax.set(yticks=[0, 1], yticklabels=["Industry enters first", "Failure type enters first"],
           xlim=(0, 1), xlabel="Share of total log-loss variance", title="Sequential variance shares depend on model order")
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(.5, -.2))
    _save(fig, output, "model-order-sensitivity", "Source: Exhibit B log-loss OLS, same additive variables in two orders. Shares are not causal contributions.")

    pilot_figures(output)


def pilot_figures(output):
    _style()
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    frequencies = np.linspace(0, .05, 101)
    fig, ax = plt.subplots(figsize=(10, 5.2))
    for severity, color in [(50_000, "#86B5C0"), (100_000, TEAL), (200_000, CORAL)]:
        ratios = [Pilot(claim_frequency=float(f), mean_covered_cost=severity).result()["combined_ratio"] for f in frequencies]
        ax.plot(frequencies, ratios, color=color, lw=2.4, label=f"CAD {severity:,.0f} mean covered cost")
    ax.axhline(1, color=MUTED, ls="--", lw=1)
    ax.scatter([.0275], [1], color=NAVY, zorder=3)
    ax.annotate("2.75% break-even at CAD 100k", xy=(.0275, 1), xytext=(.016, 1.65),
                arrowprops={"arrowstyle": "-", "color": MUTED}, fontsize=10)
    ax.set(title="Pilot economics change materially with frequency and covered cost",
           xlabel="Annual claims per policy", ylabel="Combined ratio", xlim=(0, .05))
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.legend(frameon=False, loc="upper left")
    ax.grid(alpha=.12)
    _save(fig, output, "pilot-sensitivity", "Illustration only: 100 policies, CAD 5k premium each, 25% variable expenses, CAD 100k fixed cost. See docs/pilot-design.md.")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    names = ["company_annual", "line_metrics", "severity_by_failure", "anova_order_sensitivity"]
    generate_figures({n: pd.read_csv(root / "data/processed" / f"{n}.csv") for n in names}, root / "figures")
