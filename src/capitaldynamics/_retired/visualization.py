import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def run_acquisition(
    period,
    investment,
    nominal_production,
    real_production,
    full_capacity_production,
    fixed_assets,
    labor,
    start,
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
    YAA = real_production / fixed_assets  # Fixed Assets Turnover Ratio
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    YBB = (
        investment
        * real_production[start]
        / (investment[start] * real_production)
    )
    # Labor Capital Intensity
    YCC = fixed_assets * labor[start] / (fixed_assets[start] * labor)
    YDD = (
        real_production * labor[start] / (real_production[start] * labor)
    )  # Labor Productivity
    YEE = np.log(YCC)  # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    YFF = np.log(YDD)  # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    YGG = (
        full_capacity_production / fixed_assets
    )  # Max: Fixed Assets Turnover Ratio
    # Max: Investment to Gross Domestic Product Ratio
    YHH = (
        investment
        * full_capacity_production[start]
        / (investment[start] * full_capacity_production)
    )
    # Max: Labor Productivity
    YII = (
        full_capacity_production
        * labor[start]
        / (full_capacity_production[start] * labor)
    )
    YJJ = np.log(YII)  # Max: Log Labor Productivity
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
    gammas = []
    nodes = [start]  # Gamma Switch Points & Gamma
    i = 0
    if number_of_segments == 1:
        nodes.append(len(period) - 1)
        gammas.append(
            float(
                input(
                    "Define Gamma for Period from %d to %d: "
                    % (period[nodes[i]], period[nodes[i + 1] - 1])
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
                            % (
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
                        "Select Row for Year, Should Be More Than %d:=%d: "
                        % (start, period[start])
                    )
                )
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
    YKK = [pd.NA] * (start + 1)
    for j in range(number_of_segments):
        for i in range(nodes[j], nodes[j + 1]):
            # Estimate: GCF[-] or CA[+]
            YKK.append(
                fixed_assets[i + 1]
                - fixed_assets[i]
                + gammas[j] * investment[i + 1]
            )
    YKK = pd.DataFrame(YKK, columns=["YKK"])
    df = pd.DataFrame(period, columns=["year"])
    df = pd.concat(
        [df, YAA, YBB, YCC, YDD, YEE, YFF, YGG, YHH, YII, YJJ, YKK], axis=1
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
        "YKK",
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
        "Labor Productivity, Observed & Max, %d=100, %d$-$%d"
        % (base_year, period[nodes[0]], period[nodes[number_of_segments] - 1])
    )
    plt.xlabel("Labor Capital Intensity")
    plt.ylabel(f"Labor Productivity, {base_year}=100")
    plt.grid()
    plt.figure(2)
    plt.plot(YEE, YFF)
    plt.plot(YEE, YJJ)
    plt.title(
        "Log Labor Productivity, Observed & Max, %d=100, %d$-$%d"
        % (base_year, period[nodes[0]], period[nodes[number_of_segments] - 1])
    )
    plt.xlabel("Log Labor Capital Intensity")
    plt.ylabel(f"Log Labor Productivity, {base_year}=100")
    plt.grid()
    plt.figure(3)
    plt.plot(period, YAA)
    plt.plot(period, YGG)
    plt.title(
        "Fixed Assets Turnover, Observed & Max, %d=100, %d$-$%d"
        % (base_year, period[nodes[0]], period[nodes[number_of_segments] - 1])
    )
    plt.xlabel("year")
    plt.ylabel(f"Fixed Assets Turnover, {base_year}=100")
    plt.grid()
    plt.figure(4)
    plt.plot(period, YBB)
    plt.plot(period, YHH)
    plt.title(
        "Investment to Gross Domestic Product Ratio,\nObserved & Max, %d=100, %d$-$%d"
        % (base_year, period[nodes[0]], period[nodes[number_of_segments]])
    )
    plt.xlabel("year")
    plt.ylabel(
        "Investment to Gross Domestic Product Ratio, %d=100" % (base_year)
    )
    plt.grid()
    plt.figure(5)
    plt.plot(period, YKK)
    plt.title(
        "Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), %d=100, %d$-$%d"
        % (base_year, period[nodes[0]], period[nodes[number_of_segments] - 1])
    )
    plt.xlabel("year")
    plt.ylabel(f"GCF or CA, {base_year}=100")
    plt.grid()
    plt.show()


def calculate_acquisition(df: pd.DataFrame) -> None:
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
    ###########################################################################
    # Calculate Static Values
    ###########################################################################

    YAA = df.iloc[:, 3].div(df.iloc[:, 5])  # Fixed Assets Turnover Ratio
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    YBB = df.iloc[:, 1].div(df.iloc[:, 3])
    YCC = df.iloc[:, 5].div(df.iloc[:, 6])  # Labor Capital Intensity
    YDD = df.iloc[:, 3].div(df.iloc[:, 6])  # Labor Productivity
    YBB = YBB.div(YBB[0])
    YCC = YCC.div(YCC[0])
    YDD = YDD.div(YDD[0])
    YEE = np.log(YCC)  # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    YFF = np.log(YDD)  # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    # Max: Fixed Assets Turnover Ratio
    YGG = df.iloc[:, 4].div(df.iloc[:, 5])
    # Max: Investment to Gross Domestic Product Ratio
    YHH = df.iloc[:, 1].div(df.iloc[:, 4])
    YII = df.iloc[:, 4].div(df.iloc[:, 6])  # Max: Labor Productivity
    YHH = YHH.div(YHH[0])
    YII = YII.div(YII[0])
    YJJ = np.log(YII)  # Max: Log Labor Productivity
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
        nodes.append(df.shape[0] - 1)
        gammas.append(
            float(
                input(
                    "Define Gamma for Period from {} to {}: ".format(
                        df.iloc[nodes[i], 0],
                        df.iloc[nodes[i + 1] - 1, 0],
                    )
                )
            )
        )
    elif number_of_segments >= 2:
        while i < number_of_segments:
            if i + 1 == number_of_segments:
                nodes.append(df.shape[0] - 1)
                gammas.append(
                    float(
                        input(
                            "Define Gamma for Period from {} to {}: ".format(
                                df.iloc[nodes[i], 0],
                                df.iloc[nodes[i + 1] - 1, 0],
                            )
                        )
                    )
                )
                i += 1
            else:
                node = int(
                    input(
                        "Select Row for Year, Should Be More Than {}: = {}: ".format(
                            0, df.iloc[0, 0]
                        )
                    )
                )
                if node > nodes[i]:
                    nodes.append(node)
                    gammas.append(
                        float(
                            input(
                                "Define Gamma for Period from {} to {}: ".format(
                                    df.iloc[nodes[i], 0],
                                    df.iloc[nodes[i + 1], 0],
                                )
                            )
                        )
                    )
                    i += 1
    else:
        print("Error")
    YKK = [pd.NA]
    for j in range(number_of_segments):
        for i in range(nodes[j], nodes[j + 1]):
            # Estimate: GCF[-] or CA[+]
            YKK.append(
                df.iloc[i + 1, 5]
                - df.iloc[i, 5]
                + gammas[j] * df.iloc[i + 1, 1]
            )
    YKK = pd.DataFrame(YKK, columns=["YKK"])
    result = pd.DataFrame(df.iloc[:, 0], columns=["year"])
    result = pd.concat(
        [result, YAA, YBB, YCC, YDD, YEE, YFF, YGG, YHH, YII, YJJ, YKK],
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
        "YKK",
    ]
    # {"-": "Gross Capital Formation", "+": "Capital Acquisitions"}
    for i in range(number_of_segments):
        end = nodes[i + 1] - 1 if i == number_of_segments - 1 else nodes[i + 1]
        print(
            "Model Parameter: Gamma for Period from "
            f"{df.iloc[nodes[i], 0]} to {df.iloc[end, 0]}: "
            f"{gammas[i]:.6f}"
        )
    plt.figure(1)
    plt.plot(YCC, YDD)
    plt.plot(YCC, YII)
    plt.title(
        "Labor Productivity, Observed & Max, {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[nodes[0], 0],
            df.iloc[nodes[number_of_segments] - 1, 0],
        )
    )
    plt.xlabel("Labor Capital Intensity")
    plt.ylabel("Labor Productivity, {} = 100".format(df.iloc[base_year, 0]))
    plt.grid()
    plt.figure(2)
    plt.plot(YEE, YFF)
    plt.plot(YEE, YJJ)
    plt.title(
        "Log Labor Productivity, Observed & Max, {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[nodes[0], 0],
            df.iloc[nodes[number_of_segments] - 1, 0],
        )
    )
    plt.xlabel("Log Labor Capital Intensity")
    plt.ylabel(
        "Log Labor Productivity, {} = 100".format(df.iloc[base_year, 0])
    )
    plt.grid()
    plt.figure(3)
    plt.plot(df.iloc[:, 0], YAA)
    plt.plot(df.iloc[:, 0], YGG)
    plt.title(
        "Fixed Assets Turnover ($\\lambda$), Observed & Max, {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[nodes[0], 0],
            df.iloc[nodes[number_of_segments] - 1, 0],
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
    plt.plot(df.iloc[:, 0], YBB)
    plt.plot(df.iloc[:, 0], YHH)
    plt.title(
        "Investment to Gross Domestic Product Ratio, \nObserved & Max, {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[nodes[0], 0],
            df.iloc[nodes[number_of_segments], 0],
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
    plt.plot(df.iloc[:, 0], YKK)
    plt.title(
        "Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[nodes[0], 0],
            df.iloc[nodes[number_of_segments] - 1, 0],
        )
    )
    plt.xlabel("year")
    plt.ylabel("GCF or CA, {} = 100".format(df.iloc[base_year, 0]))
    plt.grid()
    plt.show()


def run_retirement(
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
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    YAA = np.log(fixed_assets * labor[0] / (fixed_assets[0] * labor))
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    YBB = np.log(real_production * labor[0] / (real_production[0] * labor))
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
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
    ###########################################################################
    # Fixed Assets Retirement Value
    ###########################################################################
    YEE = [pd.NA]
    ###########################################################################
    # Fixed Assets Retirement Ratio
    ###########################################################################
    YFF = [pd.NA]
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
        "Investment to GDP Ratio, %d=100, %d$-$%d"
        % (base_year, period[0], period[nodes[number_of_segments]])
    )
    plt.xlabel("year")
    plt.ylabel(f"Investment to GDP Ratio, {base_year}=100")
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
    #     fixed_assets[i + 1] - fixed_assets[i] + gmm[j] * investment[i + 1]
    # )
    # YFF.append(
    #     (fixed_assets[i + 1] - fixed_assets[i] + gmm[j] * investment[i + 1])
    #     / fixed_assets[i + 1]
    # )
    ###########################################################################
    ###########################################################################
    # Replaced with
    ###########################################################################
    ###########################################################################
    # YEE.append(fixed_assets[i] - fixed_assets[i + 1] + gmm[j] * investment[i])
    # YFF.append(
    #     (fixed_assets[i] - fixed_assets[i + 1] + gmm[j] * investment[i])
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


def calculate_retirement(df: pd.DataFrame) -> None:
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
    ###########################################################################
    # Calculate Static Values
    ###########################################################################

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
        nodes.append(df.shape[0] - 1)
        gammas.append(
            float(
                input(
                    "Define Gamma for Period from {} to {}: ".format(
                        df.iloc[nodes[i], 0],
                        df.iloc[:, 0][nodes[i + 1]],
                    )
                )
            )
        )
    elif number_of_segments >= 2:
        while i < number_of_segments:
            if i + 1 == number_of_segments:
                nodes.append(df.shape[0] - 1)
                gammas.append(
                    float(
                        input(
                            "Define Gamma for Period from {} to {}: ".format(
                                df.iloc[nodes[i], 0],
                                df.iloc[nodes[i + 1], 0],
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
                                    df.iloc[nodes[i], 0],
                                    df.iloc[nodes[i + 1], 0],
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
                df.iloc[i, 4] - df.iloc[i + 1, 4] + gammas[j] * df.iloc[i, 1]
            )
            # Fixed Assets Retirement Ratio
            YFF.append(
                (df.iloc[i, 4] - df.iloc[i + 1, 4] + gammas[j] * df.iloc[i, 1])
                / df.iloc[i + 1, 4]
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
    for i in range(number_of_segments):
        end = nodes[i + 1] - 1 if i == number_of_segments - 1 else nodes[i + 1]
        print(
            "Model Parameter: Gamma for Period from "
            f"{df.iloc[nodes[i], 0]} to {df.iloc[end, 0]}: "
            f"{gammas[i]:.6f}"
        )
    plt.figure(1)
    plt.title(
        "Product, {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[0, 0],
            df.iloc[nodes[number_of_segments], 0],
        )
    )
    plt.xlabel("year")
    plt.ylabel("Product, {} = 100".format(df.iloc[base_year, 0]))
    plt.plot(df.iloc[:, 0], df.iloc[:, 3])
    plt.grid()
    plt.figure(2)
    plt.title(
        "Capital, {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[0, 0],
            df.iloc[nodes[number_of_segments], 0],
        )
    )
    plt.xlabel("year")
    plt.ylabel("Capital, {} = 100".format(df.iloc[base_year, 0]))
    plt.plot(df.iloc[:, 0], df.iloc[:, 4])
    plt.grid()
    plt.figure(3)
    plt.title(
        "Fixed Assets Turnover ($\\lambda$), {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[0, 0],
            df.iloc[nodes[number_of_segments], 0],
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
            df.iloc[base_year, 0],
            df.iloc[0, 0],
            df.iloc[nodes[number_of_segments], 0],
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
            df.iloc[base_year, 0],
            df.iloc[0, 0],
            df.iloc[nodes[number_of_segments], 0],
        )
    )
    plt.xlabel("year")
    plt.ylabel("$\\alpha(t)$, {} = 100".format(df.iloc[base_year, 0]))
    plt.plot(df.iloc[:, 0], YFF)
    plt.grid()
    plt.figure(6)
    plt.title(
        "Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[0, 0],
            df.iloc[nodes[number_of_segments], 0],
        )
    )
    plt.xlabel("$\\alpha(t)$, {} = 100".format(df.iloc[base_year, 0]))
    plt.ylabel(
        "Fixed Assets Retirement Value, {} = 100".format(df.iloc[base_year, 0])
    )
    plt.plot(YFF, YEE)
    plt.grid()
    plt.figure(7)
    plt.title(
        "Labor Capital Intensity, {} = 100, {}$-${}".format(
            df.iloc[base_year, 0],
            df.iloc[0, 0],
            df.iloc[nodes[number_of_segments], 0],
        )
    )
    plt.xlabel(
        "Labor Capital Intensity, {} = 100".format(df.iloc[base_year, 0])
    )
    plt.ylabel("Labor Productivity, {} = 100".format(df.iloc[base_year, 0]))
    plt.plot(np.exp(YAA), np.exp(YBB))
    plt.grid()
    plt.show()
