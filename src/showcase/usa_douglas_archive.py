from matplotlib import pyplot as plt

from thesis.src.common import get_fig_map_us_ma
from thesis.src.lib.plot import plot_cobb_douglas
from thesis.src.lib.pull import pull_series_ids_description
from thesis.src.lib.stockpile import stockpile_usa_hist
from thesis.src.lib.transform import transform_cobb_douglas


def usa_douglas_archive(plot_douglas):
    # =============================================================================
    # Douglas European Demographics & Growth of US Capital
    # =============================================================================
    _MAP_SERIES = pull_series_ids_description('dataset_douglas.zip')

    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 1, 0, 12, 1, TITLES[0], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 2, 12, 23, 1, TITLES[1], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 3, 23, 34, 1, TITLES[2], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 4, 34, 45, 1, TITLES[3], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 5, 45, 55, 1, TITLES[4], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 6, 55, 66, 1, TITLES[5], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 7, 66, 76, 1, TITLES[6], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 8, 76, 86, 1, TITLES[7], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 9, 86, 89, 1, TITLES[8], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 10, 89, 90, 1, TITLES[9], 'Percentage')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 11,
                 90, 93, 1, TITLES[10], 'Rate Per 1000')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 12,
                 93, 96, 1, TITLES[11], 'Rate Per 1000')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 13,
                 96, 99, 1, TITLES[12], 'Rate Per 1000')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 14,
                 99, 102, 1, TITLES[13], 'Rate Per 1000')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 15,
                 102, 105, 1, TITLES[14], 'Rate Per 1000')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 16, 105,
                 111, 1, TITLES[15], 'Rate Per 1000', TITLES_DEU)
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 17,
                 111, 114, 1, TITLES[16], 'Rate Per 1000')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 18,
                 114, 117, 1, TITLES[17], 'Rate Per 1000')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES,
                 19, 117, 121, 1, TITLES[18], 'Mixed')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 20, 121,
                 124, 1, TITLES[19], 'Millions of Dollars')
    plot_douglas('dataset_douglas.zip', _MAP_SERIES, 21, 90, 115,
                 3, TITLES[20], 'Births Rate Per 1000 People', TITLES_EUR)
    plt.show()

    # =============================================================================
    # Douglas Production Function
    # =============================================================================
    YEAR_BASE = 1899
    plot_cobb_douglas(
        *stockpile_usa_hist(SERIES_IDS).pipe(transform_cobb_douglas, year_base=YEAR_BASE), get_fig_map_us_ma(YEAR_BASE))
