from core.combine import combine_capital_combined_archived, combine_local
from core.plot import plot_capital_acquisition
from core.usa_capital_interactive import transform_call

# =============================================================================
# projectCapitalAcquisitions.py
# =============================================================================
'''Project: Capital Acquisitions'''


def transform_call(df):
    # df = combine_local().pipe(transform_local)
    _df = df.dropna()
    # =========================================================================
    # Investment
    # =========================================================================
    I = _df.iloc[:, 1].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    # =========================================================================
    # Product
    # =========================================================================
    Y = _df.iloc[:, 3]
    YN = _df.iloc[:, 2]
    # =========================================================================
    # Max: Product
    # =========================================================================
    YM = _df.iloc[:, 3].div(_df.iloc[:, 4]).mul(100)
    # =========================================================================
    # Fixed Assets, End-Period, Not Adjusted
    # =========================================================================
    C = _df.iloc[:, 6].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    L = _df.iloc[:, 7]
    plot_capital_acquisition(I, Y, YN, YM, C, L)


def cap_acq():
    # =========================================================================
    # 1967
    # =========================================================================
    # start = 38
    combine_capital_combined_archived().pipe(transform_call, start=38)
