from capitaldynamics.data.loader import load_data

from .visualization import plot_capital_acquisition

COLUMNS = [
    "real_investment",
    "nominal_gdp",
    "real_gdp",
    "full_capacity_real_gdp",
    "real_fixed_assets",
    "manufacturing_labor",
]


def main() -> None:
    data = load_data()
    data.loc[:, COLUMNS].pipe(plot_capital_acquisition)


if __name__ == "__main__":
    main()
