import numpy as np
import pandas as pd
from matplotlib.figure import Figure

from capitaldynamics.visualization.common import (
    add_reference_year,
    finish_axis,
)


def create_retirement_figures(
    source: pd.DataFrame,
    result: pd.DataFrame,
    *,
    deflator_base_year: int,
) -> dict[str, Figure]:
    """Construct the seven retirement charts without loading or saving data."""
    import matplotlib.pyplot as plt

    years = result["year"].to_numpy(dtype=int)
    first_year, last_year = int(years[0]), int(years[-1])

    def reference(label):
        return add_reference_year(
            label, deflator_base_year, first_year, last_year
        )

    figures: dict[str, Figure] = {}
    fig, ax = plt.subplots()
    ax.plot(years, source["real_gdp"].to_numpy(dtype=float))
    finish_axis(
        ax,
        title=reference("Real gross domestic product"),
        xlabel="Year",
        ylabel="Real GDP",
    )
    figures["real_output"] = fig
    fig, ax = plt.subplots()
    ax.plot(years, source["real_fixed_assets"].to_numpy(dtype=float))
    finish_axis(
        ax,
        title=reference("Real fixed assets"),
        xlabel="Year",
        ylabel="Real fixed assets",
    )
    figures["real_capital"] = fig
    fig, ax = plt.subplots()
    ax.plot(years, result["fixed_assets_turnover"])
    finish_axis(
        ax,
        title=reference("Fixed-assets turnover"),
        xlabel="Year",
        ylabel="Real GDP / real fixed assets",
    )
    figures["fixed_assets_turnover"] = fig
    fig, ax = plt.subplots()
    ax.plot(years, result["investment_output_index"])
    finish_axis(
        ax,
        title=reference("Investment-to-output ratio"),
        xlabel="Year",
        ylabel="Relative investment / output index",
    )
    figures["investment_output_ratio"] = fig
    fig, ax = plt.subplots()
    ax.plot(years, result["retirement_ratios"])
    finish_axis(
        ax,
        title=reference("Fixed-assets retirement ratio"),
        xlabel="Year",
        ylabel="Retirement value / end-period capital",
    )
    figures["retirement_ratio"] = fig
    fig, ax = plt.subplots()
    ax.plot(result["retirement_ratios"], result["retirement_values"])
    finish_axis(
        ax,
        title=reference("Retirement value and retirement ratio"),
        xlabel="Retirement ratio",
        ylabel="Retirement value",
    )
    figures["retirement_value_vs_ratio"] = fig
    fig, ax = plt.subplots()
    ax.plot(
        np.exp(result["log_capital_intensity"]),
        np.exp(result["log_labor_productivity"]),
    )
    finish_axis(
        ax,
        title=reference("Labor capital intensity and labor productivity"),
        xlabel="Labor capital intensity (index)",
        ylabel="Labor productivity (index)",
    )
    figures["labor_intensity_productivity"] = fig
    return figures
