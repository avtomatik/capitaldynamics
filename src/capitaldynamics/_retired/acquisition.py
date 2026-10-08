import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_capital_acquisition(
    period,
    investment,
    real_production,
    nominal_production,
    full_capacity_production,
    real_fixed_assets,
    labor,
):
    # =========================================================================
    # Define Basic Year for Deflator
    # =========================================================================
    i = len(period) - 1
    while abs(nominal_production[i] - real_production[i]) > 1:
        i -= 1
        base_year = i

    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    Y01 = real_production / real_fixed_assets
    # =========================================================================
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    # =========================================================================
    Y02 = investment * real_production[0] / (investment[0] * real_production)
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    Y03 = real_fixed_assets * labor[0] / (real_fixed_assets[0] * labor)
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    Y04 = real_production * labor[0] / (real_production[0] * labor)
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    # =========================================================================
    Y05 = np.log(Y03)
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    # =========================================================================
    Y06 = np.log(Y04)
    # =========================================================================
    # Max: Fixed Assets Turnover Ratio
    # =========================================================================
    Y07 = full_capacity_production / real_fixed_assets
    # =========================================================================
    # Max: Investment to Gross Domestic Product Ratio
    # =========================================================================
    Y08 = (
        investment
        * full_capacity_production[0]
        / (investment[0] * full_capacity_production)
    )
    # =========================================================================
    # Max: Labor Productivity
    # =========================================================================
    Y09 = (
        full_capacity_production
        * labor[0]
        / (full_capacity_production[0] * labor)
    )
    # =========================================================================
    # Max: Log Labor Productivity
    # =========================================================================
    Y10 = np.log(Y09)
    Y05 = pd.DataFrame(Y05, columns=["Y05"])
    Y06 = pd.DataFrame(Y06, columns=["Y06"])
    Y10 = pd.DataFrame(Y10, columns=["Y10"])
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input("Define Number of Line Segments for Pi: "))
    print(f"Number of Spans Provided: {N}")
    assert N >= 1, f"N >= 1 is Required, N = {N} Was Provided"
    # =========================================================================
    # Pi & Pi Switch Points
    # =========================================================================
    pi = []
    _knots = [0]

    _ = 0
    if N == 1:
        _knots.append(len(period) - 1)
        pi.append(
            float(
                input(
                    "Define Pi for Period from {} to {}: ".format(
                        period[_knots[_]], period[_knots[1 + _] - 1]
                    )
                )
            )
        )
    elif N >= 2:
        while _ < N:
            if 1 + _ == N:
                _knots.append(len(period) - 1)
                pi.append(
                    float(
                        input(
                            "Define Pi for Period from {} to {}: ".format(
                                period[_knots[_]], period[_knots[1 + _] - 1]
                            )
                        )
                    )
                )
                _ += 1
            else:
                _knot = int(
                    input(
                        "Select Row for Year, Should Be More Than %d:=%d: "
                        % (0, period[0])
                    )
                )
                if _knot > _knots[_]:
                    _knots.append(_knot)
                    pi.append(
                        float(
                            input(
                                "Define Pi for Period from {} to {}: ".format(
                                    period[_knots[_]], period[_knots[1 + _]]
                                )
                            )
                        )
                    )
                    _ += 1
    else:
        print("Error")
    _calculated = [np.nan]
    if N == 1:
        j = 0
        for _ in range(_knots[j], _knots[1 + j]):
            # =========================================================================
            # Estimate: GCF[-] or CA[+]
            # =========================================================================
            _calculated.append(
                real_fixed_assets[1 + _]
                - real_fixed_assets[_]
                + pi[j] * investment[1 + _]
            )
    else:
        for j in range(N):
            if j + _ == N:
                for _ in range(_knots[j], _knots[1 + j]):
                    # =========================================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================================
                    _calculated.append(
                        real_fixed_assets[1 + _]
                        - real_fixed_assets[_]
                        + pi[j] * investment[1 + _]
                    )
            else:
                for _ in range(_knots[j], _knots[1 + j]):
                    # =========================================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================================
                    _calculated.append(
                        real_fixed_assets[1 + _]
                        - real_fixed_assets[_]
                        + pi[j] * investment[1 + _]
                    )
    _calculated = pd.DataFrame(_calculated, columns=["Y11"])
    df = pd.DataFrame(period, columns=["year"])
    df = pd.concat(
        [df, Y01, Y02, Y03, Y04, Y05, Y06, Y07, Y08, Y09, Y10, _calculated],
        axis=1,
    )
    df.columns = [
        "year",
        "Y01",
        "Y02",
        "Y03",
        "Y04",
        "Y05",
        "Y06",
        "Y07",
        "Y08",
        "Y09",
        "Y10",
        "Y11",
    ]

    # {"-": "Gross Capital Formation", "+": "Capital Acquisitions"}

    for _ in range(N):
        if 1 + _ == N:
            print(
                f"Model Parameter: Pi for Period from {period[_knots[_]]} to {period[_knots[1 + _] - 1]}: {pi[_]:.6f}"
            )
            continue
        print(
            f"Model Parameter: Pi for Period from {period[_knots[_]]} to {period[_knots[1 + _]]}: {pi[_]:.6f}"
        )

    plt.figure(1)
    plt.plot(Y03, Y04)
    plt.plot(Y03, Y09)
    plt.title(
        "Labor Productivity, Observed & Max, %d=100, {}$-${}".format(
            period[base_year],
            period[_knots[0]],
        )
    )
    plt.xlabel("Labor Capital Intensity")
    plt.ylabel(f"Labor Productivity, {period[base_year]}=100")
    plt.grid()
    plt.figure(2)
    plt.plot(Y05, Y06)
    plt.plot(Y05, Y10)
    plt.title(
        "Log Labor Productivity, Observed & Max, %d=100, {}$-${}".format(
            period[base_year],
            period[_knots[0]],
        )
    )
    plt.xlabel("Log Labor Capital Intensity")
    plt.ylabel(f"Log Labor Productivity, {period[base_year]}=100")
    plt.grid()
    plt.figure(3)
    plt.plot(Y01)
    plt.plot(Y07)
    plt.title(
        "Fixed Assets Turnover, Observed & Max, %d=100, {}$-${}".format(
            period[base_year],
            period[_knots[0]],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Fixed Assets Turnover, {period[base_year]}=100")
    plt.grid()
    plt.figure(4)
    plt.plot(Y02)
    plt.plot(Y08)
    plt.title(
        "Investment to Gross Domestic Product Ratio,\nObserved & Max, %d=100, {}$-${}".format(
            period[base_year],
            period[_knots[0]],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Investment to GDP Ratio, {period[base_year]}=100")
    plt.grid()
    plt.figure(5)
    plt.plot(_calculated)
    plt.title(
        "Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), %d=100, {}$-${}".format(
            period[base_year],
            period[_knots[0]],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"GCF or CA, {period[base_year]}=100")
    plt.grid()
    plt.show()
