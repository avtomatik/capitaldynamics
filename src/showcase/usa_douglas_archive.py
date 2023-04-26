from matplotlib import pyplot as plt

from thesis.src.lib.constants import TITLES_DEU, TITLES_DOUGLAS, TITLES_EUR
from thesis.src.lib.pull import pull_series_ids_description


def usa_douglas_archive(plot_douglas):
    # =============================================================================
    # Douglas European Demographics & Growth of US Capital
    # =============================================================================
    ARCHIVE_NAME = 'dataset_douglas.zip'
    MAP_SERIES_IDS = pull_series_ids_description(ARCHIVE_NAME)

    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 1, 0, 12, 1, TITLES_DOUGLAS[0], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 2, 12, 23, 1, TITLES_DOUGLAS[1], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 3, 23, 34, 1, TITLES_DOUGLAS[2], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 4, 34, 45, 1, TITLES_DOUGLAS[3], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 5, 45, 55, 1, TITLES_DOUGLAS[4], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 6, 55, 66, 1, TITLES_DOUGLAS[5], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 7, 66, 76, 1, TITLES_DOUGLAS[6], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 8, 76, 86, 1, TITLES_DOUGLAS[7], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 9, 86, 89, 1, TITLES_DOUGLAS[8], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 10, 89, 90, 1, TITLES_DOUGLAS[9], 'Percentage')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 11, 90, 93, 1, TITLES_DOUGLAS[10], 'Rate Per 1000')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 12, 93, 96, 1, TITLES_DOUGLAS[11], 'Rate Per 1000')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 13, 96, 99, 1, TITLES_DOUGLAS[12], 'Rate Per 1000')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 14, 99, 102, 1, TITLES_DOUGLAS[13], 'Rate Per 1000')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 15, 102, 105, 1, TITLES_DOUGLAS[14], 'Rate Per 1000')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 16, 105, 111, 1, TITLES_DOUGLAS[15], 'Rate Per 1000', TITLES_DEU)
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 17, 111, 114, 1, TITLES_DOUGLAS[16], 'Rate Per 1000')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 18, 114, 117, 1, TITLES_DOUGLAS[17], 'Rate Per 1000')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 19, 117, 121, 1, TITLES_DOUGLAS[18], 'Mixed')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 20, 121, 124, 1, TITLES_DOUGLAS[19], 'Millions of Dollars')
    plot_douglas(ARCHIVE_NAME, MAP_SERIES_IDS, 21, 90, 115, 3, TITLES_DOUGLAS[20], 'Births Rate Per 1000 People', TITLES_EUR)
    plt.show()
