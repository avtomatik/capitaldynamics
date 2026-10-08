import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def run_capital_retirement(
    period,
    investment,
    real_production,
    nominal_production,
    fixed_assets,
    labor,
):
    # =========================================================================
    # Define Basic Year for Deflator
    # =========================================================================
    i = len(period) - 1
    while abs(nominal_production[i] - real_production[i]) > 1:
        i -= 1
        base_year = i

    # =============================================================================
    # Calculate Static Values
    # =============================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    X01 = np.log(fixed_assets * labor[0] / (fixed_assets[0] * labor))
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    X02 = np.log(real_production * labor[0] / (real_production[0] * labor))
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    X03 = investment * real_production[0] / (investment[0] * real_production)
    # =============================================================================
    # Fixed Assets Turnover Ratio
    # =============================================================================
    X04 = real_production / fixed_assets

    X01 = pd.DataFrame(X01, columns=["X01"])
    X02 = pd.DataFrame(X02, columns=["X02"])
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input("Define Number of Line Segments for Gamma: "))
    if N >= 1:
        print(f"Number of Spans Provided: {N}")
        # =========================================================================
        # Pi & Pi Switch Points
        # =========================================================================
        pi = []
        _knots = [0]
        i = 0
        if N == 1:
            _knots.append(len(period) - 1)
            pi.append(
                float(
                    input(
                        "Define Gamma for Period from %d to %d: "
                        % (period[_knots[i]], period[_knots[1 + i]])
                    )
                )
            )
        elif N >= 2:
            while i < N:
                if i == N - 1:
                    _knots.append(len(period) - 1)
                    pi.append(
                        float(
                            input(
                                "Define Gamma for Period from %d to %d: "
                                % (period[_knots[i]], period[_knots[1 + i]])
                            )
                        )
                    )
                    i += 1
                else:
                    y = int(input("Select Row for Year: "))
                    if y > _knots[i]:
                        _knots.append(y)
                        pi.append(
                            float(
                                input(
                                    "Define Gamma for Period from %d to %d: "
                                    % (
                                        period[_knots[i]],
                                        period[_knots[1 + i]],
                                    )
                                )
                            )
                        )
                        i += 1
        else:
            print("Error")
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
            for i in range(_knots[j], _knots[1 + j]):
                # Fixed Assets Retirement Value
                X05.append(
                    fixed_assets[i]
                    - fixed_assets[1 + i]
                    + pi[j] * investment[i]
                )
                # Fixed Assets Retirement Ratio
                X06.append(
                    (
                        fixed_assets[i]
                        - fixed_assets[1 + i]
                        + pi[j] * investment[i]
                    )
                    / fixed_assets[1 + i]
                )
        else:
            for j in range(N):
                if j == N - 1:
                    for i in range(_knots[j], _knots[1 + j]):
                        # Fixed Assets Retirement Value
                        X05.append(
                            fixed_assets[i]
                            - fixed_assets[1 + i]
                            + pi[j] * investment[i]
                        )
                        # Fixed Assets Retirement Ratio
                        X06.append(
                            (
                                fixed_assets[i]
                                - fixed_assets[1 + i]
                                + pi[j] * investment[i]
                            )
                            / fixed_assets[1 + i]
                        )
                else:
                    for i in range(_knots[j], _knots[1 + j]):
                        # Fixed Assets Retirement Value
                        X05.append(
                            fixed_assets[i]
                            - fixed_assets[1 + i]
                            + pi[j] * investment[i]
                        )
                        # Fixed Assets Retirement Ratio
                        X06.append(
                            (
                                fixed_assets[i]
                                - fixed_assets[1 + i]
                                + pi[j] * investment[i]
                            )
                            / fixed_assets[1 + i]
                        )
        X05 = pd.DataFrame(X05, columns=["X05"])
        X06 = pd.DataFrame(X06, columns=["X06"])
        df = pd.DataFrame(period, columns=["year"])
        df = pd.concat([df, X01, X02, X03, X04, X05, X06], axis=1)
        df.columns = ["year", "X01", "X02", "X03", "X04", "X05", "X06"]
        df["X07"] = df["X06"] - df["X06"].mean()
        df["X07"] = df["X07"].abs()
        df["X08"] = df["X06"].diff()
        df["X08"] = df["X08"].abs()
        for i in range(N):
            if i == N - 1:
                print(
                    "Model Parameter: Gamma for Period from %d to %d: %f"
                    % (period[_knots[i]], period[_knots[1 + i]], pi[i])
                )
            else:
                print(
                    "Model Parameter: Gamma for Period from %d to %d: %f"
                    % (period[_knots[i]], period[_knots[1 + i]], pi[i])
                )

        plt.figure(1)
        plt.title(
            "Product, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(f"Product, {base_year}=100")
        plt.plot(period, real_production)
        plt.grid()
        plt.figure(2)
        plt.title(
            "Capital, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(f"Capital, {base_year}=100")
        plt.plot(period, fixed_assets)
        plt.grid()
        plt.figure(3)
        plt.title(
            "Fixed Assets Turnover, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(f"Fixed Assets Turnover, {base_year}=100")
        plt.plot(period, real_production / fixed_assets)
        plt.grid()
        plt.figure(4)
        plt.title(
            "Investment to GDP Ratio, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(f"Investment to GDP Ratio, {base_year}=100")
        plt.plot(period, X03)
        plt.grid()
        plt.figure(5)
        plt.title(
            "$\\mu(t)$, Fixed Assets Retirement Ratio, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(f"$\\mu(t)$, {base_year}=100")
        plt.plot(period, X06)
        plt.grid()
        plt.figure(6)
        plt.title(
            "Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel(f"$\\mu(t)$, {base_year}=100")
        plt.ylabel("Fixed Assets Retirement Value, %d=100" % (base_year))
        plt.plot(X06, X05)
        plt.grid()
        plt.figure(7)
        plt.title(
            "Labor Capital Intensity, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel(f"Labor Capital Intensity, {base_year}=100")
        plt.ylabel(f"Labor Productivity, {base_year}=100")
        plt.plot(np.exp(X01), np.exp(X02))
        plt.grid()
        plt.show()

    else:
        print(f"N >= 1 is Required, N = {N} Was Provided")


def run_capital_acquisitions(
    period,
    investment,
    real_production,
    nominal_production,
    full_capacity_production,
    fixed_assets,
    labor,
    start,
):
    # =========================================================================
    # Define Basic Year for Deflator
    # =========================================================================
    i = len(period) - 1
    while abs(nominal_production[i] - real_production[i]) > 1:
        i -= 1
        base_year = i

    # =============================================================================
    # Calculate Static Values
    # =============================================================================
    X01 = real_production / fixed_assets  # Fixed Assets Turnover Ratio
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    X02 = (
        investment
        * real_production[start]
        / (investment[start] * real_production)
    )
    # Labor Capital Intensity
    X03 = fixed_assets * labor[start] / (fixed_assets[start] * labor)
    X04 = (
        real_production * labor[start] / (real_production[start] * labor)
    )  # Labor Productivity

    X05 = np.log(X03)  # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    X06 = np.log(X04)  # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    X07 = (
        full_capacity_production / fixed_assets
    )  # Max: Fixed Assets Turnover Ratio
    # Max: Investment to Gross Domestic Product Ratio
    X08 = (
        investment
        * full_capacity_production[start]
        / (investment[start] * full_capacity_production)
    )
    # Max: Labor Productivity
    X09 = (
        full_capacity_production
        * labor[start]
        / (full_capacity_production[start] * labor)
    )
    X10 = np.log(X09)  # Max: Log Labor Productivity

    X05 = pd.DataFrame(X05, columns=["X05"])
    X06 = pd.DataFrame(X06, columns=["X06"])
    X10 = pd.DataFrame(X10, columns=["X10"])
    # =============================================================================
    # Calculate Dynamic Values
    # =============================================================================
    N = int(
        input("Define Number of Line Segments for Gamma: ")
    )  # Number of Spans
    if N >= 1:
        print(f"Number of Spans Provided: {N}")
        pi = []
        _knots = []  # Gamma Switch Points & Gamma
        _knots.append(start)
        i = 0
        if N == 1:
            _knots.append(len(period) - 1)
            pi.append(
                float(
                    input(
                        "Define Gamma for Period from %d to %d: "
                        % (period[_knots[i]], period[_knots[1 + i] - 1])
                    )
                )
            )
        elif N >= 2:
            while i < N:
                if i == N - 1:
                    _knots.append(len(period) - 1)
                    pi.append(
                        float(
                            input(
                                "Define Gamma for Period from %d to %d: "
                                % (
                                    period[_knots[i]],
                                    period[_knots[1 + i] - 1],
                                )
                            )
                        )
                    )
                    i += 1
                else:
                    y = int(
                        input(
                            "Select Row for Year, Should Be More Than %d:=%d: "
                            % (start, period[start])
                        )
                    )
                    if y > _knots[i]:
                        _knots.append(y)
                        pi.append(
                            float(
                                input(
                                    "Define Gamma for Period from %d to %d: "
                                    % (
                                        period[_knots[i]],
                                        period[_knots[1 + i]],
                                    )
                                )
                            )
                        )
                        i += 1
        else:
            print("Error")
        X11 = []
        for i in range(1 + start):
            X11.append(np.nan)
        if N == 1:
            j = 0
            for i in range(_knots[j], _knots[1 + j]):
                # Estimate: GCF[-] or CA[+]
                X11.append(
                    fixed_assets[1 + i]
                    - fixed_assets[i]
                    + pi[j] * investment[1 + i]
                )
        else:
            for j in range(N):
                if j == N - 1:
                    for i in range(_knots[j], _knots[1 + j]):
                        # Estimate: GCF[-] or CA[+]
                        X11.append(
                            fixed_assets[1 + i]
                            - fixed_assets[i]
                            + pi[j] * investment[1 + i]
                        )
                else:
                    for i in range(_knots[j], _knots[1 + j]):
                        # Estimate: GCF[-] or CA[+]
                        X11.append(
                            fixed_assets[1 + i]
                            - fixed_assets[i]
                            + pi[j] * investment[1 + i]
                        )
        X11 = pd.DataFrame(X11, columns=["X11"])
        df = pd.DataFrame(period, columns=["year"])
        df = pd.concat(
            [df, X01, X02, X03, X04, X05, X06, X07, X08, X09, X10, X11], axis=1
        )
        df.columns = [
            "year",
            "X01",
            "X02",
            "X03",
            "X04",
            "X05",
            "X06",
            "X07",
            "X08",
            "X09",
            "X10",
            "X11",
        ]

        # {"-": "Gross Capital Formation", "+": "Capital Acquisitions"}

        for i in range(N):
            if i == N - 1:
                print(
                    "Model Parameter: Gamma for Period from %d to %d: %f"
                    % (period[_knots[i]], period[_knots[1 + i] - 1], pi[i])
                )
            else:
                print(
                    "Model Parameter: Gamma for Period from %d to %d: %f"
                    % (period[_knots[i]], period[_knots[1 + i]], pi[i])
                )

        plt.figure(1)
        plt.plot(X03, X04)
        plt.plot(X03, X09)
        plt.title(
            "Labor Productivity, Observed & Max, %d=100, %d$-$%d"
            % (base_year, period[_knots[0]], period[_knots[N] - 1])
        )
        plt.xlabel("Labor Capital Intensity")
        plt.ylabel(f"Labor Productivity, {base_year}=100")
        plt.grid()
        plt.figure(2)
        plt.plot(X05, X06)
        plt.plot(X05, X10)
        plt.title(
            "Log Labor Productivity, Observed & Max, %d=100, %d$-$%d"
            % (base_year, period[_knots[0]], period[_knots[N] - 1])
        )
        plt.xlabel("Log Labor Capital Intensity")
        plt.ylabel(f"Log Labor Productivity, {base_year}=100")
        plt.grid()
        plt.figure(3)
        plt.plot(period, X01)
        plt.plot(period, X07)
        plt.title(
            "Fixed Assets Turnover, Observed & Max, %d=100, %d$-$%d"
            % (base_year, period[_knots[0]], period[_knots[N] - 1])
        )
        plt.xlabel("year")
        plt.ylabel(f"Fixed Assets Turnover, {base_year}=100")
        plt.grid()
        plt.figure(4)
        plt.plot(period, X02)
        plt.plot(period, X08)
        plt.title(
            "Investment to Gross Domestic Product Ratio,\nObserved & Max, %d=100, %d$-$%d"
            % (base_year, period[_knots[0]], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(
            "Investment to Gross Domestic Product Ratio, %d=100" % (base_year)
        )
        plt.grid()
        plt.figure(5)
        plt.plot(period, X11)
        plt.title(
            "Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), %d=100, %d$-$%d"
            % (base_year, period[_knots[0]], period[_knots[N] - 1])
        )
        plt.xlabel("year")
        plt.ylabel(f"GCF or CA, {base_year}=100")
        plt.grid()
        plt.show()
    else:
        print(f"N >= 1 is Required, N = {N} Was Provided")


# =============================================================================
# projectCapitalRetirement.py
# =============================================================================


def run_capital_retirement_x(
    period,
    investment,
    real_production,
    nominal_production,
    fixed_assets,
    labor,
):
    # =============================================================================
    # Y05.append(
    #     fixed_assets[1 + i] - fixed_assets[i] + gmm[j] * investment[1 + i]
    # )
    # Y06.append(
    #     (fixed_assets[1 + i] - fixed_assets[i] + gmm[j] * investment[1 + i])
    #     / fixed_assets[1 + i]
    # )
    # =============================================================================
    # =============================================================================
    # Replaced with
    # =============================================================================
    # =============================================================================
    # Y05.append(fixed_assets[i] - fixed_assets[1 + i] + gmm[j] * investment[i])
    # Y06.append(
    #     (fixed_assets[i] - fixed_assets[1 + i] + gmm[j] * investment[i])
    #     / fixed_assets[1 + i]
    # )
    # =============================================================================
    # =============================================================================
    # Define Basic Year for Deflator
    # =============================================================================
    i = len(period) - 1
    while abs(nominal_production[i] - real_production[i]) > 1:
        i -= 1
        base_year = i

    # =============================================================================
    # Calculate Static Values
    # =============================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    Y01 = np.log(fixed_assets * labor[0] / (fixed_assets[0] * labor))
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    Y02 = np.log(real_production * labor[0] / (real_production[0] * labor))
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    Y03 = investment * real_production[0] / (investment[0] * real_production)
    Y04 = real_production / fixed_assets  # Fixed Assets Turnover Ratio
    Y01 = pd.DataFrame(Y01, columns=["Y01"])
    Y02 = pd.DataFrame(Y02, columns=["Y02"])
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input("Define Number of Line Segments for Gamma: "))
    if N >= 1:
        print(f"Number of Spans Provided: {N}")
        # =========================================================================
        # Pi & Pi Switch Points
        # =========================================================================
        pi = []
        _knots = [0]
        i = 0
        if N == 1:
            _knots.append(len(period) - 1)
            pi.append(
                float(
                    input(
                        "Define Gamma for Period from %d to %d: "
                        % (period[_knots[i]], period[_knots[1 + i]])
                    )
                )
            )
        elif N >= 2:
            while i < N:
                if i == N - 1:
                    _knots.append(len(period) - 1)
                    pi.append(
                        float(
                            input(
                                "Define Gamma for Period from %d to %d: "
                                % (period[_knots[i]], period[_knots[1 + i]])
                            )
                        )
                    )
                    i += 1
                else:
                    y = int(input("Select Row for Year: "))
                    if y > _knots[i]:
                        _knots.append(y)
                        pi.append(
                            float(
                                input(
                                    "Define Gamma for Period from %d to %d: "
                                    % (
                                        period[_knots[i]],
                                        period[_knots[1 + i]],
                                    )
                                )
                            )
                        )
                        i += 1
        else:
            print("Error")
        Y05 = []
        Y06 = []
        Y05.append(np.nan)  # Fixed Assets Retirement Value
        Y06.append(np.nan)  # Fixed Assets Retirement Ratio
        # =============================================================================
        # Calculate Dynamic Values
        # =============================================================================
        if N == 1:
            j = 0
            for i in range(_knots[j], _knots[1 + j]):
                # Fixed Assets Retirement Value
                Y05.append(
                    fixed_assets[i]
                    - fixed_assets[1 + i]
                    + pi[j] * investment[i]
                )
                # Fixed Assets Retirement Ratio
                Y06.append(
                    (
                        fixed_assets[i]
                        - fixed_assets[1 + i]
                        + pi[j] * investment[i]
                    )
                    / fixed_assets[1 + i]
                )
        else:
            for j in range(N):
                if j == N - 1:
                    for i in range(_knots[j], _knots[1 + j]):
                        # Fixed Assets Retirement Value
                        Y05.append(
                            fixed_assets[i]
                            - fixed_assets[1 + i]
                            + pi[j] * investment[i]
                        )
                        # Fixed Assets Retirement Ratio
                        Y06.append(
                            (
                                fixed_assets[i]
                                - fixed_assets[1 + i]
                                + pi[j] * investment[i]
                            )
                            / fixed_assets[1 + i]
                        )
                else:
                    for i in range(_knots[j], _knots[1 + j]):
                        # Fixed Assets Retirement Value
                        Y05.append(
                            fixed_assets[i]
                            - fixed_assets[1 + i]
                            + pi[j] * investment[i]
                        )
                        # Fixed Assets Retirement Ratio
                        Y06.append(
                            (
                                fixed_assets[i]
                                - fixed_assets[1 + i]
                                + pi[j] * investment[i]
                            )
                            / fixed_assets[1 + i]
                        )
        Y05 = pd.DataFrame(Y05, columns=["Y05"])
        Y06 = pd.DataFrame(Y06, columns=["Y06"])
        df = pd.DataFrame(period, columns=["year"])
        df = pd.concat([df, Y01, Y02, Y03, Y04, Y05, Y06], axis=1)
        df.columns = ["year", "Y01", "Y02", "Y03", "Y04", "Y05", "Y06"]
        df["Y07"] = df["Y06"] - df["Y06"].mean()
        df["Y07"] = df["Y07"].abs()
        df["Y08"] = df["Y06"].diff()
        df["Y08"] = df["Y08"].abs()
        for i in range(N):
            if i == N - 1:
                print(
                    "Model Parameter: Gamma for Period from %d to %d: %f"
                    % (period[_knots[i]], period[_knots[1 + i]], pi[i])
                )
            else:
                print(
                    "Model Parameter: Gamma for Period from %d to %d: %f"
                    % (period[_knots[i]], period[_knots[1 + i]], pi[i])
                )

        plt.figure(1)
        plt.title(
            "Product, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(f"Product, {base_year}=100")
        plt.plot(period, real_production)
        plt.grid()
        plt.figure(2)
        plt.title(
            "Capital, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(f"Capital, {base_year}=100")
        plt.plot(period, fixed_assets)
        plt.grid()
        plt.figure(3)
        plt.title(
            "Fixed Assets Turnover, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(f"Fixed Assets Turnover, {base_year}=100")
        plt.plot(period, real_production / fixed_assets)
        plt.grid()
        plt.figure(4)
        plt.title(
            "Investment to Gross Domestic Product Ratio, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(
            "Investment to Gross Domestic Product Ratio, %d=100" % (base_year)
        )
        plt.plot(period, Y03)
        plt.grid()
        plt.figure(5)
        plt.title(
            "$\\mu(t)$, Fixed Assets Retirement Ratio, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel("year")
        plt.ylabel(f"$\\mu(t)$, {base_year}=100")
        plt.plot(period, Y06)
        plt.grid()
        plt.figure(6)
        plt.title(
            "Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel(f"$\\mu(t)$, {base_year}=100")
        plt.ylabel("Fixed Assets Retirement Value, %d=100" % (base_year))
        plt.plot(Y06, Y05)
        plt.grid()
        plt.figure(7)
        plt.title(
            "Labor Capital Intensity, %d=100, %d$-$%d"
            % (base_year, period[0], period[_knots[N]])
        )
        plt.xlabel(f"Labor Capital Intensity, {base_year}=100")
        plt.ylabel(f"Labor Productivity, {base_year}=100")
        plt.plot(np.exp(Y01), np.exp(Y02))
        plt.grid()
        plt.show()
    else:
        print(f"N >= 1 is Required, N = {N} Was Provided")


def plot_calculate_capital_aquisition(df: pd.DataFrame):
    """
    df.iloc[:, 0]: Period
    df.iloc[:, 1]: Nominal Investment
    df.iloc[:, 2]: Nominal Production
    df.iloc[:, 3]: Real Production
    df.iloc[:, 4]: Maximum Real Production
    df.iloc[:, 5]: Nominal Capital
    df.iloc[:, 6]: Labor
    """
    i = df.shape[0] - 1
    while abs(df.iloc[i, 2] - df.iloc[i, 3]) > 1:
        i -= 1
        base_year = i

    """Calculate Static Values"""
    XAA = df.iloc[:, 3].div(df.iloc[:, 5])  # Fixed Assets Turnover Ratio
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    XBB = df.iloc[:, 1].div(df.iloc[:, 3])
    XCC = df.iloc[:, 5].div(df.iloc[:, 6])  # Labor Capital Intensity
    XDD = df.iloc[:, 3].div(df.iloc[:, 6])  # Labor Productivity
    XBB = XBB.div(XBB[0])
    XCC = XCC.div(XCC[0])
    XDD = XDD.div(XDD[0])
    XEE = np.log(XCC)  # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    XFF = np.log(XDD)  # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    # Max: Fixed Assets Turnover Ratio
    XGG = df.iloc[:, 4].div(df.iloc[:, 5])
    # Max: Investment to Gross Domestic Product Ratio
    XHH = df.iloc[:, 1].div(df.iloc[:, 4])
    XII = df.iloc[:, 4].div(df.iloc[:, 6])  # Max: Labor Productivity
    XHH = XHH.div(XHH[0])
    XII = XII.div(XII[0])
    XJJ = np.log(XII)  # Max: Log Labor Productivity
    XEE = pd.DataFrame(XEE, columns=["XEE"])
    XFF = pd.DataFrame(XFF, columns=["XFF"])
    XJJ = pd.DataFrame(XJJ, columns=["XJJ"])
    """Calculate Dynamic Values"""
    N = int(
        input("Define Number of Line Segments for Pi: ")
    )  # Number of Spans
    if N >= 1:
        print(f"Number of Spans Provided: {N}")
        # =========================================================================
        # Pi & Pi Switch Points
        # =========================================================================
        pi = []
        _knots = [0]
        _ = 0
        if N == 1:
            _knots.append(df.shape[0] - 1)
            pi.append(
                float(
                    input(
                        "Define Pi for Period from {} to {}: ".format(
                            df.iloc[_knots[_], 0],
                            df.iloc[_knots[1 + _] - 1, 0],
                        )
                    )
                )
            )
        elif N >= 2:
            while _ < N:
                if _ == N - 1:
                    _knots.append(df.shape[0] - 1)
                    pi.append(
                        float(
                            input(
                                "Define Pi for Period from {} to {}: ".format(
                                    df.iloc[_knots[_], 0],
                                    df.iloc[_knots[1 + _] - 1, 0],
                                )
                            )
                        )
                    )
                    _ += 1
                else:
                    y = int(
                        input(
                            "Select Row for Year, Should Be More Than {}: = {}: ".format(
                                0, df.iloc[0, 0]
                            )
                        )
                    )
                    if y > _knots[_]:
                        _knots.append(y)
                        pi.append(
                            float(
                                input(
                                    "Define Pi for Period from {} to {}: ".format(
                                        df.iloc[_knots[_], 0],
                                        df.iloc[_knots[1 + _], 0],
                                    )
                                )
                            )
                        )
                        _ += 1
        else:
            print("Error")
        XKK = []
        for _ in range(1):
            XKK.append(np.nan)
        if N == 1:
            j = 0
            for _ in range(_knots[j], _knots[1 + j]):
                # Estimate: GCF[-] or CA[+]
                XKK.append(
                    df.iloc[1 + _, 5]
                    - df.iloc[_, 5]
                    + pi[j] * df.iloc[1 + _, 1]
                )
        else:
            for j in range(N):
                if j == N - 1:
                    for _ in range(_knots[j], _knots[1 + j]):
                        # Estimate: GCF[-] or CA[+]
                        XKK.append(
                            df.iloc[1 + _, 5]
                            - df.iloc[_, 5]
                            + pi[j] * df.iloc[1 + _, 1]
                        )
                else:
                    for _ in range(_knots[j], _knots[1 + j]):
                        # Estimate: GCF[-] or CA[+]
                        XKK.append(
                            df.iloc[1 + _, 5]
                            - df.iloc[_, 5]
                            + pi[j] * df.iloc[1 + _, 1]
                        )
        XKK = pd.DataFrame(XKK, columns=["XKK"])
        result = pd.DataFrame(df.iloc[:, 0], columns=["year"])
        result = pd.concat(
            [result, XAA, XBB, XCC, XDD, XEE, XFF, XGG, XHH, XII, XJJ, XKK],
            axis=1,
        )
        result.columns = [
            "year",
            "XAA",
            "XBB",
            "XCC",
            "XDD",
            "XEE",
            "XFF",
            "XGG",
            "XHH",
            "XII",
            "XJJ",
            "XKK",
        ]

        # {"-": "Gross Capital Formation", "+": "Capital Acquisitions"}

        for _ in range(N):
            if _ == N - 1:
                print(
                    "Model Parameter: Pi for Period from {} to {}: {:.6f}".format(
                        df.iloc[_knots[_], 0],
                        df.iloc[_knots[1 + _] - 1, 0],
                        pi[_],
                    )
                )
            else:
                print(
                    "Model Parameter: Pi for Period from {} to {}: {:.6f}".format(
                        df.iloc[_knots[_], 0],
                        df.iloc[_knots[1 + _], 0],
                        pi[_],
                    )
                )
        plt.figure(1)
        plt.plot(XCC, XDD)
        plt.plot(XCC, XII)
        plt.title(
            "Labor Productivity, Observed & Max, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0],
                df.iloc[_knots[0], 0],
                df.iloc[_knots[N] - 1, 0],
            )
        )
        plt.xlabel("Labor Capital Intensity")
        plt.ylabel(
            "Labor Productivity, {} = 100".format(df.iloc[base_year, 0])
        )
        plt.grid()
        plt.figure(2)
        plt.plot(XEE, XFF)
        plt.plot(XEE, XJJ)
        plt.title(
            "Log Labor Productivity, Observed & Max, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0],
                df.iloc[_knots[0], 0],
                df.iloc[_knots[N] - 1, 0],
            )
        )
        plt.xlabel("Log Labor Capital Intensity")
        plt.ylabel(
            "Log Labor Productivity, {} = 100".format(df.iloc[base_year, 0])
        )
        plt.grid()
        plt.figure(3)
        plt.plot(df.iloc[:, 0], XAA)
        plt.plot(df.iloc[:, 0], XGG)
        plt.title(
            "Fixed Assets Turnover ($\\lambda$), Observed & Max, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0],
                df.iloc[_knots[0], 0],
                df.iloc[_knots[N] - 1, 0],
            )
        )
        plt.xlabel("year")
        plt.ylabel(
            "Fixed Assets Turnover ($\\lambda$), {} = 100".format(
                df.iloc[base_year, 0]
            )
        )
        plt.grid()
        plt.figure(4)
        plt.plot(df.iloc[:, 0], XBB)
        plt.plot(df.iloc[:, 0], XHH)
        plt.title(
            "Investment to Gross Domestic Product Ratio, \nObserved & Max, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0],
                df.iloc[_knots[0], 0],
                df.iloc[_knots[N], 0],
            )
        )
        plt.xlabel("year")
        plt.ylabel(
            "Investment to Gross Domestic Product Ratio, {} = 100".format(
                df.iloc[base_year, 0]
            )
        )
        plt.grid()
        plt.figure(5)
        plt.plot(df.iloc[:, 0], XKK)
        plt.title(
            "Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {} = 100, {}$-${}".format(
                df.iloc[base_year, 0],
                df.iloc[_knots[0], 0],
                df.iloc[_knots[N] - 1, 0],
            )
        )
        plt.xlabel("year")
        plt.ylabel("GCF or CA, {} = 100".format(df.iloc[base_year, 0]))
        plt.grid()
        plt.show()
    else:
        print(f"N >= 1 is Required, N = {N} Was Provided")


def calculate_capital_retirement(df: pd.DataFrame):
    """
    df.iloc[:, 0]: Period
    df.iloc[:, 1]: Nominal Investment
    df.iloc[:, 2]: Nominal Production
    df.iloc[:, 3]: Real Production
    df.iloc[:, 4]: Nominal Capital
    df.iloc[:, 5]: Labor
    """
    i = df.shape[0] - 1
    while abs(df.iloc[i, 2] - df.iloc[i, 3]) > 1:
        i -= 1
        base_year = i

    """Calculate Static Values"""
    YAA = df.iloc[:, 4].div(df.iloc[:, 5])
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    YAA = np.log(YAA.div(YAA[0]))
    YBB = df.iloc[:, 3].div(df.iloc[:, 5])
    YBB = np.log(YBB.div(YBB[0]))  # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    YCC = df.iloc[:, 1].div(df.iloc[:, 3])
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    YCC = YCC.div(YCC[0])
    YDD = df.iloc[:, 3].div(df.iloc[:, 4])  # Fixed Assets Turnover Ratio
    YAA = pd.DataFrame(YAA, columns=["YAA"])
    YBB = pd.DataFrame(YBB, columns=["YBB"])
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input("Define Number of Line Segments for Pi: "))
    if N >= 1:
        print(f"Number of Spans Provided: {N}")
        # =========================================================================
        # Pi & Pi Switch Points
        # =========================================================================
        pi = []
        _knots = [0]
        _ = 0
        if N == 1:
            _knots.append(df.shape[0] - 1)
            pi.append(
                float(
                    input(
                        "Define Pi for Period from {} to {}: ".format(
                            df.iloc[_knots[_], 0],
                            df.iloc[:, 0][_knots[1 + _]],
                        )
                    )
                )
            )
        elif N >= 2:
            while _ < N:
                if _ == N - 1:
                    _knots.append(df.shape[0] - 1)
                    pi.append(
                        float(
                            input(
                                "Define Pi for Period from {} to {}: ".format(
                                    df.iloc[_knots[_], 0],
                                    df.iloc[_knots[1 + _], 0],
                                )
                            )
                        )
                    )
                    _ += 1
                else:
                    y = int(input("Select Row for Year: "))
                    if y > _knots[_]:
                        _knots.append(y)
                        pi.append(
                            float(
                                input(
                                    "Define Pi for Period from {} to {}: ".format(
                                        df.iloc[_knots[_], 0],
                                        df.iloc[_knots[1 + _], 0],
                                    )
                                )
                            )
                        )
                        _ += 1
        else:
            print("Error")
        YEE = []
        YFF = []
        YEE.append(np.nan)  # Fixed Assets Retirement Value
        YFF.append(np.nan)  # Fixed Assets Retirement Ratio
        """Calculate Dynamic Values"""
        if N == 1:
            j = 0
            for _ in range(_knots[j], _knots[1 + j]):
                # Fixed Assets Retirement Value
                YEE.append(
                    df.iloc[_, 4] - df.iloc[1 + _, 4] + pi[j] * df.iloc[_, 1]
                )
                # Fixed Assets Retirement Ratio
                YFF.append(
                    (df.iloc[_, 4] - df.iloc[1 + _, 4] + pi[j] * df.iloc[_, 1])
                    / df.iloc[1 + _, 4]
                )
        else:
            for j in range(N):
                if j == N - 1:
                    for _ in range(_knots[j], _knots[1 + j]):
                        # Fixed Assets Retirement Value
                        YEE.append(
                            df.iloc[_, 4]
                            - df.iloc[1 + _, 4]
                            + pi[j] * df.iloc[_, 1]
                        )
                        # Fixed Assets Retirement Ratio
                        YFF.append(
                            (
                                df.iloc[_, 4]
                                - df.iloc[1 + _, 4]
                                + pi[j] * df.iloc[_, 1]
                            )
                            / df.iloc[1 + _, 4]
                        )
                else:
                    for _ in range(_knots[j], _knots[1 + j]):
                        # Fixed Assets Retirement Value
                        YEE.append(
                            df.iloc[_, 4]
                            - df.iloc[1 + _, 4]
                            + pi[j] * df.iloc[_, 1]
                        )
                        # Fixed Assets Retirement Ratio
                        YFF.append(
                            (
                                df.iloc[_, 4]
                                - df.iloc[1 + _, 4]
                                + pi[j] * df.iloc[_, 1]
                            )
                            / df.iloc[1 + _, 4]
                        )
        YEE = pd.DataFrame(YEE, columns=["YEE"])
        YFF = pd.DataFrame(YFF, columns=["YFF"])
        result = pd.DataFrame(df.iloc[:, 0], columns=["year"])
        result = pd.concat(
            [result, YAA, YBB, YCC, YDD, YEE, YFF], axis=1, sort=True
        )
        result.columns = ["year", "YAA", "YBB", "YCC", "YDD", "YEE", "YFF"]
        result["YGG"] = result["YFF"] - result["YFF"].mean()
        result["YGG"] = result["YGG"].abs()
        result["YHH"] = result["YFF"].diff()
        result["YHH"] = result["YHH"].abs()
        for _ in range(N):
            if _ == N - 1:
                print(
                    "Model Parameter: Pi for Period from {} to {}: {:.6f}".format(
                        df.iloc[_knots[_], 0],
                        df.iloc[_knots[1 + _], 0],
                        pi[_],
                    )
                )
            else:
                print(
                    "Model Parameter: Pi for Period from {} to {}: {:.6f}".format(
                        df.iloc[_knots[_], 0],
                        df.iloc[_knots[1 + _], 0],
                        pi[_],
                    )
                )
        plt.figure(1)
        plt.title(
            "Product, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0], df.iloc[0, 0], df.iloc[_knots[N], 0]
            )
        )
        plt.xlabel("year")
        plt.ylabel("Product, {} = 100".format(df.iloc[base_year, 0]))
        plt.plot(df.iloc[:, 0], df.iloc[:, 3])
        plt.grid()
        plt.figure(2)
        plt.title(
            "Capital, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0], df.iloc[0, 0], df.iloc[_knots[N], 0]
            )
        )
        plt.xlabel("year")
        plt.ylabel("Capital, {} = 100".format(df.iloc[base_year, 0]))
        plt.plot(df.iloc[:, 0], df.iloc[:, 4])
        plt.grid()
        plt.figure(3)
        plt.title(
            "Fixed Assets Turnover ($\\lambda$), {} = 100, {}$-${}".format(
                df.iloc[base_year, 0], df.iloc[0, 0], df.iloc[_knots[N], 0]
            )
        )
        plt.xlabel("year")
        plt.ylabel(
            "Fixed Assets Turnover ($\\lambda$), {} = 100".format(
                df.iloc[base_year, 0]
            )
        )
        plt.plot(df.iloc[:, 0], df.iloc[:, 3].div(df.iloc[:, 4]))
        plt.grid()
        plt.figure(4)
        plt.title(
            "Investment to Gross Domestic Product Ratio, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0], df.iloc[0, 0], df.iloc[_knots[N], 0]
            )
        )
        plt.xlabel("year")
        plt.ylabel(
            "Investment to Gross Domestic Product Ratio, {} = 100".format(
                df.iloc[base_year, 0]
            )
        )
        plt.plot(df.iloc[:, 0], YCC)
        plt.grid()
        plt.figure(5)
        plt.title(
            "$\\alpha(t)$, Fixed Assets Retirement Ratio, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0], df.iloc[0, 0], df.iloc[_knots[N], 0]
            )
        )
        plt.xlabel("year")
        plt.ylabel("$\\alpha(t)$, {} = 100".format(df.iloc[base_year, 0]))
        plt.plot(df.iloc[:, 0], YFF)
        plt.grid()
        plt.figure(6)
        plt.title(
            "Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0], df.iloc[0, 0], df.iloc[_knots[N], 0]
            )
        )
        plt.xlabel("$\\alpha(t)$, {} = 100".format(df.iloc[base_year, 0]))
        plt.ylabel(
            "Fixed Assets Retirement Value, {} = 100".format(
                df.iloc[base_year, 0]
            )
        )
        plt.plot(YFF, YEE)
        plt.grid()
        plt.figure(7)
        plt.title(
            "Labor Capital Intensity, {} = 100, {}$-${}".format(
                df.iloc[base_year, 0], df.iloc[0, 0], df.iloc[_knots[N], 0]
            )
        )
        plt.xlabel(
            "Labor Capital Intensity, {} = 100".format(df.iloc[base_year, 0])
        )
        plt.ylabel(
            "Labor Productivity, {} = 100".format(df.iloc[base_year, 0])
        )
        plt.plot(np.exp(YAA), np.exp(YBB))
        plt.grid()
        plt.show()
    else:
        print(f"N >= 1 is Required, N = {N} Was Provided")
