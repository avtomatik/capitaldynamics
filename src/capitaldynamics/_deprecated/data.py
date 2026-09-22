import pandas as pd

from capitaldynamics._deprecated.sources import SERIES_IDS
from capitaldynamics.data.sources import (BEA_NIPA_URL,
                                          FED_CAPACITY_UTILIZATION_SERIES)


def combine_capital_combined_archived() -> pd.DataFrame:
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17()
            .loc[:, [FED_CAPACITY_UTILIZATION_SERIES]]
            .dropna(axis=0),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            stockpile_usa_bea(
                {
                    "H4313C0": BEA_NIPA_URL,
                    "J4313C0": BEA_NIPA_URL,
                    "A4313C0": BEA_NIPA_URL,
                    "N4313C0": BEA_NIPA_URL,
                }
            ).pipe(transform_mean, name="bea_labor_mfg"),
            # =================================================================
            # For Overall Labor Series, See: A4601C0, 1929--2020
            # =================================================================
            stockpile_usa_bea({"A4601C": BEA_NIPA_URL}),
        ],
        axis=1,
        sort=True,
    ).dropna(axis=0)


def combine_local() -> pd.DataFrame:
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            stockpile_usa_bea(
                {
                    "H4313C0": BEA_NIPA_URL,
                    "J4313C0": BEA_NIPA_URL,
                    "A4313C0": BEA_NIPA_URL,
                    "N4313C0": BEA_NIPA_URL,
                }
            ).pipe(transform_mean, name="bea_labor_mfg"),
            read_usa_frb_g17()
            .loc[:, [FED_CAPACITY_UTILIZATION_SERIES]]
            .dropna(axis=0),
        ],
        axis=1,
        sort=True,
    ).dropna(axis=0)


def strip_deflator(df: pd.DataFrame, col_num: int) -> pd.DataFrame:
    return df.iloc[:, (col_num,)].dropna(axis=0).pct_change().dropna(axis=0)


def transform_local(df: pd.DataFrame) -> pd.DataFrame:
    SERIES_IDS_TO_USE = [
        "A006RC",
        "A191RC",
        "A191RX",
        "prod_max",
        "k1n31gd1es00",
        "bea_labor_mfg",
    ]
    df["prod_max"] = (
        df.loc[:, "A191RX"]
        .div(df.loc[:, FED_CAPACITY_UTILIZATION_SERIES])
        .mul(100)
    )
    return df.loc[:, SERIES_IDS_TO_USE]


def get_price_base_nr(df: pd.DataFrame, columns: tuple[int] = (0, 1)) -> int:
    """
    Determine Base Year

    Parameters
    ----------
    df : pd.DataFrame
        ======================== ===========================
        df.index                 Period
        ...                      ...
        df.iloc[:, columns[0]]   Nominal
        df.iloc[:, columns[-1]]  Real
        ======================== ===========================
    columns : tuple[int], optional
        Column Nominal, Column Real. The default is (0, 1).

    Returns
    -------
    int
        Base Year.

    """
    df["__deflator"] = (
        df.iloc[:, columns[0]].div(df.iloc[:, columns[-1]]).sub(1).abs()
    )
    # =========================================================================
    # Basic Year
    # =========================================================================
    return int(df.index[df.iloc[:, -1].astype(float).argmin()])
