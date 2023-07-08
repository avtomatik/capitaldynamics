import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from core.tools import get_price_base_nr


def plot_capital_acquisition(df: pd.DataFrame) -> None:
    """
    Interactive Shell for Processing Capital Acquisitions
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal Investment
        df.iloc[:, 1]      Nominal Production
        df.iloc[:, 2]      Real Production
        df.iloc[:, 3]      Maximum Real Production
        df.iloc[:, 4]      Nominal Capital
        df.iloc[:, 5]      Labor
        ================== =================================
    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.
    """
    _df = df.reset_index(level=0).copy()
    _df.columns = ('period', *_df.columns[1:])
    # =========================================================================
    # Basic Year
    # =========================================================================
    _b = _df.pipe(get_price_base_nr, columns=(2, 3))
    _df.drop(_df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    _df['c_turnover'] = _df.iloc[:, 3].div(_df.iloc[:, 5])
    # =========================================================================
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I_0/Y_0)
    # =========================================================================
    _df['inv_to_gdp'] = _df.iloc[:, 1].div(_df.iloc[:, 3])
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    _df['lab_cap_int'] = _df.iloc[:, 5].div(_df.iloc[:, 6])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    _df['lab_product'] = _df.iloc[:, 3].div(_df.iloc[:, 6])
    _df.iloc[:, -3:] = _df.iloc[:, -3:].div(_df.iloc[0, -3:])
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    # =========================================================================
    _df[f'{_df.columns[-2]}_log_bas'] = np.log(_df.iloc[:, -2].astype(float))
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    # =========================================================================
    _df[f'{_df.columns[-2]}_log_bas'] = np.log(_df.iloc[:, -2].astype(float))
    # =========================================================================
    # Max: Fixed Assets Turnover Ratio
    # =========================================================================
    _df[f'{_df.columns[-6]}_max'] = _df.iloc[:, 4].div(_df.iloc[:, 5])
    # =========================================================================
    # Max: Investment to Gross Domestic Product Ratio
    # =========================================================================
    _df[f'{_df.columns[-6]}_max'] = _df.iloc[:, 1].div(_df.iloc[:, 4])
    # =========================================================================
    # Max: Labor Productivity
    # =========================================================================
    _df[f'{_df.columns[-5]}_max'] = _df.iloc[:, 4].div(_df.iloc[:, 6])
    _df.iloc[:, -2:] = _df.iloc[:, -2:].div(_df.iloc[0, -2:])
    # =========================================================================
    # Max: Log Labor Productivity
    # =========================================================================
    _df[f'{_df.columns[-1]}_log_bas'] = np.log(_df.iloc[:, -1].astype(float))
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Line Spans for Pi (N, N >= 1): '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 1, f'N >= 1 is Required, N = {N} Was Provided'
    # =========================================================================
    # Pi & Pi Switch Points
    # =========================================================================
    pi, _knots = [], [0]
    _ = 0
    if N == 1:
        _knots.append(_df.index[-1])
        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
            _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _] - 1, 0]))))
    elif N >= 2:
        while _ < N:
            if 1 + _ == N:
                _knots.append(_df.index[-1])
                pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _] - 1, 0]))))
            else:
                _knot = int(input('Select Row for Year, Should Be More Than {}: = {}: '.format(
                    0, _df.iloc[0, 0])))
                if _knot > _knots[_]:
                    _knots.append(_knot)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
            _ += 1
    else:
        print("Error")
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    _calculated = [np.nan]
    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1 + j]):
            # =================================================================
            # Estimate: GCF[-] or CA[+]
            # =================================================================
            _calculated.append(
                _df.iloc[1 + i, 5] - _df.iloc[i, 5] + pi[j]*_df.iloc[1 + i, 1]
            )
    else:
        for j in range(N):
            if 1 + j == N:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================
                    _calculated.append(
                        _df.iloc[1 + i, 5] - _df.iloc[i, 5] +
                        pi[j]*_df.iloc[1 + i, 1]
                    )
            else:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================
                    _calculated.append(
                        _df.iloc[1 + i, 5] - _df.iloc[i, 5] +
                        pi[j]*_df.iloc[1 + i, 1]
                    )
    _df = pd.concat(
        [
            _df,
            pd.DataFrame(_calculated, columns=['_calculated'])
        ],
        axis=1)
    _df.set_index(_df.columns[0], inplace=True)
    # =========================================================================
    # {
    #     '-': 'Gross Capital Formation',
    #     '+': 'Capital Acquisitions'
    # }
    # =========================================================================
    for _ in range(N):
        if 1 + _ == N:
            print(
                f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _] - 1]}: {pi[_]:.6f}'
            )
            continue
        print(
            f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _]]}: {pi[_]:.6f}'
        )
    plt.figure(1)
    plt.plot(_df.iloc[:, 8], _df.iloc[:, 9])
    plt.plot(_df.iloc[:, 8], _df.iloc[:, 14])
    plt.title(
        'Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel(f'Labor Productivity, {_b}=100')
    plt.grid()
    plt.figure(2)
    plt.plot(_df.iloc[:, 10], _df.iloc[:, 11])
    plt.plot(_df.iloc[:, 10], _df.iloc[:, 15])
    plt.title(
        'Log Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Log Labor Capital Intensity')
    plt.ylabel(f'Log Labor Productivity, {_b}=100')
    plt.grid()
    plt.figure(3)
    plt.plot(_df.iloc[:, 6])
    plt.plot(_df.iloc[:, 12])
    plt.title(
        'Fixed Assets Turnover ($\\lambda$), Observed & Max, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover ($\\lambda$), {_b}=100')
    plt.grid()
    plt.figure(4)
    plt.plot(_df.iloc[:, 7])
    plt.plot(_df.iloc[:, 13])
    plt.title(
        'Investment to Gross Domestic Product Ratio,\nObserved & Max, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(
        f'Investment to Gross Domestic Product Ratio, {_b}=100')
    plt.grid()
    plt.figure(5)
    plt.plot(_df.iloc[:, 16])
    plt.title(
        'Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'GCF or CA, {_b}=100')
    plt.grid()
    plt.show()


def plot_capital_retirement(df: pd.DataFrame) -> None:
    """
    Interactive Shell for Processing Capital Retirement
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal Investment
        df.iloc[:, 1]      Nominal Production
        df.iloc[:, 2]      Real Production
        df.iloc[:, 3]      Nominal Capital
        df.iloc[:, 4]      Labor
        ================== =================================
    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.
    """
    _df = df.reset_index(level=0).copy()
    _df.columns = ('period', *_df.columns[1:])
    # =========================================================================
    # Define Basic Year for Deflator
    # =========================================================================
    # =========================================================================
    # Basic Year
    # =========================================================================
    _b = _df.pipe(get_price_base_nr, columns=(2, 3))
    _df.drop(_df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    _df['lab_cap_int_log_bas'] = _df.iloc[:, 4].div(_df.iloc[:, 5])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    _df['lab_product_log_bas'] = _df.iloc[:, 3].div(_df.iloc[:, 5])
    # =========================================================================
    # Investment to Gross Domestic Product Ratio
    # =========================================================================
    _df['inv_to_gdp'] = _df.iloc[:, 1].div(_df.iloc[:, 3])
    # =========================================================================
    # Basing
    # =========================================================================
    _df.iloc[:, -3:] = _df.iloc[:, -3:].div(_df.iloc[0, -3:])
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    # =========================================================================
    _df.iloc[:, -3] = np.log(_df.iloc[:, -3].astype(float))
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    # =========================================================================
    _df.iloc[:, -2] = np.log(_df.iloc[:, -2].astype(float))
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    _df['c_turnover'] = _df.iloc[:, 3].div(_df.iloc[:, 4])
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Line Segments for Pi: '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 1, f'N >= 1 is Required, N = {N} Was Provided'
    # =========================================================================
    # Pi & Pi Switch Points
    # =========================================================================
    pi, _knots = [], [0]
    _ = 0
    if N == 1:
        _knots.append(_df.index[-1])
        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
            _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
    elif N >= 2:
        while _ < N:
            if 1 + _ == N:
                _knots.append(_df.index[-1])
                pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
            else:
                _knot = int(input('Select Row for Year: '))
                if _knot > _knots[_]:
                    _knots.append(_knot)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
            _ += 1
    else:
        print("Error")
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    # =========================================================================
    # Fixed Assets Retirement Value
    # =========================================================================
    _value = [np.nan]
    # =========================================================================
    # Fixed Assets Retirement Ratio
    # =========================================================================
    _ratio = [np.nan]
    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1 + j]):
            # =================================================================
            # Fixed Assets Retirement Value
            # =================================================================
            _value.append(
                _df.iloc[i, 4] - _df.iloc[1 + i, 4] + pi[j]*_df.iloc[i, 1]
            )
            # =================================================================
            # Fixed Assets Retirement Ratio
            # =================================================================
            _ratio.append(
                (_df.iloc[i, 4] - _df.iloc[1 + i, 4] + pi[j]
                 * _df.iloc[i, 1]) / _df.iloc[1 + i, 4]
            )
    else:
        for j in range(N):
            if 1 + j == N:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Fixed Assets Retirement Value
                    # =========================================================
                    _value.append(
                        _df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                        pi[j]*_df.iloc[i, 1]
                    )
                    # =========================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================
                    _ratio.append(
                        (_df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                         pi[j]*_df.iloc[i, 1]) / _df.iloc[1 + i, 4]
                    )
            else:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Fixed Assets Retirement Value
                    # =========================================================
                    _value.append(
                        _df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                        pi[j]*_df.iloc[i, 1]
                    )
                    # =========================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================
                    _ratio.append(
                        (_df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                         pi[j]*_df.iloc[i, 1]) / _df.iloc[1 + i, 4]
                    )
    _df = pd.concat(
        [
            _df,
            pd.DataFrame(_value, columns=['_value']),
            pd.DataFrame(_ratio, columns=['_ratio'])
        ],
        axis=1
    )
    _df.set_index(_df.columns[0], inplace=True)
    _df['_ratio_deviation_abs'] = _df.iloc[:, 10].sub(
        _df.iloc[:, 10].mean()).abs()
    _df['_ratio_increment_abs'] = _df.iloc[:, 10].diff().abs()
    for _ in range(N):
        if 1 + _ == N:
            print(
                f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _] - 1]}: {pi[_]:.6f}'
            )
            continue
        print(
            f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _]]}: {pi[_]:.6f}'
        )
    plt.figure(1)
    plt.title('Product, {}=100, {}$-${}'.format(_b, *df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel(f'Product, {_b}=100')
    plt.plot(_df.iloc[:, 2])
    plt.grid()
    plt.figure(2)
    plt.title('Capital, {}=100, {}$-${}'.format(_b, *df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel(f'Capital, {_b}=100')
    plt.plot(_df.iloc[:, 3])
    plt.grid()
    plt.figure(3)
    plt.title(
        'Fixed Assets Turnover ($\\lambda$), {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover ($\\lambda$), {_b}=100')
    plt.plot(_df.iloc[:, 2].div(_df.iloc[:, 3]))
    plt.grid()
    plt.figure(4)
    plt.title(
        'Investment to Gross Domestic Product Ratio, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(
        f'Investment to Gross Domestic Product Ratio, {_b}=100'
    )
    plt.plot(_df.iloc[:, 7])
    plt.grid()
    plt.figure(5)
    plt.title(
        '$\\alpha(t)$, Fixed Assets Retirement Ratio, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'$\\alpha(t)$, {_b}=100')
    plt.plot(_df.iloc[:, 9])
    plt.grid()
    plt.figure(6)
    plt.title(
        'Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel(f'$\\alpha(t)$, {_b}=100')
    plt.ylabel(f'Fixed Assets Retirement Value, {_b}=100')
    plt.plot(_df.iloc[:, 9], _df.iloc[:, 8])
    plt.grid()
    plt.figure(7)
    plt.title(
        'Labor Capital Intensity, {}=100, {}$-${}'.format(_b, *df.index[[0, -1]]))
    plt.xlabel(f'Labor Capital Intensity, {_b}=100')
    plt.ylabel(f'Labor Productivity, {_b}=100')
    plt.plot(np.exp(_df.iloc[:, 5]), np.exp(_df.iloc[:, 6]))
    plt.grid()
    plt.show()
