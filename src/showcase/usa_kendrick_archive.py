from matplotlib import pyplot as plt

from thesis.src.lib.pull import pull_series_ids_description


def usa_kendrick_archive(plot_douglas):
    # =============================================================================
    # Kendrick Macroeconomic Series
    # =============================================================================
    _MAP_SERIES = pull_series_ids_description('dataset_usa_kendrick.zip')

    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES, 1, 0,
                 8, 1, TITLES[0], 'Millions Of 1929 Dollars')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES, 2, 8,
                 19, 1, TITLES[1], 'Millions Of 1929 Dollars')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES, 3, 19,
                 30, 1, TITLES[2], 'Millions Of Current Dollars')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES, 4, 30,
                 38, 1, TITLES[3], 'Millions Of 1929 Dollars')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES,
                 5, 38, 46, 1, TITLES[4], 'Thousands')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES,
                 6, 46, 54, 1, TITLES[5], 'Millions')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES, 7, 54,
                 60, 1, TITLES[6], 'Millions Of 1929 Dollars')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES, 8, 60,
                 72, 1, TITLES[7], 'Millions Of 1929 Dollars')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES,
                 9, 72, 84, 1, TITLES[8], 'Percentage')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES,
                 10, 84, 96, 1, TITLES[9], 'Percentage')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES,
                 11, 96, 100, 1, TITLES[10], 'Percentage')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES,
                 12, 100, 111, 1, TITLES[11], 'Percentage')
    plot_douglas('dataset_usa_kendrick.zip', _MAP_SERIES,
                 13, 111, 118, 1, TITLES[12], 'Percentage')
    plt.show()
