import duckdb

from capitaldynamics._deprecated.paths import WAREHOUSE
from capitaldynamics._deprecated.visualization import plot_capital_retirement
from capitaldynamics._retired.visualization import plot_calculate_capital_aquisition

# =============================================================================
# Alpha: Capital Retirement Ratio
# Pi: Investment to Capital Conversion Ratio
# =============================================================================
# =============================================================================
# Project: Interactive Capital Acquisitions
# =============================================================================
# =============================================================================
# capital_acquisitions.yaml
# =============================================================================
# =============================================================================
# Project: Interactive Capital Retirement
# =============================================================================
# =============================================================================
# capital_retirement.yaml
# =============================================================================


with duckdb.connect(str(WAREHOUSE), read_only=True) as con:
    df = con.sql(
        """
        SELECT *
        FROM marts.capital_dynamics_archived
        ORDER BY year
        """
    ).df()

df = df.set_index("year")

df.loc[
    :,
    [
        "real_investment",
        "nominal_gdp",
        "real_gdp",
        "full_capacity_real_gdp",
        "real_fixed_assets",
        "manufacturing_labor",
    ],
].pipe(plot_calculate_capital_aquisition)

df.loc[
    :,
    [
        "real_investment",
        "nominal_gdp",
        "real_gdp",
        "real_fixed_assets",
        "manufacturing_labor",
    ],
].pipe(plot_capital_retirement)

df.loc[
    :,
    [
        "real_investment",
        "full_capacity_nominal_gdp",
        "full_capacity_real_gdp",
        "real_fixed_assets",
        "manufacturing_labor",
    ],
].pipe(plot_capital_retirement)
