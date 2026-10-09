from capitaldynamics.data.loader import load_data

from .visualization import plot_capital_retirement

COLUMNS = [
    "real_investment",
    "nominal_gdp",
    "real_gdp",
    "real_fixed_assets",
    "manufacturing_labor",
]

COLUMNS = [
    "real_investment",
    "full_capacity_nominal_gdp",
    "full_capacity_real_gdp",
    "real_fixed_assets",
    "manufacturing_labor",
]


def main() -> None:
    data = load_data()
    data.loc[:, COLUMNS].pipe(plot_capital_retirement)


if __name__ == "__main__":
    main()
