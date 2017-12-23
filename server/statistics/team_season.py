import numpy as np

from .games import get_team_home_away_stats
from . import FP_ARRAY_DATA_TYPE, fraction, percentage, stats_to_array, find_index, find_rate

'''
Numpy arrays contain stats for all teams only. These are the stats calculated in _calc_teams_stats and the ones
used for ratings calculation.
The extended stats are calculated for one team only. They are returned by _calc_team_ext_stats as well as ratings.
'''

# Integers values
COL_TEAM_ID = 0
COL_GOALS_FOR = 1
COL_GOALS_AGAINST = 2
COL_SHOTS = 3
COL_PP_GOALS = 4
COL_PP_OPPORTUNITIES = 5
COL_SH_GOALS_AGAINST = 6
COL_SH_OPPORTUNITIES = 7
COL_FACE_OFF_WINS = 8
COL_FACE_OFF_TAKEN = 9
COL_BLOCKED = 10
COL_HITS = 11
COL_PENALTY_MINUTES = 12
COL_GAMES = 13
COL_WIN_REGULAR = 14
COL_WIN_OVERTIME = 15
COL_WIN_SHOOTOUT = 16
COL_LOSE_REGULAR = 17
COL_LOSE_OVERTIME = 18
COL_LOSE_SHOOTOUT = 19
COL_POINTS = 20

TEAM_STATS_INT_ARRAY_LEN = 21

# Floating-point values
COL_POINT_PERCENTAGE = 0
COL_PP_PERCENTAGE = 1
COL_PK_PERCENTAGE = 2
COL_GOAL_FOR_PER_GAME = 3
COL_GOAL_AGAINST_PER_GAME = 4
COL_GOAL_FACE_OFF_WIN_PERCENTAGE = 5

TEAM_STATS_FP_ARRAY_LEN = 6

COL_SHOOTING_PERCENTAGE = 6

TEAM_STATS_EXT_FP_ARRAY_LEN = 7

INT_ARRAY_RESULT_COLUMNS =\
    list(range(COL_TEAM_ID, COL_FACE_OFF_WINS)) + list(range(COL_PENALTY_MINUTES, TEAM_STATS_INT_ARRAY_LEN))

EXT_INT_ARRAY_RESULT_COLUMNS =\
    list(range(COL_GOALS_FOR, COL_FACE_OFF_WINS)) + list(range(COL_PENALTY_MINUTES, TEAM_STATS_INT_ARRAY_LEN))


def get_teams_stats(team_stats):
    stat_arr_int = stats_to_array(team_stats, TEAM_STATS_INT_ARRAY_LEN)
    stat_arr_fp = np.zeros([len(team_stats), TEAM_STATS_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)

    _calc_teams_stats(stat_arr_int, stat_arr_fp)

    results = []
    for i in range(0, len(team_stats)):
        results.append(stat_arr_int[i, INT_ARRAY_RESULT_COLUMNS].tolist() + stat_arr_fp[i, :].tolist())
    return results


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


def _calc_teams_stats(arr_int, arr_fp):
    arr_int[:, COL_POINTS] = team_points(arr_int)

    arr_fp[:, COL_POINT_PERCENTAGE] = percentage(arr_int[:, COL_POINTS], arr_int[:, COL_GAMES] * 2)
    arr_fp[:, COL_PP_PERCENTAGE] = percentage(arr_int[:, COL_PP_GOALS], arr_int[:, COL_PP_OPPORTUNITIES])
    arr_fp[:, COL_PK_PERCENTAGE] = 100 - percentage(arr_int[:, COL_SH_GOALS_AGAINST], arr_int[:, COL_SH_OPPORTUNITIES])
    arr_fp[:, COL_GOAL_FOR_PER_GAME] = fraction(arr_int[:, COL_GOALS_FOR], arr_int[:, COL_GAMES])
    arr_fp[:, COL_GOAL_AGAINST_PER_GAME] = fraction(arr_int[:, COL_GOALS_AGAINST], arr_int[:, COL_GAMES])
    arr_fp[:, COL_GOAL_FACE_OFF_WIN_PERCENTAGE] = \
        percentage(arr_int[:, COL_FACE_OFF_WINS], arr_int[:, COL_FACE_OFF_TAKEN])


def _calc_team_ext_stats(arr_int, arr_fp, team_row_idx, ha_stats):
    arr_fp[:, COL_SHOOTING_PERCENTAGE] = percentage(arr_int[:, COL_GOALS_FOR], arr_int[:, COL_SHOTS])

    row = arr_int[team_row_idx, :]
    shots_against = ha_stats.home_sa + ha_stats.away_sa
    ext_stats = [
        shots_against,  # shots against
        fraction(shots_against, row[COL_GAMES]),  # shots against per game
        fraction(row[COL_SHOTS], row[COL_GAMES]),  # shots per game
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
    ]

    ratings = []
    ratings.extend(_get_rate_and_avg(arr_fp, COL_PP_PERCENTAGE, team_row_idx))
    ratings.extend(_get_rate_and_avg(arr_fp, COL_PK_PERCENTAGE, team_row_idx))
    ratings.extend(_get_rate_and_avg(arr_fp, COL_GOAL_FOR_PER_GAME, team_row_idx))
    ratings.extend(_get_rate_and_avg(arr_fp, COL_GOAL_AGAINST_PER_GAME, team_row_idx, False))
    ratings.extend(_get_rate_and_avg(arr_fp, COL_GOAL_FACE_OFF_WIN_PERCENTAGE, team_row_idx))
    ratings.extend(_get_rate_and_avg(arr_fp, COL_SHOOTING_PERCENTAGE, team_row_idx))
    return ext_stats, ratings


def _get_rate_and_avg(arr, column, team_row_idx, desc_order=True):
    col = arr[:, column]
    return find_rate(team_row_idx, col, desc_order), col.mean()


def team_points(arr):
    return (arr[:, COL_WIN_REGULAR] + arr[:, COL_WIN_OVERTIME] + arr[:, COL_WIN_SHOOTOUT]) * 2 + \
           arr[:, COL_LOSE_OVERTIME] + arr[:, COL_LOSE_SHOOTOUT]
