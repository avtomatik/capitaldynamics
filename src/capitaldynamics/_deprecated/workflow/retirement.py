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


def plot_retirement(df: pd.DataFrame) -> None:
    """
    Interactive Shell for Processing Capital Retirement
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal Investment
        df.iloc[:, 1]      Nominal Production
        df.iloc[:, 2]      Real Production
        df.iloc[:, 3]      Real Capital
        df.iloc[:, 4]      Labor
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
    # Labor Capital Intensity
    ###########################################################################
    _df["lab_cap_int_log_bas"] = _df.iloc[:, 4].div(_df.iloc[:, 5])
    ###########################################################################
    # Labor Productivity
    ###########################################################################
    _df["lab_product_log_bas"] = _df.iloc[:, 3].div(_df.iloc[:, 5])
    ###########################################################################
    # Investment to Gross Domestic Product Ratio
    ###########################################################################
    _df["inv_to_gdp"] = _df.iloc[:, 1].div(_df.iloc[:, 3])
    ###########################################################################
    # Basing
    ###########################################################################
    _df.iloc[:, -3:] = _df.iloc[:, -3:].div(_df.iloc[0, -3:])
    ###########################################################################
    # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    ###########################################################################
    _df.iloc[:, -3] = np.log(_df.iloc[:, -3])
    ###########################################################################
    # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    ###########################################################################
    _df.iloc[:, -2] = np.log(_df.iloc[:, -2])
    ###########################################################################
    # Fixed Assets Turnover Ratio
    ###########################################################################
    _df["c_turnover"] = _df.iloc[:, 3].div(_df.iloc[:, 4])
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
                        _df.iloc[nodes[i], 0], _df.iloc[nodes[i + 1], 0]
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
                                _df.iloc[nodes[i + 1], 0],
                            )
                        )
                    )
                )
            else:
                node = int(input("Select Row for Year: "))
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
                _df.iloc[i, 4]
                - _df.iloc[i + 1, 4]
                + gammas[j] * _df.iloc[i, 1]
            )
            ###################################################################
            # Fixed Assets Retirement Ratio
            ###################################################################
            ratios.append(
                (
                    _df.iloc[i, 4]
                    - _df.iloc[i + 1, 4]
                    + gammas[j] * _df.iloc[i, 1]
                )
                / _df.iloc[i + 1, 4]
            )
    _df = pd.concat(
        [
            _df,
            pd.DataFrame(values, columns=["values"]),
            pd.DataFrame(ratios, columns=["ratios"]),
        ],
        axis=1,
    )
    _df.set_index(_df.columns[0], inplace=True)
    _df["_ratio_deviation_abs"] = (
        _df.iloc[:, 10].sub(_df.iloc[:, 10].mean()).abs()
    )
    _df["_ratio_increment_abs"] = _df.iloc[:, 10].diff().abs()
    for i in range(number_of_segments):
        end = nodes[i + 1] - 1 if i == number_of_segments - 1 else nodes[i + 1]
        print(
            "Model Parameter: Gamma for Period from "
            f"{_df.index[nodes[i]]} to {_df.index[end]}: "
            f"{gammas[i]:.6f}"
        )
    plt.figure(1)
    plt.title("Product, {}=100, {}$-${}".format(_b, *df.index[[0, -1]]))
    plt.xlabel("year")
    plt.ylabel(f"Product, {_b}=100")
    plt.plot(_df.iloc[:, 2])
    plt.grid()
    plt.figure(2)
    plt.title("Capital, {}=100, {}$-${}".format(_b, *df.index[[0, -1]]))
    plt.xlabel("year")
    plt.ylabel(f"Capital, {_b}=100")
    plt.plot(_df.iloc[:, 3])
    plt.grid()
    plt.figure(3)
    plt.title(
        "Fixed Assets Turnover ($\\lambda$), {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Fixed Assets Turnover ($\\lambda$), {_b}=100")
    plt.plot(_df.iloc[:, 2].div(_df.iloc[:, 3]))
    plt.grid()
    plt.figure(4)
    plt.title(
        "Investment to Gross Domestic Product Ratio, {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"Investment to Gross Domestic Product Ratio, {_b}=100")
    plt.plot(_df.iloc[:, 7])
    plt.grid()
    plt.figure(5)
    plt.title(
        "$\\alpha(t)$, Fixed Assets Retirement Ratio, {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel("year")
    plt.ylabel(f"$\\alpha(t)$, {_b}=100")
    plt.plot(_df.iloc[:, 9])
    plt.grid()
    plt.figure(6)
    plt.title(
        "Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel(f"$\\alpha(t)$, {_b}=100")
    plt.ylabel(f"Fixed Assets Retirement Value, {_b}=100")
    plt.plot(_df.iloc[:, 9], _df.iloc[:, 8])
    plt.grid()
    plt.figure(7)
    plt.title(
        "Labor Capital Intensity, {}=100, {}$-${}".format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel(f"Labor Capital Intensity, {_b}=100")
    plt.ylabel(f"Labor Productivity, {_b}=100")
    plt.plot(np.exp(_df.iloc[:, 5]), np.exp(_df.iloc[:, 6]))
    plt.grid()
    plt.show()
