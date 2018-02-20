import numpy as np

from .goalie_stats import get_goalie_home_away_stats
from . import FP_ARRAY_DATA_TYPE, fraction, percentage, stats_to_array, find_index, find_rate, find_rate2

'''
Numpy arrays contain stats for all goalies only. These are the stats calculated in _calc_goalies_stats and the ones
used for ratings calculation.
The extended stats are calculated for one goalie only. They are returned by _calc_goalie_ext_stats as well as ratings.
'''

# Integers values
COL_PLAYER_ID = 0
COL_SEASON_ID = 1
COL_IS_REGULAR = 2
COL_TOI = 3
COL_ASSISTS = 4
COL_GOALS = 5
COL_PENALTY_MINUTES = 6
COL_SHOTS = 7
COL_SAVES = 8
COL_PP_SAVES = 9
COL_SH_SAVES = 10
COL_EVEN_SAVES = 11
COL_SH_SHOTS_AGAINST = 12
COL_EVEN_SHOTS_AGAINST = 13
COL_PP_SHOTS_AGAINST = 14
COL_GAMES = 15
COL_WINS = 16
COL_SHUTOUT = 17
COL_POINTS = 18
COL_LOSSES = 19
COL_GOALS_AGAINST = 20

GOALIE_STATS_INT_ARRAY_LEN = 21

# Floating-point values
COL_GOALS_AGAINST_AVERAGE = 0
COL_SAVE_PERCENTAGE = 1

GOALIE_STATS_FP_ARRAY_LEN = 2

COL_WIN_PERCENTAGE = 2

GOALIE_STATS_EXT_FP_ARRAY_LEN = 3

INT_ARRAY_RESULT_COLUMNS = [COL_PLAYER_ID, COL_SEASON_ID, COL_IS_REGULAR, COL_TOI, COL_ASSISTS, COL_GOALS,
                            COL_PENALTY_MINUTES, COL_SHOTS, COL_SAVES, COL_GAMES, COL_WINS, COL_SHUTOUT, COL_POINTS,
                            COL_LOSSES, COL_GOALS_AGAINST]

EXT_INT_ARRAY_RESULT_COLUMNS = [COL_SAVES, COL_WINS, COL_SHUTOUT, COL_GOALS_AGAINST]


def get_goalies_stats(goalie_stats):
    stat_arr_int = stats_to_array(goalie_stats, GOALIE_STATS_INT_ARRAY_LEN)
    stat_arr_fp = np.zeros([len(goalie_stats), GOALIE_STATS_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)

    _calc_goalies_stats(stat_arr_int, stat_arr_fp)

    results = []
    for i in range(0, len(goalie_stats)):
        results.append(stat_arr_int[i, INT_ARRAY_RESULT_COLUMNS].tolist() + stat_arr_fp[i, :].tolist())
    return results


def get_goalie_ext_stats(player_id, goalie_sum_stats, goalie_stats, games):
    stat_arr_int = stats_to_array(goalie_sum_stats, GOALIE_STATS_INT_ARRAY_LEN)
    stat_arr_fp = np.zeros([len(goalie_sum_stats), GOALIE_STATS_EXT_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)
    goalie_row_idx = find_index(stat_arr_int[:, COL_PLAYER_ID], player_id)

    _calc_goalies_stats(stat_arr_int, stat_arr_fp)
    ha_stats = get_goalie_home_away_stats(goalie_stats, games)
    ext_stats, ratings = _calc_goalie_ext_stats(stat_arr_int, stat_arr_fp, goalie_row_idx, ha_stats)

    results = stat_arr_int[goalie_row_idx, EXT_INT_ARRAY_RESULT_COLUMNS].tolist() +\
        stat_arr_fp[goalie_row_idx, :].tolist() +\
        ext_stats + ratings
    return results


def _calc_goalies_stats(arr_int, arr_fp):
    arr_int[:, COL_POINTS] = arr_int[:, COL_GOALS] + arr_int[:, COL_ASSISTS]
    arr_int[:, COL_LOSSES] = arr_int[:, COL_GAMES] - arr_int[:, COL_WINS]
    arr_int[:, COL_GOALS_AGAINST] = arr_int[:, COL_SHOTS] - arr_int[:, COL_SAVES]

    arr_fp[:, COL_GOALS_AGAINST_AVERAGE] = _goals_against_average(arr_int)
    arr_fp[:, COL_SAVE_PERCENTAGE] = fraction(arr_int[:, COL_SAVES], arr_int[:, COL_SHOTS])


def _calc_goalie_ext_stats(arr_int, arr_fp, goalie_row_idx, ha_stats):
    arr_fp[:, COL_WIN_PERCENTAGE] = percentage(arr_int[:, COL_WINS], arr_int[:, COL_GAMES])

    row = arr_int[goalie_row_idx, :]
    even_ga = row[COL_EVEN_SHOTS_AGAINST] - row[COL_EVEN_SAVES]
    ext_stats = [
        even_ga,  # even strength goals against
        row[COL_PP_SHOTS_AGAINST] - row[COL_PP_SAVES],  # PP goals against
        row[COL_SH_SHOTS_AGAINST] - row[COL_SH_SAVES],  # SH goals against
        fraction(row[COL_SAVES], row[COL_GAMES]),  # saves per game
        fraction(row[COL_SHOTS], row[COL_GOALS_AGAINST]),  # shots against per goal
        percentage(even_ga, row[COL_GOALS_AGAINST]),  # even strength goals against percentage
        ha_stats.home_gaa,
        ha_stats.away_gaa,
        ha_stats.home_svp,
        ha_stats.away_svp,
        ha_stats.home_win_percentage,
        ha_stats.away_win_percentage,
        ha_stats.home_wins,
        ha_stats.away_wins
    ]

    ratings = [
        find_rate2(goalie_row_idx, arr_fp[:, COL_GOALS_AGAINST_AVERAGE], arr_int[:, COL_GAMES], False),
        find_rate2(goalie_row_idx, arr_fp[:, COL_SAVE_PERCENTAGE], arr_int[:, COL_GAMES]),
        find_rate2(goalie_row_idx, arr_fp[:, COL_WIN_PERCENTAGE], arr_int[:, COL_GAMES]),
        find_rate(goalie_row_idx, arr_int[:, COL_WINS]),
        find_rate(goalie_row_idx, arr_int[:, COL_SHUTOUT])
    ]
    return ext_stats, ratings


def _goals_against_average(arr):
    return fraction(arr[:, COL_GOALS_AGAINST] * 60, np.round(arr[:, COL_TOI] / 60))
