import numpy as np

from . import FP_ARRAY_DATA_TYPE, fraction, percentage, stats_to_array, find_index, find_rate

'''
Numpy arrays contain stats for all skaters only. These are the stats calculated in _calc_skaters_stats and the ones
used for ratings calculation.
The extended stats are calculated for one skater only. They are returned by _calc_skater_ext_stats as well as ratings.
'''

# Integers values
COL_PLAYER_ID = 0
COL_ASSISTS = 1
COL_GOALS = 2
COL_SHOTS = 3
COL_HITS = 4
COL_PP_GOALS = 5
COL_PP_ASSISTS = 6
COL_PENALTY_MINUTES = 7
COL_FACE_OFF_WINS = 8
COL_FACE_OFF_TAKEN = 9
COL_TAKEAWAYS = 10
COL_GIVEAWAYS = 11
COL_SH_GOALS = 12
COL_SH_ASSISTS = 13
COL_BLOCKED = 14
COL_PLUS_MINUS = 15
COL_TOI = 16
COL_EVEN_TOI = 17
COL_PP_TOI = 18
COL_SH_TOI = 19
COL_GAMES = 20
COL_POINTS = 21
COL_PP_POINTS = 22
COL_SH_POINTS = 23

SKATER_STATS_INT_ARRAY_LEN = 24

COL_TURNOVER = 24

SKATER_STATS_EXT_INT_ARRAY_LEN = 25

# Floating-point values
COL_POINTS_PER_GAME = 0
COL_TOI_PER_GAME = 1
COL_SHOOTING_PERCENTAGE = 2
COL_FACE_OFF_WIN_PERCENTAGE = 3

SKATER_STATS_FP_ARRAY_LEN = 4

INT_ARRAY_RESULT_COLUMNS = [COL_PLAYER_ID, COL_ASSISTS, COL_GOALS, COL_SHOTS, COL_PP_GOALS, COL_PENALTY_MINUTES,
                            COL_SH_GOALS, COL_PLUS_MINUS, COL_GAMES, COL_POINTS, COL_PP_POINTS, COL_SH_POINTS]

EXT_INT_ARRAY_RESULT_COLUMNS = [COL_ASSISTS, COL_GOALS, COL_SHOTS, COL_HITS, COL_PENALTY_MINUTES, COL_TAKEAWAYS,
                                COL_GIVEAWAYS, COL_BLOCKED, COL_PLUS_MINUS, COL_POINTS, COL_PP_POINTS, COL_SH_POINTS,
                                COL_TURNOVER]


def get_skaters_stats(skater_stats):
    stat_arr_int = stats_to_array(skater_stats, SKATER_STATS_INT_ARRAY_LEN)
    stat_arr_fp = np.zeros([len(skater_stats), SKATER_STATS_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)

    _calc_skaters_stats(stat_arr_int, stat_arr_fp)

    results = []
    for i in range(0, len(skater_stats)):
        results.append(stat_arr_int[i, INT_ARRAY_RESULT_COLUMNS].tolist() + stat_arr_fp[i, :].tolist())
    return results


def get_skater_ext_stats(player_id, skater_stats, team_player_list):
    stat_arr_int = stats_to_array(skater_stats, SKATER_STATS_EXT_INT_ARRAY_LEN)
    stat_arr_fp = np.zeros([len(skater_stats), SKATER_STATS_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)
    skater_row_idx = find_index(stat_arr_int[:, COL_PLAYER_ID], player_id)

    _calc_skaters_stats(stat_arr_int, stat_arr_fp)
    ext_stats, ratings = _calc_skater_ext_stats(stat_arr_int, skater_row_idx)
    team_ratings = _calc_team_ratings(stat_arr_int, player_id, team_player_list)

    results = stat_arr_int[skater_row_idx, EXT_INT_ARRAY_RESULT_COLUMNS].tolist() +\
        stat_arr_fp[skater_row_idx, :].tolist() +\
        ext_stats + ratings + team_ratings
    return results


def _calc_skaters_stats(arr_int, arr_fp):
    arr_int[:, COL_POINTS] = arr_int[:, COL_GOALS] + arr_int[:, COL_ASSISTS]
    arr_int[:, COL_PP_POINTS] = arr_int[:, COL_PP_GOALS] + arr_int[:, COL_PP_ASSISTS]
    arr_int[:, COL_SH_POINTS] = arr_int[:, COL_SH_GOALS] + arr_int[:, COL_SH_ASSISTS]

    arr_fp[:, COL_POINTS_PER_GAME] = fraction(arr_int[:, COL_POINTS], arr_int[:, COL_GAMES])
    arr_fp[:, COL_TOI_PER_GAME] = fraction(arr_int[:, COL_TOI], arr_int[:, COL_GAMES])
    arr_fp[:, COL_SHOOTING_PERCENTAGE] = percentage(arr_int[:, COL_GOALS], arr_int[:, COL_SHOTS])
    arr_fp[:, COL_FACE_OFF_WIN_PERCENTAGE] = \
        percentage(arr_int[:, COL_FACE_OFF_WINS], arr_int[:, COL_FACE_OFF_TAKEN])


def _calc_skater_ext_stats(arr_int, skater_row_idx):
    arr_int[:, COL_TURNOVER] = arr_int[:, COL_TAKEAWAYS] - arr_int[:, COL_GIVEAWAYS]

    row = arr_int[skater_row_idx, :]
    ext_stats = [
        _calc_60_min_stat(row, COL_POINTS),  # points per 60 min
        percentage(row[COL_GOALS], row[COL_POINTS]),  # goal percentage of points
        percentage(row[COL_ASSISTS], row[COL_POINTS]),  # assist percentage of points
        fraction(row[COL_GOALS], row[COL_GAMES]),  # goals per game
        _calc_60_min_stat(row, COL_GOALS),  # goals per 60 min
        percentage(row[COL_GOALS] - row[COL_PP_GOALS] - row[COL_SH_GOALS], row[COL_GOALS]),  # even strength goal %
        percentage(row[COL_PP_GOALS], row[COL_GOALS]),  # PP goal percentage
        fraction(row[COL_ASSISTS], row[COL_GAMES]),  # assists per game
        _calc_60_min_stat(row, COL_ASSISTS),  # assists per 60 min
        percentage(row[COL_ASSISTS] - row[COL_PP_ASSISTS] - row[COL_SH_ASSISTS], row[COL_ASSISTS]),  # even assist %
        percentage(row[COL_PP_ASSISTS], row[COL_ASSISTS]),  # PP assist percentage
        fraction(row[COL_SHOTS], row[COL_GAMES]),  # shots per game
        _calc_60_min_stat(row, COL_SHOTS),  # shots per 60 min
        fraction(row[COL_SHOTS], row[COL_GOALS]),  # shots per goal
        _calc_60_min_stat(row, COL_TURNOVER),  # turnover per 60 min
        fraction(row[COL_TAKEAWAYS], row[COL_GIVEAWAYS]),  # turnover ratio
        _calc_60_min_stat(row, COL_BLOCKED),  # blocks per 60 min
        _calc_60_min_stat(row, COL_HITS),  # hits per 60 min
        _calc_60_min_stat(row, COL_PENALTY_MINUTES)  # PIMs per 60 min
    ]

    ratings = [
        find_rate(skater_row_idx, arr_int[:, COL_GOALS]),
        find_rate(skater_row_idx, arr_int[:, COL_ASSISTS]),
        find_rate(skater_row_idx, arr_int[:, COL_POINTS]),
        find_rate(skater_row_idx, arr_int[:, COL_PLUS_MINUS]),
        find_rate(skater_row_idx, arr_int[:, COL_TURNOVER])
    ]
    return ext_stats, ratings


def _calc_team_ratings(arr_int, player_id, team_player_list):
    # filter array to get stats for players from team only
    team_pl_arr = arr_int[np.isin(arr_int[:, COL_PLAYER_ID], team_player_list)]

    skater_row_idx = find_index(team_pl_arr[:, COL_PLAYER_ID], player_id)
    ratings = [
        find_rate(skater_row_idx, team_pl_arr[:, COL_GOALS]),
        find_rate(skater_row_idx, team_pl_arr[:, COL_ASSISTS]),
        find_rate(skater_row_idx, team_pl_arr[:, COL_POINTS]),
        find_rate(skater_row_idx, team_pl_arr[:, COL_PLUS_MINUS]),
        find_rate(skater_row_idx, team_pl_arr[:, COL_TURNOVER])
    ]
    return ratings


def _calc_60_min_stat(row, column):
    return fraction(row[column], row[COL_TOI] / 3600)