import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def run_capital_retirement(period, investment, production, production_n, capital, labor):

    i = len(period)-1
    # if production==YM:

    while abs(production_n[i]-production[i]) > 1:
        i -= 1
    # =============================================================================
    # Basic Year
    # =============================================================================
        year_base = i

    # =============================================================================
    # Calculate Static Values
    # =============================================================================

    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    X01 = np.log(capital*labor[0]/(capital[0]*labor))
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    X02 = np.log(production*labor[0]/(production[0]*labor))
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    X03 = investment*production[0]/(investment[0]*production)
    # =============================================================================
    # Fixed Assets Turnover Ratio
    # =============================================================================
    X04 = production/capital

    # =============================================================================
    # Convert List to Dataframe
    # =============================================================================
    X01 = pd.DataFrame(X01, columns=['X01'])
    # =============================================================================
    # Convert List to Dataframe
    # =============================================================================
    X02 = pd.DataFrame(X02, columns=['X02'])
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Line Segments for Gamma: '))
    if N >= 1:
        print(f'Number of Spans Provided: {N}')
        # =========================================================================
        # Pi & Pi Switch Points
        # =========================================================================
        pi, _knots = [], [0]
        i = 0
        if N == 1:
            _knots.append(len(period)-1)
            pi.append(float(input('Define Gamma for Period from %d to %d: ' % (
                period[_knots[i]], period[_knots[1+i]]))))
        elif N >= 2:
            while i < N:
                if i == N-1:
                    _knots.append(len(period)-1)
                    pi.append(float(input('Define Gamma for Period from %d to %d: ' % (
                        period[_knots[i]], period[_knots[1+i]]))))
                    i += 1
                else:
                    y = int(input('Select Row for Year: '))
                    if y > _knots[i]:
                        _knots.append(y)
                        pi.append(float(input('Define Gamma for Period from %d to %d: ' % (
                            period[_knots[i]], period[_knots[1+i]]))))
                        i += 1
        else:
            print('Error')
        X05 = []
        X06 = []
    # =============================================================================
    # Fixed Assets Retirement Value
    # =============================================================================
        X05.append(np.nan)
    # =============================================================================
    # Fixed Assets Retirement Ratio
    # =============================================================================
        X06.append(np.nan)
        # =============================================================================
        # Calculate Dynamic Values
        # =============================================================================
        if N == 1:
            j = 0
            for i in range(_knots[j], _knots[1+j]):
                # Fixed Assets Retirement Value
                X05.append(capital[i]-capital[1+i]+pi[j]*investment[i])
                # Fixed Assets Retirement Ratio
                X06.append((capital[i]-capital[1+i]+pi[j]
                           * investment[i])/capital[1+i])
        else:
            for j in range(N):
                if j == N-1:
                    for i in range(_knots[j], _knots[1+j]):
                        # Fixed Assets Retirement Value
                        X05.append(capital[i]-capital[1+i] +
                                   pi[j]*investment[i])
                        # Fixed Assets Retirement Ratio
                        X06.append(
                            (capital[i]-capital[1+i]+pi[j]*investment[i])/capital[1+i])
                else:
                    for i in range(_knots[j], _knots[1+j]):
                        # Fixed Assets Retirement Value
                        X05.append(capital[i]-capital[1+i] +
                                   pi[j]*investment[i])
                        # Fixed Assets Retirement Ratio
                        X06.append(
                            (capital[i]-capital[1+i]+pi[j]*investment[i])/capital[1+i])
        X05 = pd.DataFrame(X05, columns=['X05'])  # Convert List to Dataframe
        X06 = pd.DataFrame(X06, columns=['X06'])  # Convert List to Dataframe
        df = pd.DataFrame(period, columns=['Period'])
        df = pd.concat(
            [df, X01, X02, X03, X04, X05, X06], axis=1)
        df.columns = ['Period', 'X01',
                      'X02', 'X03', 'X04', 'X05', 'X06']
        df['X07'] = df['X06']-df['X06'].mean()
        df['X07'] = df['X07'].abs()
        df['X08'] = df['X06'].diff()
        df['X08'] = df['X08'].abs()
        for i in range(N):
            if i == N-1:
                print('Model Parameter: Gamma for Period from %d to %d: %f' %
                      (period[_knots[i]], period[_knots[1+i]], pi[i]))
            else:
                print('Model Parameter: Gamma for Period from %d to %d: %f' %
                      (period[_knots[i]], period[_knots[1+i]], pi[i]))

        plt.figure(1)
        plt.title('Product, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel(f'Product, {year_base}=100')
        plt.plot(period, production)
        plt.grid()
        plt.figure(2)
        plt.title('Capital, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel(f'Capital, {year_base}=100')
        plt.plot(period, capital)
        plt.grid()
        plt.figure(3)
        plt.title('Fixed Assets Turnover, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel(f'Fixed Assets Turnover, {year_base}=100')
        plt.plot(period, production/capital)
        plt.grid()
        plt.figure(4)
        plt.title('Investment to GDP Ratio, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel(f'Investment to GDP Ratio, {year_base}=100')
        plt.plot(period, X03)
        plt.grid()
        plt.figure(5)
        plt.title('$\\mu(t)$, Fixed Assets Retirement Ratio, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel(f'$\\mu(t)$, {year_base}=100')
        plt.plot(period, X06)
        plt.grid()
        plt.figure(6)
        plt.title('Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel(f'$\\mu(t)$, {year_base}=100')
        plt.ylabel('Fixed Assets Retirement Value, %d=100' %
                   (year_base))
        plt.plot(X06, X05)
        plt.grid()
        plt.figure(7)
        plt.title('Labor Capital Intensity, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel(f'Labor Capital Intensity, {year_base}=100')
        plt.ylabel(f'Labor Productivity, {year_base}=100')
        plt.plot(np.exp(X01), np.exp(X02))
        plt.grid()
        # plt.legend()
        plt.show()

    else:
        print(f'N >= 1 is Required, N = {N} Was Provided')


def run_capital_acquisitions(period, investment, production, production_n, production_m, capital, labor, start):
    i = len(period)-1
    while abs(production_n[i]-production[i]) > 1:
        i -= 1
        year_base = i  # Basic Year
    # =============================================================================
    # Calculate Static Values
    # =============================================================================
    X01 = production/capital  # Fixed Assets Turnover Ratio
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    X02 = investment*production[start]/(investment[start]*production)
    # Labor Capital Intensity
    X03 = capital*labor[start]/(capital[start]*labor)
    X04 = production*labor[start] / \
        (production[start]*labor)  # Labor Productivity

    X05 = np.log(X03)  # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    X06 = np.log(X04)  # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    X07 = production_m/capital  # Max: Fixed Assets Turnover Ratio
    # Max: Investment to Gross Domestic Product Ratio
    X08 = investment*production_m[start]/(investment[start]*production_m)
    # Max: Labor Productivity
    X09 = production_m*labor[start]/(production_m[start]*labor)
    X10 = np.log(X09)  # Max: Log Labor Productivity

    X05 = pd.DataFrame(X05, columns=['X05'])  # Convert List to Dataframe
    X06 = pd.DataFrame(X06, columns=['X06'])  # Convert List to Dataframe
    X10 = pd.DataFrame(X10, columns=['X10'])  # Convert List to Dataframe
    # =============================================================================
    # Calculate Dynamic Values
    # =============================================================================
    N = int(input('Define Number of Line Segments for Gamma: ')
            )  # Number of Spans
    if N >= 1:
        print(f'Number of Spans Provided: {N}')
        pi, _knots = [], []  # Gamma Switch Points & Gamma
        _knots.append(start)
        i = 0
        if N == 1:
            _knots.append(len(period)-1)
            pi.append(float(input('Define Gamma for Period from %d to %d: ' % (
                period[_knots[i]], period[_knots[1+i]-1]))))
        elif N >= 2:
            while i < N:
                if i == N-1:
                    _knots.append(len(period)-1)
                    pi.append(float(input('Define Gamma for Period from %d to %d: ' % (
                        period[_knots[i]], period[_knots[1+i]-1]))))
                    i += 1
                else:
                    y = int(input('Select Row for Year, Should Be More Than %d:=%d: ' % (
                        start, period[start])))
                    if y > _knots[i]:
                        _knots.append(y)
                        pi.append(float(input('Define Gamma for Period from %d to %d: ' % (
                            period[_knots[i]], period[_knots[1+i]]))))
                        i += 1
        else:
            print('Error')
        X11 = []
        for i in range(1+start):
            X11.append(np.nan)
        if N == 1:
            j = 0
            for i in range(_knots[j], _knots[1+j]):
                # Estimate: GCF[-] or CA[+]
                X11.append(capital[1+i]-capital[i]+pi[j]*investment[1+i])
        else:
            for j in range(N):
                if j == N-1:
                    for i in range(_knots[j], _knots[1+j]):
                        # Estimate: GCF[-] or CA[+]
                        X11.append(capital[1+i]-capital[i] +
                                   pi[j]*investment[1+i])
                else:
                    for i in range(_knots[j], _knots[1+j]):
                        # Estimate: GCF[-] or CA[+]
                        X11.append(capital[1+i]-capital[i] +
                                   pi[j]*investment[1+i])
        X11 = pd.DataFrame(X11, columns=['X11'])  # Convert List to Dataframe
        df = pd.DataFrame(period, columns=['Period'])
        df = pd.concat(
            [df, X01, X02, X03, X04, X05, X06, X07, X08, X09, X10, X11], axis=1)
        df.columns = ['Period', 'X01', 'X02', 'X03',
                      'X04', 'X05', 'X06', 'X07', 'X08', 'X09', 'X10', 'X11']
    # [-] Gross Capital Formation
    # [+] Capital Acquisitions
        for i in range(N):
            if i == N-1:
                print('Model Parameter: Gamma for Period from %d to %d: %f' %
                      (period[_knots[i]], period[_knots[1+i]-1], pi[i]))
            else:
                print('Model Parameter: Gamma for Period from %d to %d: %f' %
                      (period[_knots[i]], period[_knots[1+i]], pi[i]))

        plt.figure(1)
        plt.plot(X03, X04)
        plt.plot(X03, X09)
        plt.title('Labor Productivity, Observed & Max, %d=100, %d$-$%d' %
                  (year_base, period[_knots[0]], period[_knots[N]-1]))
        plt.xlabel('Labor Capital Intensity')
        plt.ylabel(f'Labor Productivity, {year_base}=100')
        plt.grid()
        plt.figure(2)
        plt.plot(X05, X06)
        plt.plot(X05, X10)
        plt.title('Log Labor Productivity, Observed & Max, %d=100, %d$-$%d' %
                  (year_base, period[_knots[0]], period[_knots[N]-1]))
        plt.xlabel('Log Labor Capital Intensity')
        plt.ylabel(f'Log Labor Productivity, {year_base}=100')
        plt.grid()
        plt.figure(3)
        plt.plot(period, X01)
        plt.plot(period, X07)
        plt.title('Fixed Assets Turnover, Observed & Max, %d=100, %d$-$%d' %
                  (year_base, period[_knots[0]], period[_knots[N]-1]))
        plt.xlabel('Period')
        plt.ylabel(f'Fixed Assets Turnover, {year_base}=100')
        plt.grid()
        plt.figure(4)
        plt.plot(period, X02)
        plt.plot(period, X08)
        plt.title('Investment to Gross Domestic Product Ratio,\nObserved & Max, %d=100, %d$-$%d' %
                  (year_base, period[_knots[0]], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio, %d=100' %
                   (year_base))
        plt.grid()
        plt.figure(5)
        plt.plot(period, X11)
        plt.title('Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), %d=100, %d$-$%d' %
                  (year_base, period[_knots[0]], period[_knots[N]-1]))
        plt.xlabel('Period')
        plt.ylabel(f'GCF or CA, {year_base}=100')
        plt.grid()
        plt.show()
    else:
        print(f'N >= 1 is Required, N = {N} Was Provided')


# =============================================================================
# projectCapitalRetirement.py
# =============================================================================


def run_capital_retirement_x(period, investment, production, production_n, capital, labor):
    # =============================================================================
    # Y05.append(capital[1+i]-capital[i]+gmm[j]*investment[1+i])
    # =============================================================================
    # =============================================================================
    # Y06.append((capital[1+i]-capital[i]+gmm[j]*investment[1+i])/capital[1+i])
    # =============================================================================
    # =============================================================================
    # Replaced with
    # =============================================================================
    # =============================================================================
    # Y05.append(capital[i]-capital[1+i]+gmm[j]*investment[i])
    # =============================================================================
    # =============================================================================
    # Y06.append((capital[i]-capital[1+i]+gmm[j]*investment[i])/capital[1+i])
    # =============================================================================
    # =============================================================================
    # Define Basic Year for Deflator
    # =============================================================================
    i = len(period)-1
    while abs(production_n[i]-production[i]) > 1:
        i -= 1
        year_base = i  # Basic Year
    # =============================================================================
    # Calculate Static Values
    # =============================================================================

    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    Y01 = np.log(capital*labor[0]/(capital[0]*labor))
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    Y02 = np.log(production*labor[0]/(production[0]*labor))
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    Y03 = investment*production[0]/(investment[0]*production)
    Y04 = production/capital  # Fixed Assets Turnover Ratio
    Y01 = pd.DataFrame(Y01, columns=['Y01'])  # Convert List to Dataframe
    Y02 = pd.DataFrame(Y02, columns=['Y02'])  # Convert List to Dataframe
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Line Segments for Gamma: '))
    if N >= 1:
        print(f'Number of Spans Provided: {N}')
        # =========================================================================
        # Pi & Pi Switch Points
        # =========================================================================
        pi, _knots = [], [0]
        i = 0
        if N == 1:
            _knots.append(len(period)-1)
            pi.append(float(input('Define Gamma for Period from %d to %d: ' % (
                period[_knots[i]], period[_knots[1+i]]))))
        elif N >= 2:
            while i < N:
                if i == N-1:
                    _knots.append(len(period)-1)
                    pi.append(float(input('Define Gamma for Period from %d to %d: ' % (
                        period[_knots[i]], period[_knots[1+i]]))))
                    i += 1
                else:
                    y = int(input('Select Row for Year: '))
                    if y > _knots[i]:
                        _knots.append(y)
                        pi.append(float(input('Define Gamma for Period from %d to %d: ' % (
                            period[_knots[i]], period[_knots[1+i]]))))
                        i += 1
        else:
            print('Error')
        Y05 = []
        Y06 = []
        Y05.append(np.nan)  # Fixed Assets Retirement Value
        Y06.append(np.nan)  # Fixed Assets Retirement Ratio
        # =============================================================================
        # Calculate Dynamic Values
        # =============================================================================
        if N == 1:
            j = 0
            for i in range(_knots[j], _knots[1+j]):
                # Fixed Assets Retirement Value
                Y05.append(capital[i]-capital[1+i]+pi[j]*investment[i])
                # Fixed Assets Retirement Ratio
                Y06.append((capital[i]-capital[1+i]+pi[j]
                           * investment[i])/capital[1+i])
        else:
            for j in range(N):
                if j == N-1:
                    for i in range(_knots[j], _knots[1+j]):
                        # Fixed Assets Retirement Value
                        Y05.append(capital[i]-capital[1+i] +
                                   pi[j]*investment[i])
                        # Fixed Assets Retirement Ratio
                        Y06.append(
                            (capital[i]-capital[1+i]+pi[j]*investment[i])/capital[1+i])
                else:
                    for i in range(_knots[j], _knots[1+j]):
                        # Fixed Assets Retirement Value
                        Y05.append(capital[i]-capital[1+i] +
                                   pi[j]*investment[i])
                        # Fixed Assets Retirement Ratio
                        Y06.append(
                            (capital[i]-capital[1+i]+pi[j]*investment[i])/capital[1+i])
        Y05 = pd.DataFrame(Y05, columns=['Y05'])  # Convert List to Dataframe
        Y06 = pd.DataFrame(Y06, columns=['Y06'])  # Convert List to Dataframe
        df = pd.DataFrame(period, columns=['Period'])
        df = pd.concat(
            [
                df,
                Y01, Y02, Y03, Y04, Y05, Y06
            ],
            axis=1
        )
        df.columns = ['Period', 'Y01', 'Y02', 'Y03', 'Y04', 'Y05', 'Y06']
        df['Y07'] = df['Y06']-df['Y06'].mean()
        df['Y07'] = df['Y07'].abs()
        df['Y08'] = df['Y06'].diff()
        df['Y08'] = df['Y08'].abs()
        for i in range(N):
            if i == N-1:
                print('Model Parameter: Gamma for Period from %d to %d: %f' %
                      (period[_knots[i]], period[_knots[1+i]], pi[i]))
            else:
                print('Model Parameter: Gamma for Period from %d to %d: %f' %
                      (period[_knots[i]], period[_knots[1+i]], pi[i]))

        plt.figure(1)
        plt.title('Product, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel(f'Product, {year_base}=100')
        plt.plot(period, production)
        plt.grid()
        plt.figure(2)
        plt.title('Capital, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel(f'Capital, {year_base}=100')
        plt.plot(period, capital)
        plt.grid()
        plt.figure(3)
        plt.title('Fixed Assets Turnover, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel(f'Fixed Assets Turnover, {year_base}=100')
        plt.plot(period, production/capital)
        plt.grid()
        plt.figure(4)
        plt.title('Investment to Gross Domestic Product Ratio, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio, %d=100' %
                   (year_base))
        plt.plot(period, Y03)
        plt.grid()
        plt.figure(5)
        plt.title('$\\mu(t)$, Fixed Assets Retirement Ratio, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel('Period')
        plt.ylabel(f'$\\mu(t)$, {year_base}=100')
        plt.plot(period, Y06)
        plt.grid()
        plt.figure(6)
        plt.title('Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel(f'$\\mu(t)$, {year_base}=100')
        plt.ylabel('Fixed Assets Retirement Value, %d=100' %
                   (year_base))
        plt.plot(Y06, Y05)
        plt.grid()
        plt.figure(7)
        plt.title('Labor Capital Intensity, %d=100, %d$-$%d' %
                  (year_base, period[0], period[_knots[N]]))
        plt.xlabel(f'Labor Capital Intensity, {year_base}=100')
        plt.ylabel(f'Labor Productivity, {year_base}=100')
        plt.plot(np.exp(Y01), np.exp(Y02))
        plt.grid()
        # plt.legend()
        plt.show()
    else:
        print(f'N >= 1 is Required, N = {N} Was Provided')


def calculate_capital_aquisition(_df):
    """
    _df.iloc[:, 0]: Period
    _df.iloc[:, 1]: Nominal Investment
    _df.iloc[:, 2]: Nominal Production
    _df.iloc[:, 3]: Real Production
    _df.iloc[:, 4]: Maximum Real Production
    _df.iloc[:, 5]: Nominal Capital
    _df.iloc[:, 6]: Labor
    """
    _ = _df.shape[0]-1
    while abs(_df.iloc[_, 2]-_df.iloc[_, 3]) > 1:
        _ -= 1
        year_base = _  # Basic Year
    """Calculate Static Values"""
    XAA = _df.iloc[:, 3].div(_df.iloc[:, 5])  # Fixed Assets Turnover Ratio
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    XBB = _df.iloc[:, 1].div(_df.iloc[:, 3])
    XCC = _df.iloc[:, 5].div(_df.iloc[:, 6])  # Labor Capital Intensity
    XDD = _df.iloc[:, 3].div(_df.iloc[:, 6])  # Labor Productivity
    XBB = XBB.div(XBB[0])
    XCC = XCC.div(XCC[0])
    XDD = XDD.div(XDD[0])
    XEE = np.log(XCC)  # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    XFF = np.log(XDD)  # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    # Max: Fixed Assets Turnover Ratio
    XGG = _df.iloc[:, 4].div(_df.iloc[:, 5])
    # Max: Investment to Gross Domestic Product Ratio
    XHH = _df.iloc[:, 1].div(_df.iloc[:, 4])
    XII = _df.iloc[:, 4].div(_df.iloc[:, 6])  # Max: Labor Productivity
    XHH = XHH.div(XHH[0])
    XII = XII.div(XII[0])
    XJJ = np.log(XII)  # Max: Log Labor Productivity
    XEE = pd.DataFrame(XEE, columns=['XEE'])  # Convert List to Dataframe
    XFF = pd.DataFrame(XFF, columns=['XFF'])  # Convert List to Dataframe
    XJJ = pd.DataFrame(XJJ, columns=['XJJ'])  # Convert List to Dataframe
    """Calculate Dynamic Values"""
    N = int(input('Define Number of Line Segments for Pi: '))  # Number of Spans
    if N >= 1:
        print(f'Number of Spans Provided: {N}')
        # =========================================================================
        # Pi & Pi Switch Points
        # =========================================================================
        pi, _knots = [], [0]
        _ = 0
        if N == 1:
            _knots.append(_df.shape[0]-1)
            pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                _df.iloc[_knots[_], 0], _df.iloc[_knots[1+_]-1, 0]))))
        elif N >= 2:
            while _ < N:
                if _ == N-1:
                    _knots.append(_df.shape[0]-1)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        _df.iloc[_knots[_], 0], _df.iloc[_knots[1+_]-1, 0]))))
                    _ += 1
                else:
                    y = int(input('Select Row for Year, Should Be More Than {}: = {}: '.format(
                        0, _df.iloc[0, 0])))
                    if y > _knots[_]:
                        _knots.append(y)
                        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                            _df.iloc[_knots[_], 0], _df.iloc[_knots[1+_], 0]))))
                        _ += 1
        else:
            print('Error')
        XKK = []
        for _ in range(1):
            XKK.append(np.nan)
        if N == 1:
            j = 0
            for _ in range(_knots[j], _knots[1+j]):
                # Estimate: GCF[-] or CA[+]
                XKK.append(_df.iloc[1+_, 5] -
                           _df.iloc[_, 5]+pi[j]*_df.iloc[1+_, 1])
        else:
            for j in range(N):
                if j == N-1:
                    for _ in range(_knots[j], _knots[1+j]):
                        # Estimate: GCF[-] or CA[+]
                        XKK.append(
                            _df.iloc[1+_, 5]-_df.iloc[_, 5]+pi[j]*_df.iloc[1+_, 1])
                else:
                    for _ in range(_knots[j], _knots[1+j]):
                        # Estimate: GCF[-] or CA[+]
                        XKK.append(
                            _df.iloc[1+_, 5]-_df.iloc[_, 5]+pi[j]*_df.iloc[1+_, 1])
        XKK = pd.DataFrame(XKK, columns=['XKK'])  # Convert List to Dataframe
        df = pd.DataFrame(_df.iloc[:, 0], columns=['Period'])
        df = pd.concat(
            [df, XAA, XBB, XCC, XDD, XEE, XFF, XGG, XHH, XII, XJJ, XKK], axis=1)
        df.columns = ['Period', 'XAA', 'XBB', 'XCC',
                      'XDD', 'XEE', 'XFF', 'XGG', 'XHH', 'XII', 'XJJ', 'XKK']
        """
        `-` Gross Capital Formation
        `+` Capital Acquisitions
        """
        for _ in range(N):
            if _ == N-1:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1+_]-1, 0], pi[_]))
            else:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1+_], 0], pi[_]))
        plt.figure(1)
        plt.plot(XCC, XDD)
        plt.plot(XCC, XII)
        plt.title('Labor Productivity, Observed & Max, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[_knots[0], 0], _df.iloc[_knots[N]-1, 0]))
        plt.xlabel('Labor Capital Intensity')
        plt.ylabel('Labor Productivity, {} = 100'.format(
            _df.iloc[year_base, 0]))
        plt.grid()
        plt.figure(2)
        plt.plot(XEE, XFF)
        plt.plot(XEE, XJJ)
        plt.title('Log Labor Productivity, Observed & Max, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[_knots[0], 0], _df.iloc[_knots[N]-1, 0]))
        plt.xlabel('Log Labor Capital Intensity')
        plt.ylabel('Log Labor Productivity, {} = 100'.format(
            _df.iloc[year_base, 0]))
        plt.grid()
        plt.figure(3)
        plt.plot(_df.iloc[:, 0], XAA)
        plt.plot(_df.iloc[:, 0], XGG)
        plt.title('Fixed Assets Turnover ($\\lambda$), Observed & Max, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[_knots[0], 0], _df.iloc[_knots[N]-1, 0]))
        plt.xlabel('Period')
        plt.ylabel('Fixed Assets Turnover ($\\lambda$), {} = 100'.format(
            _df.iloc[year_base, 0]))
        plt.grid()
        plt.figure(4)
        plt.plot(_df.iloc[:, 0], XBB)
        plt.plot(_df.iloc[:, 0], XHH)
        plt.title('Investment to Gross Domestic Product Ratio, \nObserved & Max, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[_knots[0], 0], _df.iloc[_knots[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio, {} = 100'.format(
            _df.iloc[year_base, 0]))
        plt.grid()
        plt.figure(5)
        plt.plot(_df.iloc[:, 0], XKK)
        plt.title('Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[_knots[0], 0], _df.iloc[_knots[N]-1, 0]))
        plt.xlabel('Period')
        plt.ylabel('GCF or CA, {} = 100'.format(_df.iloc[year_base, 0]))
        plt.grid()
        plt.show()
    else:
        print(f'N >= 1 is Required, N = {N} Was Provided')


def calculate_capital_retirement(_df):
    """
    _df.iloc[:, 0]: Period
    _df.iloc[:, 1]: Nominal Investment
    _df.iloc[:, 2]: Nominal Production
    _df.iloc[:, 3]: Real Production
    _df.iloc[:, 4]: Nominal Capital
    _df.iloc[:, 5]: Labor
    """
    """Define Basic Year for Deflator"""
    _ = _df.shape[0]-1
    while abs(_df.iloc[_, 2]-_df.iloc[_, 3]) > 1:
        _ -= 1
        year_base = _  # Basic Year
    """Calculate Static Values"""
    YAA = _df.iloc[:, 4].div(_df.iloc[:, 5])
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    YAA = np.log(YAA.div(YAA[0]))
    YBB = _df.iloc[:, 3].div(_df.iloc[:, 5])
    YBB = np.log(YBB.div(YBB[0]))  # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    YCC = _df.iloc[:, 1].div(_df.iloc[:, 3])
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    YCC = YCC.div(YCC[0])
    YDD = _df.iloc[:, 3].div(_df.iloc[:, 4])  # Fixed Assets Turnover Ratio
    YAA = pd.DataFrame(YAA, columns=['YAA'])  # Convert List to Dataframe
    YBB = pd.DataFrame(YBB, columns=['YBB'])  # Convert List to Dataframe
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Line Segments for Pi: '))
    if N >= 1:
        print(f'Number of Spans Provided: {N}')
        # =========================================================================
        # Pi & Pi Switch Points
        # =========================================================================
        pi, _knots = [], [0]
        _ = 0
        if N == 1:
            _knots.append(_df.shape[0]-1)
            pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                _df.iloc[_knots[_], 0], _df.iloc[:, 0][_knots[1+_]]))))
        elif N >= 2:
            while _ < N:
                if _ == N-1:
                    _knots.append(_df.shape[0]-1)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        _df.iloc[_knots[_], 0], _df.iloc[_knots[1+_], 0]))))
                    _ += 1
                else:
                    y = int(input('Select Row for Year: '))
                    if y > _knots[_]:
                        _knots.append(y)
                        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                            _df.iloc[_knots[_], 0], _df.iloc[_knots[1+_], 0]))))
                        _ += 1
        else:
            print('Error')
        YEE = []
        YFF = []
        YEE.append(np.nan)  # Fixed Assets Retirement Value
        YFF.append(np.nan)  # Fixed Assets Retirement Ratio
        """Calculate Dynamic Values"""
        if N == 1:
            j = 0
            for _ in range(_knots[j], _knots[1+j]):
                # Fixed Assets Retirement Value
                YEE.append(_df.iloc[_, 4] -
                           _df.iloc[1+_, 4]+pi[j]*_df.iloc[_, 1])
                # Fixed Assets Retirement Ratio
                YFF.append((_df.iloc[_, 4]-_df.iloc[1+_, 4] +
                           pi[j]*_df.iloc[_, 1])/_df.iloc[1+_, 4])
        else:
            for j in range(N):
                if j == N-1:
                    for _ in range(_knots[j], _knots[1+j]):
                        # Fixed Assets Retirement Value
                        YEE.append(
                            _df.iloc[_, 4]-_df.iloc[1+_, 4]+pi[j]*_df.iloc[_, 1])
                        # Fixed Assets Retirement Ratio
                        YFF.append(
                            (_df.iloc[_, 4]-_df.iloc[1+_, 4]+pi[j]*_df.iloc[_, 1])/_df.iloc[1+_, 4])
                else:
                    for _ in range(_knots[j], _knots[1+j]):
                        # Fixed Assets Retirement Value
                        YEE.append(
                            _df.iloc[_, 4]-_df.iloc[1+_, 4]+pi[j]*_df.iloc[_, 1])
                        # Fixed Assets Retirement Ratio
                        YFF.append(
                            (_df.iloc[_, 4]-_df.iloc[1+_, 4]+pi[j]*_df.iloc[_, 1])/_df.iloc[1+_, 4])
        YEE = pd.DataFrame(YEE, columns=['YEE'])  # Convert List to Dataframe
        YFF = pd.DataFrame(YFF, columns=['YFF'])  # Convert List to Dataframe
        df = pd.DataFrame(_df.iloc[:, 0], columns=['Period'])
        df = pd.concat(
            [df, YAA, YBB, YCC, YDD, YEE, YFF],
            axis=1,
            sort=True
        )
        df.columns = ['Period', 'YAA',
                      'YBB', 'YCC', 'YDD', 'YEE', 'YFF']
        df['YGG'] = df['YFF']-df['YFF'].mean()
        df['YGG'] = df['YGG'].abs()
        df['YHH'] = df['YFF'].diff()
        df['YHH'] = df['YHH'].abs()
        for _ in range(N):
            if _ == N-1:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1+_], 0], pi[_]))
            else:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1+_], 0], pi[_]))
        plt.figure(1)
        plt.title('Product, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[0, 0], _df.iloc[_knots[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Product, {} = 100'.format(_df.iloc[year_base, 0]))
        plt.plot(_df.iloc[:, 0], _df.iloc[:, 3])
        plt.grid()
        plt.figure(2)
        plt.title('Capital, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[0, 0], _df.iloc[_knots[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Capital, {} = 100'.format(_df.iloc[year_base, 0]))
        plt.plot(_df.iloc[:, 0], _df.iloc[:, 4])
        plt.grid()
        plt.figure(3)
        plt.title('Fixed Assets Turnover ($\\lambda$), {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[0, 0], _df.iloc[_knots[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Fixed Assets Turnover ($\\lambda$), {} = 100'.format(
            _df.iloc[year_base, 0]))
        plt.plot(_df.iloc[:, 0], _df.iloc[:, 3].div(_df.iloc[:, 4]))
        plt.grid()
        plt.figure(4)
        plt.title('Investment to Gross Domestic Product Ratio, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[0, 0], _df.iloc[_knots[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio, {} = 100'.format(
            _df.iloc[year_base, 0]))
        plt.plot(_df.iloc[:, 0], YCC)
        plt.grid()
        plt.figure(5)
        plt.title('$\\alpha(t)$, Fixed Assets Retirement Ratio, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[0, 0], _df.iloc[_knots[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('$\\alpha(t)$, {} = 100'.format(_df.iloc[year_base, 0]))
        plt.plot(_df.iloc[:, 0], YFF)
        plt.grid()
        plt.figure(6)
        plt.title('Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[0, 0], _df.iloc[_knots[N], 0]))
        plt.xlabel('$\\alpha(t)$, {} = 100'.format(_df.iloc[year_base, 0]))
        plt.ylabel('Fixed Assets Retirement Value, {} = 100'.format(
            _df.iloc[year_base, 0]))
        plt.plot(YFF, YEE)
        plt.grid()
        plt.figure(7)
        plt.title('Labor Capital Intensity, {} = 100, {}$-${}'.format(
            _df.iloc[year_base, 0], _df.iloc[0, 0], _df.iloc[_knots[N], 0]))
        plt.xlabel('Labor Capital Intensity, {} = 100'.format(
            _df.iloc[year_base, 0]))
        plt.ylabel('Labor Productivity, {} = 100'.format(
            _df.iloc[year_base, 0]))
        plt.plot(np.exp(YAA), np.exp(YBB))
        plt.grid()
        plt.show()
    else:
        print(f'N >= 1 is Required, N = {N} Was Provided')
