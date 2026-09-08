from pathlib import Path

import matplotlib.pyplot as plt

from ..domain.acquisition import AcquisitionResult


def figures(result: AcquisitionResult) -> list[plt.Figure]:
    d = result.data
    years = d["period"]
    figs = []

    fig, ax = plt.subplots()
    ax.plot(d["capital_intensity"], d["labor_productivity"], label="Observed")
    ax.plot(
        d["capital_intensity"],
        d["maximum_labor_productivity"],
        label="Maximum",
    )
    ax.set(
        title="Labor Productivity, Observed & Maximum",
        xlabel="Labor Capital Intensity",
        ylabel="Labor Productivity",
    )
    ax.grid()
    ax.legend()
    figs.append(fig)

    fig, ax = plt.subplots()
    ax.plot(
        d["log_capital_intensity"],
        d["log_labor_productivity"],
        label="Observed",
    )
    ax.plot(
        d["log_capital_intensity"],
        d["maximum_log_labor_productivity"],
        label="Maximum",
    )
    ax.set(
        title="Log Labor Productivity, Observed & Maximum",
        xlabel="Log Labor Capital Intensity",
        ylabel="Log Labor Productivity",
    )
    ax.grid()
    ax.legend()
    figs.append(fig)

    fig, ax = plt.subplots()
    ax.plot(years, d["capital_turnover"], label="Observed")
    ax.plot(years, d["maximum_capital_turnover"], label="Maximum")
    ax.set(
        title="Fixed Assets Turnover",
        xlabel="Period",
        ylabel="Fixed Assets Turnover",
    )
    ax.grid()
    ax.legend()
    figs.append(fig)

    fig, ax = plt.subplots()
    ax.plot(years, d["investment_to_output"], label="Observed")
    ax.plot(years, d["maximum_investment_to_output"], label="Maximum")
    ax.set(
        title="Investment to GDP Ratio",
        xlabel="Period",
        ylabel="Investment / GDP",
    )
    ax.grid()
    ax.legend()
    figs.append(fig)

    fig, ax = plt.subplots()
    ax.plot(years, d["capital_acquisition"])
    ax.set(
        title="Gross Capital Formation / Capital Acquisitions Estimate",
        xlabel="Period",
        ylabel="Estimate",
    )
    ax.grid()
    figs.append(fig)

    return figs


def save(
    figures_list: list[plt.Figure],
    directory: str | Path,
    stem: str = "acquisition",
) -> None:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for i, fig in enumerate(figures_list, 1):
        fig.savefig(
            directory / f"{stem}_{i:02d}.png", dpi=160, bbox_inches="tight"
        )
