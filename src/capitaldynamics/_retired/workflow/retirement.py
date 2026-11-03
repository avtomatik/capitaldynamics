import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def run_retirement_workflow(
    period,
    investment,
    nominal_production,
    real_production,
    fixed_assets,
    labor,
) -> None:
    ###########################################################################
    # Define Basic Year for Deflator
    ###########################################################################
    i = len(period) - 1
    while abs(nominal_production[i] - real_production[i]) > 1:
        i -= 1
        base_year = i
    ###########################################################################
    # Calculate Static Values
    ###########################################################################
    ###########################################################################
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    ###########################################################################
    YAA = np.log(fixed_assets * labor[0] / (fixed_assets[0] * labor))
    ###########################################################################
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    ###########################################################################
    YBB = np.log(real_production * labor[0] / (real_production[0] * labor))
    ###########################################################################
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    ###########################################################################
    YCC = investment * real_production[0] / (investment[0] * real_production)
    ###########################################################################
    # Fixed Assets Turnover Ratio
    ###########################################################################
    YDD = real_production / fixed_assets
    YAA = pd.DataFrame(YAA, columns=["YAA"])
    YBB = pd.DataFrame(YBB, columns=["YBB"])
    number_of_segments = int(
        input("Enter the number of line segments for Gamma (must be >= 1): ")
    )
    if number_of_segments < 1:
        print(
            f"At least 1 line segment is required; received {number_of_segments}."
        )
        return
    print(f"Number of line segments provided: {number_of_segments}.")
    ###########################################################################
    # Gamma & Gamma Switch Points
    ###########################################################################
    gammas = []
    nodes = [0]
    i = 0
    if number_of_segments == 1:
        nodes.append(len(period) - 1)
        gammas.append(
            float(
                input(
                    "Define Gamma for Period from {} to {}: ".format(
                        period[nodes[i]], period[nodes[i + 1]]
                    )
                )
            )
        )
    elif number_of_segments >= 2:
        while i < number_of_segments:
            if i + 1 == number_of_segments:
                nodes.append(len(period) - 1)
                gammas.append(
                    float(
                        input(
                            "Define Gamma for Period from {} to {}: ".format(
                                period[nodes[i]], period[nodes[i + 1]]
                            )
                        )
                    )
                )
                i += 1
            else:
                node = int(input("Select Row for Year: "))
                if node > nodes[i]:
                    nodes.append(node)
                    gammas.append(
                        float(
                            input(
                                "Define Gamma for Period from {} to {}: ".format(
                                    period[nodes[i]], period[nodes[i + 1]]
                                )
                            )
                        )
                    )
                    i += 1
    else:
        print("Error")
    ###########################################################################
    # Calculate Dynamic Values
    ###########################################################################
    ###########################################################################
    # Fixed Assets Retirement Value
    ###########################################################################
    values = [pd.NA]
    ###########################################################################
    # Fixed Assets Retirement Ratio
    ###########################################################################
    ratios = [pd.NA]
    for j in range(number_of_segments):
        for i in range(nodes[j], nodes[j + 1]):
            ###################################################################
            # Fixed Assets Retirement Value
            ###################################################################
            values.append(
                fixed_assets[i]
                - fixed_assets[i + 1]
                + gammas[j] * investment[i]
            )
            ###################################################################
            # Fixed Assets Retirement Ratio
            ###################################################################
            ratios.append(
                (
                    fixed_assets[i]
                    - fixed_assets[i + 1]
                    + gammas[j] * investment[i]
                )
                / fixed_assets[i + 1]
            )
    values = pd.DataFrame(values, columns=["YEE"])
    ratios = pd.DataFrame(ratios, columns=["YFF"])
    df = pd.DataFrame(period, columns=["year"])
    df = pd.concat([df, YAA, YBB, YCC, YDD, values, ratios], axis=1)
    df.columns = ["year", "YAA", "YBB", "YCC", "YDD", "YEE", "YFF"]
    df["YGG"] = df["YFF"] - df["YFF"].mean()
    df["YGG"] = df["YGG"].abs()
    df["YHH"] = df["YFF"].diff()
    df["YHH"] = df["YHH"].abs()
    for i in range(number_of_segments):
        end = nodes[i + 1] - 1 if i == number_of_segments - 1 else nodes[i + 1]
        print(
            "Model Parameter: Gamma for Period from "
            f"{period[nodes[i]]} to {period[end]}: "
            f"{gammas[i]:.6f}"
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
    plt.plot(YCC)
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
    plt.plot(ratios)
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
    plt.plot(ratios, values)
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
    plt.plot(np.exp(YAA), np.exp(YBB))
    plt.grid()
    plt.show()
