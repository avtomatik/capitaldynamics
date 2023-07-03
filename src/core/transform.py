from pandas import DataFrame


def strip_deflator(df: DataFrame, col_num: int) -> DataFrame:
    return df.iloc[:, (col_num,)].dropna(axis=0).pct_change().dropna(axis=0)


def transform_local(df: DataFrame) -> DataFrame:
    SERIES_ID = 'CAPUTL.B50001.A'
    SERIES_IDS_TO_USE = [
        'A006RC', 'A191RC', 'A191RX', 'prod_max', 'k1n31gd1es00', 'bea_labor_mfg'
    ]
    df['prod_max'] = df.loc[:, 'A191RX'].div(df.loc[:, SERIES_ID]).mul(100)
    return df.loc[:, SERIES_IDS_TO_USE]
