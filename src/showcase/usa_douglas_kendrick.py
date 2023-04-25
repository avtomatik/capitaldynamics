#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:34:11 2023

@author: green-machine

Subproject XII. USA Douglas & Kendrick
"""


from matplotlib import pyplot as plt

from showcase.src.showcase.usa_douglas import usa_douglas
from showcase.src.showcase.usa_douglas_archive import usa_douglas_archive
from showcase.src.showcase.usa_kendrick import usa_kendrick
from showcase.src.showcase.usa_kendrick_archive import usa_kendrick_archive
from thesis.src.lib.pull import pull_series_ids_description
from thesis.src.lib.read import read_usa_hist


def plotSpecialLabels(archive_id, num, start, stop, step, title, measure, label):
    plt.figure(num)
    for _ in range(start, stop, step):
        plt.plot(read_usa_hist(
            archive_id, _MAP_SERIES.iloc[_, 0]), label=_MAP_SERIES.iloc[_, 1])
    plt.title(title)
    plt.xlabel('Period')
    plt.ylabel(measure)
    plt.grid()
    plt.legend(label)


_MAP_SERIES = pull_series_ids_description('dataset_usa_kendrick.zip')

plotSpecialLabels('dataset_douglas.zip', 21, 90, 115,
                  3, 'Birth Rates by Countries', 'Births Rate Per 1000 People', TITLES_EUR)
plt.show()

# =============================================================================
# projectUSADouglas0001.py
# =============================================================================


def plot_douglas(archive_name, num, start_at, stop, step, titles, measures):
    plt.figure(num)
    for _ in range(start_at, stop, step):
        plt.plot(read_usa_hist(
            archive_name, _MAP_SERIES.iloc[_, 0]), label=_MAP_SERIES.iloc[_, 1])
    plt.title(titles)
    plt.xlabel('Period')
    plt.ylabel(measures)
    plt.grid()
    plt.legend()


def plot_douglas_labels(archive_name, num, start_at, stop, step, titles, measures, label):
    plt.figure(num)
    for _ in range(start_at, stop, step):
        plt.plot(read_usa_hist(
            archive_name, _MAP_SERIES.iloc[_, 0]), label=_MAP_SERIES.iloc[_, 1])
    plt.title(titles)
    plt.xlabel('Period')
    plt.ylabel(measures)
    plt.grid()
    plt.legend(label)


_MAP_SERIES = pull_series_ids_description('dataset_douglas.zip')

plot_douglas('dataset_douglas.zip', 1, 0, 12, 1, TITLES[0], 'Percentage')
plot_douglas('dataset_douglas.zip', 2, 12, 23, 1, TITLES[1], 'Percentage')
plot_douglas('dataset_douglas.zip', 3, 23, 34, 1, TITLES[2], 'Percentage')
plot_douglas('dataset_douglas.zip', 4, 34, 45, 1, TITLES[3], 'Percentage')
plot_douglas('dataset_douglas.zip', 5, 45, 55, 1, TITLES[4], 'Percentage')
plot_douglas('dataset_douglas.zip', 6, 55, 66, 1, TITLES[5], 'Percentage')
plot_douglas('dataset_douglas.zip', 7, 66, 76, 1, TITLES[6], 'Percentage')
plot_douglas('dataset_douglas.zip', 8, 76, 86, 1, TITLES[7], 'Percentage')
plot_douglas('dataset_douglas.zip', 9, 86, 89, 1, TITLES[8], 'Percentage')
plot_douglas('dataset_douglas.zip', 10, 89, 90, 1, TITLES[9], 'Percentage')
plot_douglas('dataset_douglas.zip', 11, 90, 93, 1, TITLES[10], 'Rate Per 1000')
plot_douglas('dataset_douglas.zip', 12, 93, 96, 1, TITLES[11], 'Rate Per 1000')
plot_douglas('dataset_douglas.zip', 13, 96, 99, 1, TITLES[12], 'Rate Per 1000')
plot_douglas('dataset_douglas.zip', 14, 99, 102,
             1, TITLES[13], 'Rate Per 1000')
plot_douglas('dataset_douglas.zip', 15, 102,
             105, 1, TITLES[14], 'Rate Per 1000')
plot_douglas_labels('dataset_douglas.zip', 16, 105, 111, 1,
                    TITLES[15], 'Rate Per 1000', TITLES_DEU)
plot_douglas('dataset_douglas.zip', 17, 111,
             114, 1, TITLES[16], 'Rate Per 1000')
plot_douglas('dataset_douglas.zip', 18, 114,
             117, 1, TITLES[17], 'Rate Per 1000')
plot_douglas('dataset_douglas.zip', 19, 117, 121, 1, TITLES[18], 'Mixed')
plot_douglas('dataset_douglas.zip', 20, 121, 124,
             1, TITLES[19], 'Millions of Dollars')
plot_douglas_labels('dataset_douglas.zip', 21, 90, 115, 3,
                    TITLES[20], 'Births Rate Per 1000 People', TITLES_EUR)
plt.show()

# =============================================================================
# projectUSAKendrick0001.py
# =============================================================================


_MAP_SERIES = pull_series_ids_description('dataset_usa_kendrick.zip')


plot_douglas('dataset_usa_kendrick.zip', 1, 0, 8, 1, TITLES[0], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 2, 8, 19, 1, TITLES[1], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 3, 19, 30, 1, TITLES[2], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 4, 30, 38, 1, TITLES[3], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 5, 38, 46, 1, TITLES[4], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 6, 46, 54, 1, TITLES[5], 'Dimension')
# =============================================================================
# 'KTA10S07', 'KTA10S08' Not Working
# =============================================================================

plot_douglas('dataset_usa_kendrick.zip', 7, 54, 60, 1, TITLES[6], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 8, 62, 72, 1, TITLES[7], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 9, 72, 84, 1, TITLES[8], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 10, 84, 96, 1, TITLES[9], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 11, 96,
             100, 1, TITLES[10], 'Dimension')
plot_douglas('dataset_usa_kendrick.zip', 12, 100,
             111, 1, TITLES[11], 'Dimension')
plt.show()
# =============================================================================
# projectUSAKendrick0002.py
# =============================================================================


def plot_douglas(archive_name, num, start_at, stop, step, titles, measures):
    '''Same, But Flat Dictionary'''
    plt.figure(num)
    for _ in range(start_at, stop, step):
        plt.plot(read_usa_hist(
            archive_name, _MAP_SERIES.iloc[_, 0]), label=_MAP_SERIES.iloc[_, 0])
    plt.title(titles)
    plt.xlabel('Period')
    plt.ylabel(measures)
    plt.grid()
    plt.legend()


_MAP_SERIES = pd.read_csv('dataset_usa_kendrick.zip',
                          usecols=[4]).drop_duplicates()
_MAP_SERIES = _MAP_SERIES.reset_index(drop=True)

plot_douglas('dataset_usa_kendrick.zip',
             1, 0, 7, 1, 'Kendrick J.W. Indexes', 'Percentage')
plt.show()

# =============================================================================
# project_usa_douglas_kendrick.py
# =============================================================================


def plot_douglas(df, dictionary, num, start, stop, step, title, measure, label=None):
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
    for _ in range(start, stop, step):
        plt.plot(read_usa_hist(
            df, dictionary.iloc[_, 0]), label=dictionary.iloc[_, 1])
    plt.title(title)
    plt.xlabel('Period')
    plt.ylabel(measure)
    plt.grid()
    if label is None:
        plt.legend()
    else:
        plt.legend(label)


usa_douglas_archive(plot_douglas)

usa_kendrick_archive(plot_douglas)

usa_douglas(plot_douglas)

usa_kendrick(plot_douglas)
