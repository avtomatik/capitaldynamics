import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_price_base_nr(df: pd.DataFrame, columns: tuple[int] = (0, 1)) -> int:
    """
    Determine Base Year

    Parameters
    ----------
    df : pd.DataFrame
        ======================== ===========================
        df.index                 Period
        ...                      ...
        df.iloc[:, columns[0]]   Nominal
        df.iloc[:, columns[-1]]  Real
        ======================== ===========================
    columns : tuple[int], optional
        Column Nominal, Column Real. The default is (0, 1).

    Returns
    -------
    int
        Base Year.

    """
    df["__deflator"] = (
        df.iloc[:, columns[0]].div(df.iloc[:, columns[-1]]).sub(1).abs()
    )
    return int(df.index[df.iloc[:, -1].argmin()])


def plot_acquisition(df: pd.DataFrame) -> None:
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
        df.iloc[:, 4]      Real Capital
        df.iloc[:, 5]      Labor
        ================== =================================
    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.
    """
    _df = df.reset_index(level=0).copy()
    _df.columns = ["year", *_df.columns[1:]]
    ###########################################################################
    # Basic Year
    ###########################################################################
    ###########################################################################
    # Define Basic Year for Deflator
    ###########################################################################
    _b = _df.pipe(get_price_base_nr, columns=(2, 3))
    _df.drop(_df.columns[-1], axis=1, inplace=True)
    ###########################################################################
    # Calculate Static Values
    ###########################################################################
    ###########################################################################
    # Fixed Assets Turnover Ratio
    ###########################################################################
    _df["c_turnover"] = _df.iloc[:, 3].div(_df.iloc[:, 5])
    ###########################################################################
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I_0/Y_0)
    ###########################################################################
    _df["inv_to_gdp"] = _df.iloc[:, 1].div(_df.iloc[:, 3])
    ###########################################################################
    # Labor Capital Intensity
    ###########################################################################
    _df["lab_cap_int"] = _df.iloc[:, 5].div(_df.iloc[:, 6])
    ###########################################################################
    # Labor Productivity
    ###########################################################################
    _df["lab_product"] = _df.iloc[:, 3].div(_df.iloc[:, 6])
    _df.iloc[:, -3:] = _df.iloc[:, -3:].div(_df.iloc[0, -3:])
    ###########################################################################
    # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    ###########################################################################
    _df[f"{_df.columns[-2]}_log_bas"] = np.log(_df.iloc[:, -2])
    ###########################################################################
    # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    ###########################################################################
    _df[f"{_df.columns[-2]}_log_bas"] = np.log(_df.iloc[:, -2])
    ###########################################################################
    # Max: Fixed Assets Turnover Ratio
    ###########################################################################
    _df[f"{_df.columns[-6]}_max"] = _df.iloc[:, 4].div(_df.iloc[:, 5])
    ###########################################################################
    # Max: Investment to Gross Domestic Product Ratio
    ###########################################################################
    _df[f"{_df.columns[-6]}_max"] = _df.iloc[:, 1].div(_df.iloc[:, 4])
    ###########################################################################
    # Max: Labor Productivity
    ###########################################################################
    _df[f"{_df.columns[-5]}_max"] = _df.iloc[:, 4].div(_df.iloc[:, 6])
    _df.iloc[:, -2:] = _df.iloc[:, -2:].div(_df.iloc[0, -2:])
    ###########################################################################
    # Max: Log Labor Productivity
    ###########################################################################
    _df[f"{_df.columns[-1]}_log_bas"] = np.log(_df.iloc[:, -1])
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
        nodes.append(_df.index[-1])
        gammas.append(
            float(
                input(
                    "Define Gamma for Period from {} to {}: ".format(
                        _df.iloc[nodes[i], 0], _df.iloc[nodes[i + 1] - 1, 0]
                    )
                )
            )
        )
    elif number_of_segments >= 2:
        while i < number_of_segments:
            if i + 1 == number_of_segments:
                nodes.append(_df.index[-1])
                gammas.append(
                    float(
                        input(
                            "Define Gamma for Period from {} to {}: ".format(
                                _df.iloc[nodes[i], 0],
                                _df.iloc[nodes[i + 1] - 1, 0],
                            )
                        )
                    )
                )
            else:
                node = int(
                    input(
                        "Select Row for Year, Should Be More Than {}: = {}: ".format(
                            0, _df.iloc[0, 0]
                        )
                    )
                )
                if node > nodes[i]:
                    nodes.append(node)
                    gammas.append(
                        float(
                            input(
                                "Define Gamma for Period from {} to {}: ".format(
                                    _df.iloc[nodes[i], 0],
                                    _df.iloc[nodes[i + 1], 0],
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
    estimates = [pd.NA]
    for j in range(number_of_segments):
        for i in range(nodes[j], nodes[j + 1]):
            ###################################################################
            # Estimate: GCF[-] or CA[+]
            ###################################################################
            estimates.append(
                _df.iloc[i + 1, 5]
                - _df.iloc[i, 5]
                + gammas[j] * _df.iloc[i + 1, 1]
            )
    _df = pd.concat(
        [_df, pd.DataFrame(estimates, columns=["_calculated"])], axis=1
    )
    _df.set_index(_df.columns[0], inplace=True)
    # {"-": "Gross Capital Formation", "+": "Capital Acquisitions"}
    for i in range(number_of_segments):
        end = nodes[i + 1] - 1 if i == number_of_segments - 1 else nodes[i + 1]
        print(
            "Model Parameter: Gamma for Period from "
            f"{_df.index[nodes[i]]} to {_df.index[end]}: "
            f"{gammas[i]:.6f}"
        )
    plt.figure(1)
    plt.plot(_df.iloc[:, 8], _df.iloc[:, 9])
    plt.plot(_df.iloc[:, 8], _df.iloc[:, 14])
    plt.title(
        "Labor Productivity, Observed & Max, {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel("Labor Capital Intensity")
    plt.ylabel(f"Labor Productivity, {_b}=100")
    plt.grid()
    plt.figure(2)
    plt.plot(_df.iloc[:, 10], _df.iloc[:, 11])
    plt.plot(_df.iloc[:, 10], _df.iloc[:, 15])
    plt.title(
        "Log Labor Productivity, Observed & Max, {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel("Log Labor Capital Intensity")
    plt.ylabel(f"Log Labor Productivity, {_b}=100")
    plt.grid()
    plt.figure(3)
    plt.plot(_df.iloc[:, 6])
    plt.plot(_df.iloc[:, 12])
    plt.title(
        "Fixed Assets Turnover ($\\lambda$), Observed & Max, {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Fixed Assets Turnover ($\\lambda$), {_b}=100")
    plt.grid()
    plt.figure(4)
    plt.plot(_df.iloc[:, 7])
    plt.plot(_df.iloc[:, 13])
    plt.title(
        "Investment to Gross Domestic Product Ratio,\nObserved & Max, {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Investment to Gross Domestic Product Ratio, {_b}=100")
    plt.grid()
    plt.figure(5)
    plt.plot(_df.iloc[:, 16])
    plt.title(
        "Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"GCF or CA, {_b}=100")
    plt.grid()
    plt.show()
