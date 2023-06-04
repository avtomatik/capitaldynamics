SERIES_IDS = {
    # =====================================================================
    # Nominal Investment Series: A006RC, 1929--2021
    # =====================================================================
    'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =====================================================================
    # Nominal Gross Domestic Product Series: A191RC, 1929--2021
    # =====================================================================
    'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =====================================================================
    # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
    # =====================================================================
    'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =====================================================================
    # Fixed Assets Series: k1n31gd1es00, 1925--2020
    # =====================================================================
    'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
}


DATA_CAPITAL_ACQUISITIONS = {
    'option_1': {
        'Define Number of Line Segments for Pi': 1,
        'Number of Spans Provided': 1,
        'Define Pi for Period from 1968 to 2010': 0
    },
    'option_2': {
        'Define Number of Line Segments for Pi': 1,
        'Number of Spans Provided': 1,
        'Define Pi for Period from 1968 to 2010': 1
    },
    'option_3': {
        'Define Number of Line Segments for Pi': 2,
        'Number of Spans Provided': 2,
        'Define Pi for Period from 1968 to 1981': 1,
        'Define Pi for Period from 1982 to 2010': 0
    },
    'option_4': {
        'Define Number of Line Segments for Pi': 4,
        'Number of Spans Provided': 4,
        'Define Pi for Period from 1968 to 1981': 1,
        'Define Pi for Period from 1982 to 1991': 0.537711622818944,
        'Define Pi for Period from 1992 to 2001': 0.815869779361117,
        'Define Pi for Period from 2002 to 2010': 0.956084835528969
    }
}


DATA_CAPITAL_RETIREMENT = {
    'option_1': {
        'Define Number of Line Segments for Pi': 1,
        'Number of Spans Provided': 1,
        'Define Pi for Period from 1951 to 2011': 0
    },
    'option_2': {
        'Define Number of Line Segments for Pi': 2,
        'Number of Spans Provided': 2,
        'Select Row for Year': 52,
        'Define Pi for Period from 1951 to 2003': 1,
        'Define Pi for Period from 2003 to 2011': 1.4
    },
    'option_3': {
        'Define Number of Line Segments for Pi': 2,
        'Number of Spans Provided': 2,
        'Select Row for Year': 11,
        'Define Pi for Period from 1951 to 1962': 0.0493299706940006,
        'Define Pi for Period from 1962 to 2011': 0.0168837249983057
    }
}
