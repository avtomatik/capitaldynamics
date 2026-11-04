import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def analyze_capital_retirement(df: pd.DataFrame) -> None:
    """
    Expected DataFrame structure:
        index: Year
        column 0: Nominal Investment
        column 1: Nominal Production
        column 2: Real Production
        column 3: Real Capital
        column 4: Labor
    """
    period = df.index.to_numpy()
    investment = df.iloc[:, 0].to_numpy()
    nominal_production = df.iloc[:, 1].to_numpy()
    real_production = df.iloc[:, 2].to_numpy()
    real_fixed_assets = df.iloc[:, 3].to_numpy()
    labor = df.iloc[:, 4].to_numpy()
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
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    YAA = np.log(real_fixed_assets * labor[0] / (real_fixed_assets[0] * labor))
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    YBB = np.log(real_production * labor[0] / (real_production[0] * labor))
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    YCC = investment * real_production[0] / (investment[0] * real_production)
    # Fixed Assets Turnover Ratio
    YDD = real_production / real_fixed_assets
    YAA = pd.DataFrame(YAA, columns=["YAA"])
    YBB = pd.DataFrame(YBB, columns=["YBB"])
    ###########################################################################
    # Gamma & Gamma Switch Points
    ###########################################################################
    number_of_segments = int(
        input("Enter the number of line segments for Gamma (must be >= 1): ")
    )
    if number_of_segments < 1:
        print(
            f"At least 1 line segment is required; received {number_of_segments}."
        )
        return
    print(f"Number of line segments provided: {number_of_segments}.")
    gammas = []
    nodes = [0]
    i = 0
    if number_of_segments == 1:
        nodes.append(len(period) - 1)
        gammas.append(
            float(
                input(
                    "Define Gamma for Period from {} to {}: ".format(
                        period[nodes[i]],
                        period[nodes[i + 1]],
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
                                period[nodes[i]],
                                period[nodes[i + 1]],
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
                                    period[nodes[i]],
                                    period[nodes[i + 1]],
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
    # Fixed Assets Retirement Value
    YEE = [pd.NA]
    # Fixed Assets Retirement Ratio
    YFF = [pd.NA]
    for j in range(number_of_segments):
        for i in range(nodes[j], nodes[j + 1]):
            # Fixed Assets Retirement Value
            retirement_value = (
                real_fixed_assets[i]
                - real_fixed_assets[i + 1]
                + gammas[j] * investment[i]
            )
            YEE.append(retirement_value)
            # Fixed Assets Retirement Ratio
            YFF.append(retirement_value / real_fixed_assets[i + 1])
    YEE = pd.DataFrame(YEE, columns=["YEE"])
    YFF = pd.DataFrame(YFF, columns=["YFF"])
    ###########################################################################
    # Assemble Results
    ###########################################################################
    result = pd.DataFrame(period, columns=["year"])
    result = pd.concat(
        [result, YAA, YBB, pd.DataFrame(YCC), pd.DataFrame(YDD), YEE, YFF],
        axis=1,
    )
    result.columns = [
        "year",
        "YAA",
        "YBB",
        "YCC",
        "YDD",
        "YEE",
        "YFF",
    ]
    result["YGG"] = (result["YFF"] - result["YFF"].mean()).abs()
    result["YHH"] = result["YFF"].diff().abs()
    ###########################################################################
    # Print Model Parameters
    ###########################################################################
    for i in range(number_of_segments):
        end = nodes[i + 1] - 1 if i == number_of_segments - 1 else nodes[i + 1]
        print(
            "Model Parameter: Gamma for Period from "
            f"{period[nodes[i]]} to {period[end]}: "
            f"{gammas[i]:.6f}"
        )
    ###########################################################################
    # Visualization
    ###########################################################################
    plt.figure(1)
    plt.title(
        "Product, {} = 100, {}$-${}".format(
            period[base_year],
            period[0],
            period[nodes[number_of_segments]],
        )
    )
    plt.xlabel("year")
    plt.ylabel("Product, {} = 100".format(period[base_year]))
    plt.plot(period, real_production)
    plt.grid()
    plt.figure(2)
    plt.title(
        "Capital, {} = 100, {}$-${}".format(
            period[base_year],
            period[0],
            period[nodes[number_of_segments]],
        )
    )
    plt.xlabel("year")
    plt.ylabel("Capital, {} = 100".format(period[base_year]))
    plt.plot(period, real_fixed_assets)
    plt.grid()
    plt.figure(3)
    plt.title(
        "Fixed Assets Turnover ($\\lambda$), {} = 100, {}$-${}".format(
            period[base_year],
            period[0],
            period[nodes[number_of_segments]],
        )
    )
    plt.xlabel("year")
    plt.ylabel(
        "Fixed Assets Turnover ($\\lambda$), {} = 100".format(
            period[base_year]
        )
    )
    plt.plot(period, YDD)
    plt.grid()
    plt.figure(4)
    plt.title(
        "Investment to Gross Domestic Product Ratio, {} = 100, {}$-${}".format(
            period[base_year],
            period[0],
            period[nodes[number_of_segments]],
        )
    )
    plt.xlabel("year")
    plt.ylabel(
        "Investment to Gross Domestic Product Ratio, {} = 100".format(
            period[base_year]
        )
    )
    plt.plot(period, YCC)
    plt.grid()
    plt.figure(5)
    plt.title(
        "$\\alpha(t)$, Fixed Assets Retirement Ratio, {} = 100, {}$-${}".format(
            period[base_year],
            period[0],
            period[nodes[number_of_segments]],
        )
    )
    plt.xlabel("year")
    plt.ylabel("$\\alpha(t)$, {} = 100".format(period[base_year]))
    plt.plot(period, YFF)
    plt.grid()
    plt.figure(6)
    plt.title(
        "Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, "
        "{} = 100, {}$-${}".format(
            period[base_year],
            period[0],
            period[nodes[number_of_segments]],
        )
    )
    plt.xlabel("$\\alpha(t)$, {} = 100".format(period[base_year]))
    plt.ylabel(
        "Fixed Assets Retirement Value, {} = 100".format(period[base_year])
    )
    plt.plot(YFF, YEE)
    plt.grid()
    plt.figure(7)
    plt.title(
        "Labor Capital Intensity, {} = 100, {}$-${}".format(
            period[base_year],
            period[0],
            period[nodes[number_of_segments]],
        )
    )
    plt.xlabel("Labor Capital Intensity, {} = 100".format(period[base_year]))
    plt.ylabel("Labor Productivity, {} = 100".format(period[base_year]))
    plt.plot(np.exp(YAA), np.exp(YBB))
    plt.grid()
    plt.show()
