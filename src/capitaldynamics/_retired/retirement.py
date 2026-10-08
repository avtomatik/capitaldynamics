import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_capital_retirement(
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

    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    # =========================================================================
    Y01 = np.log(fixed_assets * labor[0] / (fixed_assets[0] * labor))
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    # =========================================================================
    Y02 = np.log(real_production * labor[0] / (real_production[0] * labor))
    # =========================================================================
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    # =========================================================================
    Y03 = investment * real_production[0] / (investment[0] * real_production)
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    Y04 = real_production / fixed_assets
    Y01 = pd.DataFrame(Y01, columns=["Y01"])
    Y02 = pd.DataFrame(Y02, columns=["Y02"])
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
                        period[_knots[_]], period[_knots[1 + _]]
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
                                period[_knots[_]], period[_knots[1 + _]]
                            )
                        )
                    )
                )
                _ += 1
            else:
                _knot = int(input("Select Row for Year: "))
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
        for _ in range(_knots[j], _knots[1 + j]):
            # =========================================================================
            # Fixed Assets Retirement Value
            # =========================================================================
            _value.append(
                fixed_assets[_] - fixed_assets[1 + _] + pi[j] * investment[_]
            )
            # =========================================================================
            # Fixed Assets Retirement Ratio
            # =========================================================================
            _ratio.append(
                (fixed_assets[_] - fixed_assets[1 + _] + pi[j] * investment[_])
                / fixed_assets[1 + _]
            )
    else:
        for j in range(N):
            if j + _ == N:
                for _ in range(_knots[j], _knots[1 + j]):
                    # =========================================================================
                    # Fixed Assets Retirement Value
                    # =========================================================================
                    _value.append(
                        fixed_assets[_]
                        - fixed_assets[1 + _]
                        + pi[j] * investment[_]
                    )
                    # =========================================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================================
                    _ratio.append(
                        (
                            fixed_assets[_]
                            - fixed_assets[1 + _]
                            + pi[j] * investment[_]
                        )
                        / fixed_assets[1 + _]
                    )
            else:
                for _ in range(_knots[j], _knots[1 + j]):
                    # =========================================================================
                    # Fixed Assets Retirement Value
                    # =========================================================================
                    _value.append(
                        fixed_assets[_]
                        - fixed_assets[1 + _]
                        + pi[j] * investment[_]
                    )
                    # =========================================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================================
                    _ratio.append(
                        (
                            fixed_assets[_]
                            - fixed_assets[1 + _]
                            + pi[j] * investment[_]
                        )
                        / fixed_assets[1 + _]
                    )
    _value = pd.DataFrame(_value, columns=["Y05"])
    _ratio = pd.DataFrame(_ratio, columns=["Y06"])
    df = pd.DataFrame(period, columns=["year"])
    df = pd.concat([df, Y01, Y02, Y03, Y04, _value, _ratio], axis=1)
    df.columns = ("year", "Y01", "Y02", "Y03", "Y04", "Y05", "Y06")
    df["Y07"] = df["Y06"] - df["Y06"].mean()
    df["Y07"] = df["Y07"].abs()
    df["Y08"] = df["Y06"].diff()
    df["Y08"] = df["Y08"].abs()
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
    plt.title(
        "Product, %d=100, {}$-${}".format(
            period[base_year],
            period[0],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Product, {period[base_year]}=100")
    plt.plot(real_production)
    plt.grid()
    plt.figure(2)
    plt.title(
        "Capital, %d=100, {}$-${}".format(
            period[base_year],
            period[0],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Capital, {period[base_year]}=100")
    plt.plot(fixed_assets)
    plt.grid()
    plt.figure(3)
    plt.title(
        "Fixed Assets Turnover, %d=100, {}$-${}".format(
            period[base_year],
            period[0],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Fixed Assets Turnover, {period[base_year]}=100")
    plt.plot(real_production / fixed_assets)
    plt.grid()
    plt.figure(4)
    plt.title(
        "Investment to GDP Ratio, %d=100, {}$-${}".format(
            period[base_year],
            period[0],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Investment to GDP Ratio, {period[base_year]}=100")
    plt.plot(Y03)
    plt.grid()
    plt.figure(5)
    plt.title(
        "$\\mu(t)$, Fixed Assets Retirement Ratio, %d=100, {}$-${}".format(
            period[base_year],
            period[0],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"$\\mu(t)$, {period[base_year]}=100")
    plt.plot(_ratio)
    plt.grid()
    plt.figure(6)
    plt.title(
        "Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, %d=100, {}$-${}".format(
            period[base_year],
            period[0],
        )
    )
    plt.xlabel(f"$\\mu(t)$, {period[base_year]}=100")
    plt.ylabel(f"Fixed Assets Retirement Value, {period[base_year]}=100")
    plt.plot(_ratio, _value)
    plt.grid()
    plt.figure(7)
    plt.title(
        "Labor Capital Intensity, %d=100, {}$-${}".format(
            period[base_year],
            period[0],
        )
    )
    plt.xlabel(f"Labor Capital Intensity, {period[base_year]}=100")
    plt.ylabel(f"Labor Productivity, {period[base_year]}=100")
    plt.plot(np.exp(Y01), np.exp(Y02))
    plt.grid()
    plt.show()
