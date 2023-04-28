import pandas as pd

from capital_interactive.src.constants import SERIES_IDS
from thesis.src.lib.constants import SERIES_IDS_LAB
from thesis.src.lib.read import read_usa_frb_g17
from thesis.src.lib.stockpile import stockpile_usa_bea
from thesis.src.lib.transform import transform_mean


def combine_usa_bea_labor() -> pd.DataFrame:
    """
    Labor Series: A4601C0, 1929--2013
    """
    SERIES_IDS = {
        'A4601C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    return stockpile_usa_bea(SERIES_IDS)


def combine_capital_combined_archived() -> pd.DataFrame:
    SERIES_ID = 'CAPUTL.B50001.A'
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, [SERIES_ID]].dropna(axis=0),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name="bea_labor_mfg"),
            # =================================================================
            # For Overall Labor Series, See: A4601C0, 1929--2020
            # =================================================================
            combine_usa_bea_labor()
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)


def combine_local() -> pd.DataFrame:
    SERIES_ID = 'CAPUTL.B50001.A'
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name="bea_labor_mfg"
            ),
            read_usa_frb_g17().loc[:, [SERIES_ID]].dropna(axis=0),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
