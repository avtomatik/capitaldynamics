import pandas as pd


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
    df['__deflator'] = df.iloc[:, columns[0]].div(
        df.iloc[:, columns[-1]]
    ).sub(1).abs()
    # =========================================================================
    # Basic Year
    # =========================================================================
    return int(df.index[df.iloc[:, -1].astype(float).argmin()])
