#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:34:11 2023

@author: green-machine

Subproject XII. USA Douglas & Kendrick
"""


import pandas as pd
from matplotlib import pyplot as plt

from showcase.src.showcase.usa_douglas import usa_douglas
from showcase.src.showcase.usa_douglas_archive import usa_douglas_archive
from showcase.src.showcase.usa_kendrick import usa_kendrick
from showcase.src.showcase.usa_kendrick_archive import usa_kendrick_archive
from thesis.src.lib.constants import (TITLES_DEU, TITLES_DOUGLAS, TITLES_EUR,
                                      TITLES_KENDRICK)
from thesis.src.lib.pull import pull_by_series_id, pull_series_ids_description
from thesis.src.lib.read import read_usa_hist


def plot_douglas(archive_name, dictionary, num, start_at, stop, step, titles, measures, label=None):
    """
    df: Source Database,
    dictionary: Dictionary of Series Codes to Series Titles from Source Database,
    num: Plot Number,
    start: Start Series Code,
    stop: Stop Series Code,
    step: Step for Series Codes,
    title: Plot Title,
    measure: Dimenstion for Series,
    label: Additional Sublabels"""
    plt.figure(num)
    for _ in range(start_at, stop, step):
        plt.plot(read_usa_hist(archive_name).pipe(
            pull_by_series_id, key), label=MAP_SERIES_IDS[key])
    plt.title(titles)
    plt.xlabel('Period')
    plt.ylabel(measures)
    plt.grid()
    if label is None:
        plt.legend()
    else:
        plt.legend(label)


ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
MAP_SERIES_IDS = pull_series_ids_description(ARCHIVE_NAME)

ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, 21, 90, 115, 3,
             'Birth Rates by Countries', 'Births Rate Per 1000 People', TITLES_EUR)
plt.show()

# =============================================================================
# projectUSADouglas0001.py
# =============================================================================


ARCHIVE_NAME = 'dataset_douglas.zip'
MAP_SERIES_IDS = pull_series_ids_description(ARCHIVE_NAME)

plot_douglas(ARCHIVE_NAME, 1, 0, 12, 1, TITLES_DOUGLAS[0], 'Percentage')
plot_douglas(ARCHIVE_NAME, 2, 12, 23, 1, TITLES_DOUGLAS[1], 'Percentage')
plot_douglas(ARCHIVE_NAME, 3, 23, 34, 1, TITLES_DOUGLAS[2], 'Percentage')
plot_douglas(ARCHIVE_NAME, 4, 34, 45, 1, TITLES_DOUGLAS[3], 'Percentage')
plot_douglas(ARCHIVE_NAME, 5, 45, 55, 1, TITLES_DOUGLAS[4], 'Percentage')
plot_douglas(ARCHIVE_NAME, 6, 55, 66, 1, TITLES_DOUGLAS[5], 'Percentage')
plot_douglas(ARCHIVE_NAME, 7, 66, 76, 1, TITLES_DOUGLAS[6], 'Percentage')
plot_douglas(ARCHIVE_NAME, 8, 76, 86, 1, TITLES_DOUGLAS[7], 'Percentage')
plot_douglas(ARCHIVE_NAME, 9, 86, 89, 1, TITLES_DOUGLAS[8], 'Percentage')
plot_douglas(ARCHIVE_NAME, 10, 89, 90, 1, TITLES_DOUGLAS[9], 'Percentage')
plot_douglas(ARCHIVE_NAME, 11, 90, 93, 1, TITLES_DOUGLAS[10], 'Rate Per 1000')
plot_douglas(ARCHIVE_NAME, 12, 93, 96, 1, TITLES_DOUGLAS[11], 'Rate Per 1000')
plot_douglas(ARCHIVE_NAME, 13, 96, 99, 1, TITLES_DOUGLAS[12], 'Rate Per 1000')
plot_douglas(ARCHIVE_NAME, 14, 99, 102, 1, TITLES_DOUGLAS[13], 'Rate Per 1000')
plot_douglas(ARCHIVE_NAME, 15, 102, 105, 1, TITLES_DOUGLAS[14], 'Rate Per 1000')
plot_douglas(ARCHIVE_NAME, 16, 105, 111, 1,
             TITLES_DOUGLAS[15], 'Rate Per 1000', TITLES_DEU)
plot_douglas(ARCHIVE_NAME, 17, 111, 114, 1, TITLES_DOUGLAS[16], 'Rate Per 1000')
plot_douglas(ARCHIVE_NAME, 18, 114, 117, 1, TITLES_DOUGLAS[17], 'Rate Per 1000')
plot_douglas(ARCHIVE_NAME, 19, 117, 121, 1, TITLES_DOUGLAS[18], 'Mixed')
plot_douglas(ARCHIVE_NAME, 20, 121, 124, 1, TITLES_DOUGLAS[19], 'Millions of Dollars')
plot_douglas(ARCHIVE_NAME, 21, 90, 115, 3,
             TITLES_DOUGLAS[20], 'Births Rate Per 1000 People', TITLES_EUR)
plt.show()

# =============================================================================
# projectUSAKendrick0001.py
# =============================================================================


ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
MAP_SERIES_IDS = pull_series_ids_description(ARCHIVE_NAME)

plot_douglas(ARCHIVE_NAME, 1, 0, 8, 1, TITLES_KENDRICK[0], 'Dimension')
plot_douglas(ARCHIVE_NAME, 2, 8, 19, 1, TITLES_KENDRICK[1], 'Dimension')
plot_douglas(ARCHIVE_NAME, 3, 19, 30, 1, TITLES_KENDRICK[2], 'Dimension')
plot_douglas(ARCHIVE_NAME, 4, 30, 38, 1, TITLES_KENDRICK[3], 'Dimension')
plot_douglas(ARCHIVE_NAME, 5, 38, 46, 1, TITLES_KENDRICK[4], 'Dimension')
plot_douglas(ARCHIVE_NAME, 6, 46, 54, 1, TITLES_KENDRICK[5], 'Dimension')
# =============================================================================
# 'KTA10S07', 'KTA10S08' Not Working
# =============================================================================

plot_douglas(ARCHIVE_NAME, 7, 54, 60, 1, TITLES_KENDRICK[6], 'Dimension')
plot_douglas(ARCHIVE_NAME, 8, 62, 72, 1, TITLES_KENDRICK[7], 'Dimension')
plot_douglas(ARCHIVE_NAME, 9, 72, 84, 1, TITLES_KENDRICK[8], 'Dimension')
plot_douglas(ARCHIVE_NAME, 10, 84, 96, 1, TITLES_KENDRICK[9], 'Dimension')
plot_douglas(ARCHIVE_NAME, 11, 96, 100, 1, TITLES_KENDRICK[10], 'Dimension')
plot_douglas(ARCHIVE_NAME, 12, 100, 111, 1, TITLES_KENDRICK[11], 'Dimension')
plt.show()
# =============================================================================
# projectUSAKendrick0002.py
# =============================================================================


ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
MAP_SERIES_IDS = pull_series_ids_description(ARCHIVE_NAME)

plot_douglas(ARCHIVE_NAME,
             1, 0, 7, 1, 'Kendrick J.W. Indexes', 'Percentage')
plt.show()

# =============================================================================
# project_usa_douglas_kendrick.py
# =============================================================================


usa_douglas_archive(plot_douglas)

usa_kendrick_archive(plot_douglas)

usa_douglas(plot_douglas)

usa_kendrick(plot_douglas)
