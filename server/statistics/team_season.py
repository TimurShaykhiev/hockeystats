from collections import namedtuple

import numpy as np

from .games import get_team_home_away_stats
from . import FP_ARRAY_DATA_TYPE, fraction, percentage, stats_to_array, find_index, get_rate_and_avg,\
    get_indexes_max_results, get_indexes_min_results

'''
Numpy arrays contain stats for all teams only. These are the stats calculated in _calc_teams_stats and the ones
used for ratings calculation.
The extended stats are calculated for one team only. They are returned by _calc_team_ext_stats as well as ratings.
'''

# Integers values
COL_TEAM_ID = 0
COL_SEASON_ID = 1
COL_IS_REGULAR = 2
COL_GOALS_FOR = 3
COL_GOALS_AGAINST = 4
COL_SHOTS = 5
COL_PP_GOALS = 6
COL_PP_OPPORTUNITIES = 7
COL_SH_GOALS_AGAINST = 8
COL_SH_OPPORTUNITIES = 9
COL_FACE_OFF_WINS = 10
COL_FACE_OFF_TAKEN = 11
COL_BLOCKED = 12
COL_HITS = 13
COL_PENALTY_MINUTES = 14
COL_GAMES = 15
COL_WIN_REGULAR = 16
COL_WIN_OVERTIME = 17
COL_WIN_SHOOTOUT = 18
COL_LOSE_REGULAR = 19
COL_LOSE_OVERTIME = 20
COL_LOSE_SHOOTOUT = 21
COL_POINTS = 22
COL_GOALS_DIFF = 23
COL_RO_WINS = 24

TEAM_STATS_INT_ARRAY_LEN = 23

STANDINGS_STATS_INT_ARRAY_LEN = 25

# Floating-point values
COL_POINT_PERCENTAGE = 0
COL_PP_PERCENTAGE = 1
COL_PK_PERCENTAGE = 2
COL_GOAL_FOR_PER_GAME = 3
COL_GOAL_AGAINST_PER_GAME = 4
COL_SHOTS_PER_GAME = 5
COL_FACE_OFF_WIN_PERCENTAGE = 6

TEAM_STATS_FP_ARRAY_LEN = 7

COL_SHOOTING_PERCENTAGE = 7

TEAM_STATS_EXT_FP_ARRAY_LEN = 8

INT_ARRAY_RESULT_COLUMNS = [COL_TEAM_ID, COL_SEASON_ID, COL_IS_REGULAR, COL_GOALS_FOR, COL_GOALS_AGAINST, COL_GAMES,
                            COL_WIN_REGULAR, COL_WIN_OVERTIME, COL_WIN_SHOOTOUT, COL_LOSE_REGULAR, COL_LOSE_OVERTIME,
                            COL_LOSE_SHOOTOUT, COL_POINTS]

EXT_INT_ARRAY_RESULT_COLUMNS = [COL_GOALS_FOR, COL_GOALS_AGAINST, COL_PP_GOALS, COL_SH_GOALS_AGAINST, COL_POINTS]

STANDINGS_INT_ARRAY_RESULT_COLUMNS = [COL_TEAM_ID, COL_POINTS, COL_GAMES, COL_RO_WINS, COL_GOALS_DIFF]

StandingsStats = namedtuple('StandingsStats', ['tid', 'points', 'games', 'wins', 'diff', 'cid', 'did'])
TeamSeasonTopResult = namedtuple('TeamSeasonTopResult', ['type', 'tid', 'value'])


def get_teams_stats(team_stats):
    stat_arr_int = stats_to_array(team_stats, TEAM_STATS_INT_ARRAY_LEN)
    stat_arr_fp = np.zeros([len(team_stats), TEAM_STATS_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)

    _calc_teams_stats(stat_arr_int, stat_arr_fp)

    results = []
    for i in range(0, len(team_stats)):
        results.append(stat_arr_int[i, INT_ARRAY_RESULT_COLUMNS].tolist() + stat_arr_fp[i, :].tolist())
    return results


def get_teams_season_top_results(team_stats):
    col_ppp = 0
    col_pkp = 1
    arr_int = stats_to_array(team_stats, TEAM_STATS_INT_ARRAY_LEN)
    arr_fp = np.zeros([len(team_stats), 2], dtype=FP_ARRAY_DATA_TYPE)
    _set_team_points(arr_int)

    arr_fp[:, col_ppp] = percentage(arr_int[:, COL_PP_GOALS], arr_int[:, COL_PP_OPPORTUNITIES])
    arr_fp[:, col_pkp] = 100 - percentage(arr_int[:, COL_SH_GOALS_AGAINST], arr_int[:, COL_SH_OPPORTUNITIES])

    result = \
        _get_results_for_int_column(arr_int, COL_POINTS, 'points') +\
        _get_results_for_int_column(arr_int, COL_GOALS_FOR, 'goals') +\
        _get_results_for_int_column(arr_int, COL_GOALS_AGAINST, 'goalsAgainst') +\
        _get_results_for_fp_column(arr_fp, arr_int, col_ppp, 'ppp') +\
        _get_results_for_fp_column(arr_fp, arr_int, col_pkp, 'pkp')

    return result


def get_team_ext_stats(team_id, team_stats, games):
    stat_arr_int = stats_to_array(team_stats, TEAM_STATS_INT_ARRAY_LEN)
    stat_arr_fp = np.zeros([len(team_stats), TEAM_STATS_EXT_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)
    team_row_idx = find_index(stat_arr_int[:, COL_TEAM_ID], team_id)

    _calc_teams_stats(stat_arr_int, stat_arr_fp)
    home_away_stats = get_team_home_away_stats(team_id, games)
    ext_stats, ratings = _calc_team_ext_stats(stat_arr_int, stat_arr_fp, team_row_idx, home_away_stats)

    results = stat_arr_int[team_row_idx, EXT_INT_ARRAY_RESULT_COLUMNS].tolist() +\
        stat_arr_fp[team_row_idx, :].tolist() +\
        ext_stats + ratings
    return results


def get_standings_stats(team_stats, team_info):
    arr = stats_to_array(team_stats, STANDINGS_STATS_INT_ARRAY_LEN)

    _set_team_points(arr)
    arr[:, COL_RO_WINS] = arr[:, COL_WIN_REGULAR] + arr[:, COL_WIN_OVERTIME]
    arr[:, COL_GOALS_DIFF] = arr[:, COL_GOALS_FOR] - arr[:, COL_GOALS_AGAINST]

    results = []
    for i in range(0, len(team_stats)):
        stats = arr[i, STANDINGS_INT_ARRAY_RESULT_COLUMNS].tolist() + team_info[arr[i, COL_TEAM_ID]]
        results.append(StandingsStats._make(stats))
    return results


def _calc_teams_stats(arr_int, arr_fp):
    _set_team_points(arr_int)

    arr_fp[:, COL_POINT_PERCENTAGE] = percentage(arr_int[:, COL_POINTS], arr_int[:, COL_GAMES] * 2)
    arr_fp[:, COL_PP_PERCENTAGE] = percentage(arr_int[:, COL_PP_GOALS], arr_int[:, COL_PP_OPPORTUNITIES])
    arr_fp[:, COL_PK_PERCENTAGE] = 100 - percentage(arr_int[:, COL_SH_GOALS_AGAINST], arr_int[:, COL_SH_OPPORTUNITIES])
    arr_fp[:, COL_GOAL_FOR_PER_GAME] = fraction(arr_int[:, COL_GOALS_FOR], arr_int[:, COL_GAMES])
    arr_fp[:, COL_GOAL_AGAINST_PER_GAME] = fraction(arr_int[:, COL_GOALS_AGAINST], arr_int[:, COL_GAMES])
    arr_fp[:, COL_SHOTS_PER_GAME] = fraction(arr_int[:, COL_SHOTS], arr_int[:, COL_GAMES])
    arr_fp[:, COL_FACE_OFF_WIN_PERCENTAGE] = \
        percentage(arr_int[:, COL_FACE_OFF_WINS], arr_int[:, COL_FACE_OFF_TAKEN])


def _calc_team_ext_stats(arr_int, arr_fp, team_row_idx, ha_stats):
    arr_fp[:, COL_SHOOTING_PERCENTAGE] = percentage(arr_int[:, COL_GOALS_FOR], arr_int[:, COL_SHOTS])

    row = arr_int[team_row_idx, :]
    shots_against = ha_stats.home_sa + ha_stats.away_sa
    ext_stats = [
        fraction(shots_against, row[COL_GAMES]),  # shots against per game
        fraction(shots_against, row[COL_GOALS_AGAINST]),  # shots against per goal
        percentage(row[COL_GOALS_AGAINST], shots_against),  # opponent shooting percentage
        fraction(row[COL_GOALS_FOR], row[COL_GOALS_AGAINST]),  # scoring efficiency ratio
        fraction(row[COL_SHOTS], shots_against),  # shot efficiency ratio
        fraction(ha_stats.home_opp_pim + ha_stats.away_opp_pim, row[COL_PENALTY_MINUTES]),  # penalty efficiency ratio
        fraction(row[COL_POINTS], row[COL_GAMES]),  # points per game
        fraction(row[COL_PP_GOALS], row[COL_GAMES]),  # PP goals per game
        fraction(row[COL_SH_GOALS_AGAINST], row[COL_GAMES]),  # SH goals against per game
        fraction(row[COL_PP_OPPORTUNITIES], row[COL_GAMES]),  # PP per game
        fraction(row[COL_SH_OPPORTUNITIES], row[COL_GAMES]),  # SH per game
        fraction(shots_against - row[COL_GOALS_AGAINST], shots_against),  # save percentage
        fraction(row[COL_SHOTS] - row[COL_GOALS_FOR], row[COL_SHOTS]),  # opponent save percentage
        ha_stats.home_shutouts + ha_stats.away_shutouts,  # shutouts
        ha_stats.home_opp_shutouts + ha_stats.away_opp_shutouts,  # opponent shutouts
        # shootout winning %
        percentage(row[COL_WIN_SHOOTOUT], row[COL_WIN_SHOOTOUT] + row[COL_LOSE_SHOOTOUT]),
        ha_stats.home_goals,
        ha_stats.away_goals,
        ha_stats.home_ga,
        ha_stats.away_ga,
        ha_stats.home_shots,
        ha_stats.away_shots,
        ha_stats.home_sa,
        ha_stats.away_sa,
        percentage(ha_stats.home_pp_goals, ha_stats.home_pp_opp),  # home PP percentage
        percentage(ha_stats.away_pp_goals, ha_stats.away_pp_opp),  # away PP percentage
        100 - percentage(ha_stats.home_sh_goals, ha_stats.home_sh_opp),  # home PK percentage
        100 - percentage(ha_stats.away_sh_goals, ha_stats.away_sh_opp),  # away PK percentage
        ha_stats.home_win_percentage,
        ha_stats.away_win_percentage
    ]

    ratings = []
    ratings.extend(get_rate_and_avg(arr_fp, COL_PP_PERCENTAGE, team_row_idx))
    ratings.extend(get_rate_and_avg(arr_fp, COL_PK_PERCENTAGE, team_row_idx))
    ratings.extend(get_rate_and_avg(arr_fp, COL_GOAL_FOR_PER_GAME, team_row_idx))
    ratings.extend(get_rate_and_avg(arr_fp, COL_GOAL_AGAINST_PER_GAME, team_row_idx, False))
    ratings.extend(get_rate_and_avg(arr_fp, COL_FACE_OFF_WIN_PERCENTAGE, team_row_idx))
    ratings.extend(get_rate_and_avg(arr_fp, COL_SHOOTING_PERCENTAGE, team_row_idx))
    return ext_stats, ratings


def _set_team_points(arr):
    if arr[0, COL_IS_REGULAR] == 1:
        arr[:, COL_POINTS] = (arr[:, COL_WIN_REGULAR] + arr[:, COL_WIN_OVERTIME] + arr[:, COL_WIN_SHOOTOUT]) * 2 + \
                             arr[:, COL_LOSE_OVERTIME] + arr[:, COL_LOSE_SHOOTOUT]


def _get_top_results_from_int(arr, indexes, column, res_type):
    return [TeamSeasonTopResult(res_type, s[COL_TEAM_ID], s[column]) for s in arr[indexes, :]]


def _get_top_results_from_fp(arr_fp, arr_int, indexes, column, res_type):
    return [TeamSeasonTopResult(res_type, arr_int[i, COL_TEAM_ID], arr_fp[i, column]) for i in indexes]


def _get_results_for_int_column(arr, column, res_type):
    res_idx = get_indexes_max_results(arr, column)
    max_res = _get_top_results_from_int(arr, res_idx, column, res_type)
    res_idx = get_indexes_min_results(arr, column)
    min_res = _get_top_results_from_int(arr, res_idx, column, res_type + 'Min')
    return max_res + min_res


def _get_results_for_fp_column(arr_fp, arr_int, column, res_type):
    res_idx = get_indexes_max_results(arr_fp, column)
    max_res = _get_top_results_from_fp(arr_fp, arr_int, res_idx, column, res_type)
    res_idx = get_indexes_min_results(arr_fp, column)
    min_res = _get_top_results_from_fp(arr_fp, arr_int, res_idx, column, res_type + 'Min')
    return max_res + min_res
