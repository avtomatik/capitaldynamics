import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def run_acquisition_workflow(
    period,
    investment,
    nominal_production,
    real_production,
    full_capacity_production,
    real_fixed_assets,
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
    # Fixed Assets Turnover Ratio
    ###########################################################################
    YAA = real_production / real_fixed_assets
    ###########################################################################
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    ###########################################################################
    YBB = investment * real_production[0] / (investment[0] * real_production)
    ###########################################################################
    # Labor Capital Intensity
    ###########################################################################
    YCC = real_fixed_assets * labor[0] / (real_fixed_assets[0] * labor)
    ###########################################################################
    # Labor Productivity
    ###########################################################################
    YDD = real_production * labor[0] / (real_production[0] * labor)
    ###########################################################################
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    ###########################################################################
    YEE = np.log(YCC)
    ###########################################################################
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    ###########################################################################
    YFF = np.log(YDD)
    ###########################################################################
    # Max: Fixed Assets Turnover Ratio
    ###########################################################################
    YGG = full_capacity_production / real_fixed_assets
    ###########################################################################
    # Max: Investment to Gross Domestic Product Ratio
    ###########################################################################
    YHH = (
        investment
        * full_capacity_production[0]
        / (investment[0] * full_capacity_production)
    )
    ###########################################################################
    # Max: Labor Productivity
    ###########################################################################
    YII = (
        full_capacity_production
        * labor[0]
        / (full_capacity_production[0] * labor)
    )
    ###########################################################################
    # Max: Log Labor Productivity
    ###########################################################################
    YJJ = np.log(YII)
    YEE = pd.DataFrame(YEE, columns=["YEE"])
    YFF = pd.DataFrame(YFF, columns=["YFF"])
    YJJ = pd.DataFrame(YJJ, columns=["YJJ"])
    ###########################################################################
    # Calculate Dynamic Values
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
                        period[nodes[i]], period[nodes[i + 1] - 1]
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
                                period[nodes[i]], period[nodes[i + 1] - 1]
                            )
                        )
                    )
                )
                i += 1
            else:
                node = int(
                    input(
                        "Select Row for Year, Should Be More Than %d:=%d: "
                        % (0, period[0])
                    )
                )
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
    estimates = [pd.NA]
    for j in range(number_of_segments):
        for i in range(nodes[j], nodes[j + 1]):
            ###################################################################
            # Estimate: GCF[-] or CA[+]
            ###################################################################
            estimates.append(
                real_fixed_assets[i + 1]
                - real_fixed_assets[i]
                + gammas[j] * investment[i + 1]
            )
    estimates = pd.DataFrame(estimates, columns=["estimates"])
    df = pd.DataFrame(period, columns=["year"])
    df = pd.concat(
        [df, YAA, YBB, YCC, YDD, YEE, YFF, YGG, YHH, YII, YJJ, estimates],
        axis=1,
    )
    df.columns = [
        "year",
        "YAA",
        "YBB",
        "YCC",
        "YDD",
        "YEE",
        "YFF",
        "YGG",
        "YHH",
        "YII",
        "YJJ",
        "estimates",
    ]
    # {"-": "Gross Capital Formation", "+": "Capital Acquisitions"}
    for i in range(number_of_segments):
        end = nodes[i + 1] - 1 if i == number_of_segments - 1 else nodes[i + 1]
        print(
            "Model Parameter: Gamma for Period from "
            f"{period[nodes[i]]} to {period[end]}: "
            f"{gammas[i]:.6f}"
        )
    plt.figure(1)
    plt.plot(YCC, YDD)
    plt.plot(YCC, YII)
    plt.title(
        "Labor Productivity, Observed & Max, %d=100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
        )
    )
    plt.xlabel("Labor Capital Intensity")
    plt.ylabel(f"Labor Productivity, {period[base_year]}=100")
    plt.grid()
    plt.figure(2)
    plt.plot(YEE, YFF)
    plt.plot(YEE, YJJ)
    plt.title(
        "Log Labor Productivity, Observed & Max, %d=100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
        )
    )
    plt.xlabel("Log Labor Capital Intensity")
    plt.ylabel(f"Log Labor Productivity, {period[base_year]}=100")
    plt.grid()
    plt.figure(3)
    plt.plot(YAA)
    plt.plot(YGG)
    plt.title(
        "Fixed Assets Turnover, Observed & Max, %d=100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Fixed Assets Turnover, {period[base_year]}=100")
    plt.grid()
    plt.figure(4)
    plt.plot(YBB)
    plt.plot(YHH)
    plt.title(
        "Investment to Gross Domestic Product Ratio,\nObserved & Max, %d=100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Investment to GDP Ratio, {period[base_year]}=100")
    plt.grid()
    plt.figure(5)
    plt.plot(estimates)
    plt.title(
        "Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), %d=100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"GCF or CA, {period[base_year]}=100")
    plt.grid()
    plt.show()
