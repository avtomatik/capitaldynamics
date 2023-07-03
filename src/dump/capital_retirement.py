
from core.constants import DATA_CAPITAL_RETIREMENT
from run_capital import run_capital_retirement

DATA_CAPITAL_RETIREMENT


def gate(df, start, stop):
    df.reset_index(level=0, inplace=True)
    df['Period'] = df['Period'].astype(int)

    # =============================================================================
    # Investment
    # =============================================================================
    I = df.iloc[:, 1].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
    # =============================================================================
    # Product
    # =============================================================================
    Y = df.iloc[:, 3]
    YN = df.iloc[:, 2]
    # =============================================================================
    # Max: Product
    # =============================================================================
    YM = df.iloc[:, 3].mul(100).div(df.iloc[:, 4])
    # =============================================================================
    # Capital, End-Period, Not Adjusted
    # =============================================================================
    C = df.iloc[:, 6].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
    L = df.iloc[:, 7]
    T = T[start:stop].reset_index(drop=True)
    I = I[start:stop].reset_index(drop=True)
    Y = Y[start:stop].reset_index(drop=True)
    YN = YN[start:stop].reset_index(drop=True)
    YM = YM[start:stop].reset_index(drop=True)
    C = C[start:stop].reset_index(drop=True)
    L = L[start:stop].reset_index(drop=True)
    run_capital_retirement(I, Y, YN, C, L)
    run_capital_retirement(I, YM, YN, C, L)


df = combine_capital_combined_archived()
# start = 22  # 1951
# start = 38  # 1967
# stop = 83  # 2011
gate(df, 38, 83)
