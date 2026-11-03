import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def analyze_capital_productivity(df: pd.DataFrame) -> None:
    """
    Calculate and visualize capital acquisition indicators.

    Expected DataFrame structure:
        index: Year
        column 0: Nominal Investment
        column 1: Nominal Production
        column 2: Real Production
        column 3: Full Capacity Production
        column 4: Nominal Capital
        column 5: Labor
    """
    period = df.index.to_numpy()
    investment = df.iloc[:, 0].to_numpy()
    nominal_production = df.iloc[:, 1].to_numpy()
    real_production = df.iloc[:, 2].to_numpy()
    full_capacity_production = df.iloc[:, 3].to_numpy()
    fixed_assets = df.iloc[:, 4].to_numpy()
    labor = df.iloc[:, 5].to_numpy()
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
    YAA = real_production / fixed_assets
    YBB = investment * real_production[0] / (investment[0] * real_production)
    YCC = fixed_assets * labor[0] / (fixed_assets[0] * labor)
    YDD = real_production * labor[0] / (real_production[0] * labor)
    YEE = np.log(YCC)
    YFF = np.log(YDD)
    YGG = full_capacity_production / fixed_assets
    YHH = (
        investment
        * full_capacity_production[0]
        / (investment[0] * full_capacity_production)
    )
    YII = (
        full_capacity_production
        * labor[0]
        / (full_capacity_production[0] * labor)
    )
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
                        period[nodes[i]],
                        period[nodes[i + 1] - 1],
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
                                period[nodes[i + 1] - 1],
                            )
                        )
                    )
                )
                i += 1
            else:
                node = int(
                    input(
                        "Select Row for Year, Should Be More Than {}: = {}: ".format(
                            0, period[0]
                        )
                    )
                )
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
    # Estimate Gross Capital Formation / Capital Acquisitions
    ###########################################################################
    estimates = [pd.NA]
    for j in range(number_of_segments):
        for i in range(nodes[j], nodes[j + 1]):
            # Estimate: GCF[-] or CA[+]
            estimates.append(
                fixed_assets[i + 1]
                - fixed_assets[i]
                + gammas[j] * investment[i + 1]
            )
    estimates = pd.DataFrame(estimates, columns=["estimates"])
    ###########################################################################
    # Assemble Results
    ###########################################################################
    result = pd.DataFrame(period, index=df.index, columns=["year"])
    result = pd.concat(
        [
            result,
            YAA,
            YBB,
            YCC,
            YDD,
            YEE,
            YFF,
            YGG,
            YHH,
            YII,
            YJJ,
            estimates,
        ],
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
        "YGG",
        "YHH",
        "YII",
        "YJJ",
        "estimates",
    ]
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
    plt.plot(YCC, YDD)
    plt.plot(YCC, YII)
    plt.title(
        "Labor Productivity, Observed & Max, {} = 100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
            period[nodes[number_of_segments] - 1],
        )
    )
    plt.xlabel("Labor Capital Intensity")
    plt.ylabel("Labor Productivity, {} = 100".format(period[base_year]))
    plt.grid()
    plt.figure(2)
    plt.plot(YEE, YFF)
    plt.plot(YEE, YJJ)
    plt.title(
        "Log Labor Productivity, Observed & Max, {} = 100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
            period[nodes[number_of_segments] - 1],
        )
    )
    plt.xlabel("Log Labor Capital Intensity")
    plt.ylabel("Log Labor Productivity, {} = 100".format(period[base_year]))
    plt.grid()
    plt.figure(3)
    plt.plot(period, YAA)
    plt.plot(period, YGG)
    plt.title(
        "Fixed Assets Turnover ($\\lambda$), Observed & Max, {} = 100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
            period[nodes[number_of_segments] - 1],
        )
    )
    plt.xlabel("year")
    plt.ylabel(
        "Fixed Assets Turnover ($\\lambda$), {} = 100".format(
            period[base_year]
        )
    )
    plt.grid()
    plt.figure(4)
    plt.plot(period, YBB)
    plt.plot(period, YHH)
    plt.title(
        "Investment to Gross Domestic Product Ratio, \nObserved & Max, {} = 100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
            period[nodes[number_of_segments]],
        )
    )
    plt.xlabel("year")
    plt.ylabel(
        "Investment to Gross Domestic Product Ratio, {} = 100".format(
            period[base_year]
        )
    )
    plt.grid()
    plt.figure(5)
    plt.plot(period, estimates)
    plt.title(
        "Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {} = 100, {}$-${}".format(
            period[base_year],
            period[nodes[0]],
            period[nodes[number_of_segments] - 1],
        )
    )
    plt.xlabel("year")
    plt.ylabel("GCF or CA, {} = 100".format(period[base_year]))
    plt.grid()
    plt.show()


def analyze_capital_retirement(df: pd.DataFrame) -> None:
    """
    Expected DataFrame structure:
        index: Year
        column 0: Nominal Investment
        column 1: Nominal Production
        column 2: Real Production
        column 3: Nominal Capital
        column 4: Labor
    """
    period = df.index.to_numpy()
    investment = df.iloc[:, 0].to_numpy()
    nominal_production = df.iloc[:, 1].to_numpy()
    real_production = df.iloc[:, 2].to_numpy()
    fixed_assets = df.iloc[:, 3].to_numpy()
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
    YAA = np.log(fixed_assets * labor[0] / (fixed_assets[0] * labor))
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    YBB = np.log(real_production * labor[0] / (real_production[0] * labor))
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    YCC = investment * real_production[0] / (investment[0] * real_production)
    # Fixed Assets Turnover Ratio
    YDD = real_production / fixed_assets
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
                fixed_assets[i]
                - fixed_assets[i + 1]
                + gammas[j] * investment[i]
            )
            YEE.append(retirement_value)
            # Fixed Assets Retirement Ratio
            YFF.append(retirement_value / fixed_assets[i + 1])
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
    plt.plot(period, fixed_assets)
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


###############################################################################
# projectCapitalRetirement.py
###############################################################################
def run_retirement_option(
    period,
    investment,
    nominal_production,
    real_production,
    fixed_assets,
    labor,
) -> None:
    ###########################################################################
    # YEE.append(
    #     fixed_assets[i + 1] - fixed_assets[i] + gammas[j] * investment[i + 1]
    # )
    # YFF.append(
    #     (fixed_assets[i + 1] - fixed_assets[i] + gammas[j] * investment[i + 1])
    #     / fixed_assets[i + 1]
    # )
    ###########################################################################
    ###########################################################################
    # Replaced with
    ###########################################################################
    ###########################################################################
    # YEE.append(fixed_assets[i] - fixed_assets[i + 1] + gammas[j] * investment[i])
    # YFF.append(
    #     (fixed_assets[i] - fixed_assets[i + 1] + gammas[j] * investment[i])
    #     / fixed_assets[i + 1]
    # )
    ###########################################################################
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
    YAA = np.log(fixed_assets * labor[0] / (fixed_assets[0] * labor))
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    YBB = np.log(real_production * labor[0] / (real_production[0] * labor))
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    YCC = investment * real_production[0] / (investment[0] * real_production)
    YDD = real_production / fixed_assets  # Fixed Assets Turnover Ratio
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
                    "Define Gamma for Period from %d to %d: "
                    % (period[nodes[i]], period[nodes[i + 1]])
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
                            "Define Gamma for Period from %d to %d: "
                            % (period[nodes[i]], period[nodes[i + 1]])
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
                                "Define Gamma for Period from %d to %d: "
                                % (
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
    YEE = [pd.NA]  # Fixed Assets Retirement Value
    YFF = [pd.NA]  # Fixed Assets Retirement Ratio
    for j in range(number_of_segments):
        for i in range(nodes[j], nodes[j + 1]):
            # Fixed Assets Retirement Value
            YEE.append(
                fixed_assets[i]
                - fixed_assets[i + 1]
                + gammas[j] * investment[i]
            )
            # Fixed Assets Retirement Ratio
            YFF.append(
                (
                    fixed_assets[i]
                    - fixed_assets[i + 1]
                    + gammas[j] * investment[i]
                )
                / fixed_assets[i + 1]
            )
    YEE = pd.DataFrame(YEE, columns=["YEE"])
    YFF = pd.DataFrame(YFF, columns=["YFF"])
    df = pd.DataFrame(period, columns=["year"])
    df = pd.concat([df, YAA, YBB, YCC, YDD, YEE, YFF], axis=1)
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
        "Product, %d=100, %d$-$%d"
        % (base_year, period[0], period[nodes[number_of_segments]])
    )
    plt.xlabel("year")
    plt.ylabel(f"Product, {base_year}=100")
    plt.plot(period, real_production)
    plt.grid()
    plt.figure(2)
    plt.title(
        "Capital, %d=100, %d$-$%d"
        % (base_year, period[0], period[nodes[number_of_segments]])
    )
    plt.xlabel("year")
    plt.ylabel(f"Capital, {base_year}=100")
    plt.plot(period, fixed_assets)
    plt.grid()
    plt.figure(3)
    plt.title(
        "Fixed Assets Turnover, %d=100, %d$-$%d"
        % (base_year, period[0], period[nodes[number_of_segments]])
    )
    plt.xlabel("year")
    plt.ylabel(f"Fixed Assets Turnover, {base_year}=100")
    plt.plot(period, real_production / fixed_assets)
    plt.grid()
    plt.figure(4)
    plt.title(
        "Investment to Gross Domestic Product Ratio, %d=100, %d$-$%d"
        % (base_year, period[0], period[nodes[number_of_segments]])
    )
    plt.xlabel("year")
    plt.ylabel(
        "Investment to Gross Domestic Product Ratio, %d=100" % (base_year)
    )
    plt.plot(period, YCC)
    plt.grid()
    plt.figure(5)
    plt.title(
        "$\\mu(t)$, Fixed Assets Retirement Ratio, %d=100, %d$-$%d"
        % (base_year, period[0], period[nodes[number_of_segments]])
    )
    plt.xlabel("year")
    plt.ylabel(f"$\\mu(t)$, {base_year}=100")
    plt.plot(period, YFF)
    plt.grid()
    plt.figure(6)
    plt.title(
        "Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, %d=100, %d$-$%d"
        % (base_year, period[0], period[nodes[number_of_segments]])
    )
    plt.xlabel(f"$\\mu(t)$, {base_year}=100")
    plt.ylabel("Fixed Assets Retirement Value, %d=100" % (base_year))
    plt.plot(YFF, YEE)
    plt.grid()
    plt.figure(7)
    plt.title(
        "Labor Capital Intensity, %d=100, %d$-$%d"
        % (base_year, period[0], period[nodes[number_of_segments]])
    )
    plt.xlabel(f"Labor Capital Intensity, {base_year}=100")
    plt.ylabel(f"Labor Productivity, {base_year}=100")
    plt.plot(np.exp(YAA), np.exp(YBB))
    plt.grid()
    plt.show()
