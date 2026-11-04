import pandas as pd
from matplotlib.figure import Figure

from capitaldynamics.visualization.common import (
    add_reference_year,
    finish_axis,
)


def create_acquisition_figures(
    source: pd.DataFrame,
    result: pd.DataFrame,
    *,
    deflator_base_year: int,
) -> dict[str, Figure]:
    """Construct the five acquisition charts without loading or saving data."""
    import matplotlib.pyplot as plt

    years = result["year"].to_numpy(dtype=int)
    first_year, last_year = int(years[0]), int(years[-1])

    def reference(label):
        return add_reference_year(
            label, deflator_base_year, first_year, last_year
        )

    figures: dict[str, Figure] = {}
    fig, ax = plt.subplots()
    ax.plot(
        result["capital_intensity_index"],
        result["observed_labor_productivity"],
        label="Observed productivity",
    )
    ax.plot(
        result["capital_intensity_index"],
        result["full_capacity_labor_productivity"],
        label="Full-capacity productivity",
    )
    finish_axis(
        ax,
        title=reference("Labor productivity: observed and full capacity"),
        xlabel="Labor capital intensity (index)",
        ylabel="Labor productivity (index)",
    )
    ax.legend()
    figures["labor_productivity"] = fig
    fig, ax = plt.subplots()
    ax.plot(
        result["log_capital_intensity"],
        result["log_observed_productivity"],
        label="Observed productivity",
    )
    ax.plot(
        result["log_capital_intensity"],
        result["log_full_capacity_productivity"],
        label="Full-capacity productivity",
    )
    finish_axis(
        ax,
        title=reference("Log labor productivity: observed and full capacity"),
        xlabel="Log labor capital intensity",
        ylabel="Log labor productivity",
    )
    ax.legend()
    figures["log_labor_productivity"] = fig
    fig, ax = plt.subplots()
    ax.plot(
        years, result["observed_turnover"], label="Observed output / capital"
    )
    ax.plot(
        years,
        result["full_capacity_turnover"],
        label="Full-capacity output / capital",
    )
    finish_axis(
        ax,
        title=reference("Fixed-assets turnover"),
        xlabel="Year",
        ylabel="Output / capital",
    )
    ax.legend()
    figures["fixed_assets_turnover"] = fig
    fig, ax = plt.subplots()
    ax.plot(years, result["investment_output_index"], label="Observed output")
    ax.plot(
        years,
        result["full_capacity_investment_output_index"],
        label="Full-capacity output",
    )
    finish_axis(
        ax,
        title=reference(
            "Investment-to-output ratio: observed and full capacity"
        ),
        xlabel="Year",
        ylabel="Relative investment / output index",
    )
    ax.legend()
    figures["investment_output_ratio"] = fig
    fig, ax = plt.subplots()
    ax.plot(years, result["estimates"], label="Estimated capital acquisition")
    finish_axis(
        ax,
        title=reference(
            "Gross capital formation / capital acquisitions estimate"
        ),
        xlabel="Year",
        ylabel="Estimate (real units)",
    )
    ax.legend()
    figures["capital_acquisition_estimate"] = fig
    return figures
