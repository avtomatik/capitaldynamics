from matplotlib import pyplot as plt

from thesis.src.lib.constants import TITLES_KENDRICK
from thesis.src.lib.pull import pull_series_ids_description


def usa_kendrick_archive(plot_douglas):
    # =============================================================================
    # Kendrick Macroeconomic Series
    # =============================================================================
    ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
    MAP_SERIES_IDS = pull_series_ids_description(ARCHIVE_NAME)

    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 1, 0, 8, 1, TITLES_KENDRICK[0], 'Millions Of 1929 Dollars')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 2, 8, 19, 1, TITLES_KENDRICK[1], 'Millions Of 1929 Dollars')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 3, 19, 30, 1, TITLES_KENDRICK[2], 'Millions Of Current Dollars')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 4, 30, 38, 1, TITLES_KENDRICK[3], 'Millions Of 1929 Dollars')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 5, 38, 46, 1, TITLES_KENDRICK[4], 'Thousands')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 6, 46, 54, 1, TITLES_KENDRICK[5], 'Millions')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 7, 54, 60, 1, TITLES_KENDRICK[6], 'Millions Of 1929 Dollars')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 8, 60, 72, 1, TITLES_KENDRICK[7], 'Millions Of 1929 Dollars')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 9, 72, 84, 1, TITLES_KENDRICK[8], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 10, 84, 96, 1, TITLES_KENDRICK[9], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 11, 96, 100, 1, TITLES_KENDRICK[10], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 12, 100, 111, 1, TITLES_KENDRICK[11], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 13, 111, 118, 1, TITLES_KENDRICK[12], 'Percentage')
    plt.show()
