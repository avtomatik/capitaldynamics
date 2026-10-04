from pathlib import Path

import matplotlib.pyplot as plt

from ..domain.retirement import RetirementResult


def figures(result: RetirementResult) -> list[plt.Figure]:
    d = result.data
    years = d["year"]
    figs = []
    specs = [
        ("Product", years, d["real_gdp"], "Period", "Product"),
        ("Capital", years, d["real_capital"], "Period", "Capital"),
        (
            "Fixed Assets Turnover",
            years,
            d["capital_turnover"],
            "Period",
            "Fixed Assets Turnover",
        ),
        (
            "Investment to GDP Ratio",
            years,
            d["investment_to_output"],
            "Period",
            "Investment / GDP",
        ),
        (
            "Fixed Assets Retirement Ratio",
            years,
            d["retirement_ratio"],
            "Period",
            "Retirement Ratio",
        ),
    ]
    for title, x, y, xlabel, ylabel in specs:
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
        ax.grid()
        figs.append(fig)
    fig, ax = plt.subplots()
    ax.plot(d["retirement_ratio"], d["retirement_value"])
    ax.set(
        title="Retirement Ratio vs Retirement Value",
        xlabel="Retirement Ratio",
        ylabel="Retirement Value",
    )
    ax.grid()
    figs.append(fig)
    fig, ax = plt.subplots()
    ax.plot(d["capital_intensity"], d["labor_productivity"])
    ax.set(
        title="Labor Capital Intensity vs Labor Productivity",
        xlabel="Labor Capital Intensity",
        ylabel="Labor Productivity",
    )
    ax.grid()
    figs.append(fig)
    return figs


def save(
    figures_list: list[plt.Figure],
    directory: str | Path,
    stem: str = "retirement",
) -> None:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for i, fig in enumerate(figures_list, 1):
        fig.savefig(
            directory / f"{stem}_{i:02d}.png", dpi=160, bbox_inches="tight"
        )
