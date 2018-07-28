from collections import namedtuple

import numpy as np

from .skater_stats import get_skater_home_away_stats
from . import FP_ARRAY_DATA_TYPE, SeasonTopResult, fraction, percentage, stats_to_array, find_index, find_rate,\
    get_indexes_max_results, get_indexes_min_results

'''
Numpy arrays contain stats for all skaters only. These are the stats calculated in _calc_skaters_stats and the ones
used for ratings calculation.
The extended stats are calculated for one skater only. They are returned by _calc_skater_ext_stats as well as ratings.
'''

# Integers values
COL_PLAYER_ID = 0
COL_SEASON_ID = 1
COL_IS_REGULAR = 2
COL_ASSISTS = 3
COL_GOALS = 4
COL_SHOTS = 5
COL_HITS = 6
COL_PP_GOALS = 7
COL_PP_ASSISTS = 8
COL_PENALTY_MINUTES = 9
COL_FACE_OFF_WINS = 10
COL_FACE_OFF_TAKEN = 11
COL_TAKEAWAYS = 12
COL_GIVEAWAYS = 13
COL_SH_GOALS = 14
COL_SH_ASSISTS = 15
COL_BLOCKED = 16
COL_PLUS_MINUS = 17
COL_TOI = 18
COL_EVEN_TOI = 19
COL_PP_TOI = 20
COL_SH_TOI = 21
COL_GAMES = 22
COL_POINTS = 23
COL_PP_POINTS = 24
COL_SH_POINTS = 25

SKATER_STATS_INT_ARRAY_LEN = 26

COL_TURNOVER = 26
COL_PIM_FILTERED = 27

SKATER_STATS_EXT_INT_ARRAY_LEN = 28

# Floating-point values
COL_POINTS_PER_GAME = 0
COL_TOI_PER_GAME = 1
COL_SHOOTING_PERCENTAGE = 2
COL_FACE_OFF_WIN_PERCENTAGE = 3

SKATER_STATS_FP_ARRAY_LEN = 4

COL_HITS_PER_GAME = 4
COL_BLOCKS_PER_GAME = 5
COL_TAKEAWAYS_PER_GAME = 6
COL_GIVEAWAYS_PER_GAME = 7
COL_PP_TOI_PER_GAME = 8
COL_SH_TOI_PER_GAME = 9

SEASON_STATS_FP_ARRAY_LEN = 10

INT_ARRAY_RESULT_COLUMNS = [COL_PLAYER_ID, COL_SEASON_ID, COL_IS_REGULAR, COL_ASSISTS, COL_GOALS, COL_SHOTS,
                            COL_PP_GOALS, COL_PENALTY_MINUTES, COL_SH_GOALS, COL_PLUS_MINUS, COL_GAMES, COL_POINTS,
                            COL_PP_POINTS, COL_SH_POINTS, COL_FACE_OFF_TAKEN]

EXT_INT_ARRAY_RESULT_COLUMNS = [COL_ASSISTS, COL_GOALS, COL_SHOTS, COL_HITS, COL_PENALTY_MINUTES, COL_TAKEAWAYS,
                                COL_GIVEAWAYS, COL_BLOCKED, COL_PLUS_MINUS, COL_POINTS, COL_PP_POINTS, COL_SH_POINTS,
                                COL_TURNOVER]

FP_ARRAY_RESULT_COLUMNS = [COL_POINTS_PER_GAME, COL_TOI_PER_GAME, COL_SHOOTING_PERCENTAGE, COL_FACE_OFF_WIN_PERCENTAGE]


def get_skaters_stats(skater_stats):
    stat_arr_int = stats_to_array(skater_stats, SKATER_STATS_INT_ARRAY_LEN)
    stat_arr_fp = np.zeros([len(skater_stats), SKATER_STATS_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)

    _calc_skaters_stats(stat_arr_int, stat_arr_fp)

    results = []
    for i in range(0, len(skater_stats)):
        results.append(stat_arr_int[i, INT_ARRAY_RESULT_COLUMNS].tolist() +
                       stat_arr_fp[i, FP_ARRAY_RESULT_COLUMNS].tolist())
    return results


def get_skater_ext_stats(player_id, skater_sum_stats, team_player_list, home_stats, away_stats):
    stat_arr_int = stats_to_array(skater_sum_stats, SKATER_STATS_EXT_INT_ARRAY_LEN)
    stat_arr_fp = np.zeros([len(skater_sum_stats), SKATER_STATS_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)
    skater_row_idx = find_index(stat_arr_int[:, COL_PLAYER_ID], player_id)

    _calc_skaters_stats(stat_arr_int, stat_arr_fp)
    ha_stats = get_skater_home_away_stats(home_stats, away_stats)
    ext_stats, ratings = _calc_skater_ext_stats(stat_arr_int, skater_row_idx, ha_stats)
    team_ratings = _calc_team_ratings(stat_arr_int, player_id, team_player_list)

    results = stat_arr_int[skater_row_idx, EXT_INT_ARRAY_RESULT_COLUMNS].tolist() +\
        stat_arr_fp[skater_row_idx, FP_ARRAY_RESULT_COLUMNS].tolist() +\
        ext_stats + ratings + team_ratings
    return results


def get_skaters_season_top_results(fwd_stats, def_stats):
    fwd_arr_int = stats_to_array(fwd_stats, SKATER_STATS_EXT_INT_ARRAY_LEN)
    fwd_arr_fp = np.zeros([len(fwd_stats), SEASON_STATS_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)
    def_arr_int = stats_to_array(def_stats, SKATER_STATS_EXT_INT_ARRAY_LEN)
    def_arr_fp = np.zeros([len(def_stats), SEASON_STATS_FP_ARRAY_LEN], dtype=FP_ARRAY_DATA_TYPE)
    _calc_season_stats(fwd_arr_int, fwd_arr_fp, False)
    _calc_season_stats(def_arr_int, def_arr_fp, True)

    result = \
        _get_max_results_for_int_column(fwd_arr_int, def_arr_int, COL_GOALS, _get_res_types('goals')) +\
        _get_max_results_for_int_column(fwd_arr_int, def_arr_int, COL_ASSISTS, _get_res_types('assists')) +\
        _get_max_results_for_int_column(fwd_arr_int, def_arr_int, COL_POINTS, _get_res_types('points')) +\
        _get_max_results_for_int_column(fwd_arr_int, def_arr_int, COL_PP_GOALS, _get_res_types('ppGoals')) +\
        _get_max_results_for_int_column(fwd_arr_int, def_arr_int, COL_PP_POINTS, _get_res_types('ppPoints')) +\
        _get_max_results_for_int_column(fwd_arr_int, def_arr_int, COL_PLUS_MINUS, _get_res_types('plusMinus')) +\
        _get_min_results_for_int_column(fwd_arr_int, def_arr_int, COL_PLUS_MINUS, _get_res_types('plusMinusMin')) +\
        _get_max_results_for_int_column(fwd_arr_int, def_arr_int, COL_TURNOVER, _get_res_types('turnover')) +\
        _get_min_results_for_int_column(fwd_arr_int, def_arr_int, COL_TURNOVER, _get_res_types('turnoverMin')) +\
        _get_max_results_for_int_column(fwd_arr_int, def_arr_int, COL_PENALTY_MINUTES, _get_res_types('pim')) +\
        _get_min_results_for_int_column(fwd_arr_int, def_arr_int, COL_PIM_FILTERED, _get_res_types('pimMin')) +\
        _get_max_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, COL_TOI_PER_GAME,
                                       _get_res_types('toiPerGame')) +\
        _get_max_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, COL_PP_TOI_PER_GAME,
                                       _get_res_types('ppToiPerGame')) +\
        _get_max_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, COL_SH_TOI_PER_GAME,
                                       _get_res_types('shToiPerGame')) +\
        _get_max_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, COL_HITS_PER_GAME,
                                       _get_res_types('hitsPerGame')) +\
        _get_max_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, COL_BLOCKS_PER_GAME,
                                       _get_res_types('blocksPerGame')) +\
        _get_max_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, COL_TAKEAWAYS_PER_GAME,
                                       _get_res_types('taPerGame')) +\
        _get_max_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, COL_GIVEAWAYS_PER_GAME,
                                       _get_res_types('gaPerGame')) +\
        _get_max_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, COL_SHOOTING_PERCENTAGE,
                                       _get_res_types('shootingPrc'))

    res_idx = get_indexes_max_results(fwd_arr_fp, COL_FACE_OFF_WIN_PERCENTAGE)
    res = [_get_top_results_from_fp(fwd_arr_fp, fwd_arr_int, res_idx, COL_FACE_OFF_WIN_PERCENTAGE, 'fow')]
    result.extend(res)

    return result


def _calc_skaters_stats(arr_int, arr_fp):
    arr_int[:, COL_POINTS] = arr_int[:, COL_GOALS] + arr_int[:, COL_ASSISTS]
    arr_int[:, COL_PP_POINTS] = arr_int[:, COL_PP_GOALS] + arr_int[:, COL_PP_ASSISTS]
    arr_int[:, COL_SH_POINTS] = arr_int[:, COL_SH_GOALS] + arr_int[:, COL_SH_ASSISTS]

    arr_fp[:, COL_POINTS_PER_GAME] = fraction(arr_int[:, COL_POINTS], arr_int[:, COL_GAMES])
    arr_fp[:, COL_TOI_PER_GAME] = fraction(arr_int[:, COL_TOI], arr_int[:, COL_GAMES])
    arr_fp[:, COL_SHOOTING_PERCENTAGE] = percentage(arr_int[:, COL_GOALS], arr_int[:, COL_SHOTS])
    arr_fp[:, COL_FACE_OFF_WIN_PERCENTAGE] = \
        percentage(arr_int[:, COL_FACE_OFF_WINS], arr_int[:, COL_FACE_OFF_TAKEN])


def _calc_season_stats(arr_int, arr_fp, def_only):
    _calc_skaters_stats(arr_int, arr_fp)
    arr_int[:, COL_TURNOVER] = arr_int[:, COL_TAKEAWAYS] - arr_int[:, COL_GIVEAWAYS]

    # We remove stats for players who played few games/made few shots etc.
    games_threshold = np.max(arr_int[:, COL_GAMES]) // 2
    hits_arr = np.where(arr_int[:, COL_GAMES] > games_threshold, arr_int[:, COL_HITS], 0)
    arr_fp[:, COL_HITS_PER_GAME] = fraction(hits_arr, arr_int[:, COL_GAMES])

    blocks_arr = np.where(arr_int[:, COL_GAMES] > games_threshold, arr_int[:, COL_BLOCKED], 0)
    arr_fp[:, COL_BLOCKS_PER_GAME] = fraction(blocks_arr, arr_int[:, COL_GAMES])

    ta_arr = np.where(arr_int[:, COL_GAMES] > games_threshold, arr_int[:, COL_TAKEAWAYS], 0)
    arr_fp[:, COL_TAKEAWAYS_PER_GAME] = fraction(ta_arr, arr_int[:, COL_GAMES])

    ga_arr = np.where(arr_int[:, COL_GAMES] > games_threshold, arr_int[:, COL_GIVEAWAYS], 0)
    arr_fp[:, COL_GIVEAWAYS_PER_GAME] = fraction(ga_arr, arr_int[:, COL_GAMES])

    pp_toi_arr = np.where(arr_int[:, COL_GAMES] > games_threshold, arr_int[:, COL_PP_TOI], 0)
    arr_fp[:, COL_PP_TOI_PER_GAME] = fraction(pp_toi_arr, arr_int[:, COL_GAMES])

    sh_toi_arr = np.where(arr_int[:, COL_GAMES] > games_threshold, arr_int[:, COL_SH_TOI], 0)
    arr_fp[:, COL_SH_TOI_PER_GAME] = fraction(sh_toi_arr, arr_int[:, COL_GAMES])

    shots_threshold = np.max(arr_int[:, COL_SHOTS]) // 2
    goals_arr = np.where(arr_int[:, COL_SHOTS] > shots_threshold, arr_int[:, COL_GOALS], 0)
    arr_fp[:, COL_SHOOTING_PERCENTAGE] = percentage(goals_arr, arr_int[:, COL_SHOTS])

    toi_threshold = np.max(arr_int[:, COL_TOI]) // 2
    arr_int[:, COL_PIM_FILTERED] = np.where(arr_int[:, COL_TOI] > toi_threshold, arr_int[:, COL_PENALTY_MINUTES], 1000)

    if not def_only:
        fo_taken_threshold = np.max(arr_int[:, COL_FACE_OFF_TAKEN]) // 2
        fo_wins_arr = np.where(arr_int[:, COL_FACE_OFF_TAKEN] > fo_taken_threshold, arr_int[:, COL_FACE_OFF_WINS], 0)
        arr_fp[:, COL_FACE_OFF_WIN_PERCENTAGE] = percentage(fo_wins_arr, arr_int[:, COL_FACE_OFF_TAKEN])


def _calc_skater_ext_stats(arr_int, skater_row_idx, ha_stats):
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
        _calc_60_min_stat(row, COL_PENALTY_MINUTES),  # PIMs per 60 min
        ha_stats.home_goals,
        ha_stats.away_goals,
        ha_stats.home_assists,
        ha_stats.away_assists,
        ha_stats.home_plus_minus,
        ha_stats.away_plus_minus,
        ha_stats.home_turnover,
        ha_stats.away_turnover,
        ha_stats.home_points_per_game,
        ha_stats.away_points_per_game,
        ha_stats.home_pim,
        ha_stats.away_pim
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


def _get_res_types(res_type):
    ResTypes = namedtuple('ResTypes', ['total', 'fwd', 'df'])
    return ResTypes(res_type, 'fwd{}{}'.format(res_type[0].upper(), res_type[1:]),
                    'def{}{}'.format(res_type[0].upper(), res_type[1:]))


def _get_top_results_from_int(arr, indexes, column, res_type):
    value = arr[indexes[0], column]
    return SeasonTopResult(res_type, value, [s[COL_PLAYER_ID] for s in arr[indexes, :]])


def _get_top_results_from_fp(arr_fp, arr_int, indexes, column, res_type):
    value = arr_fp[indexes[0], column]
    return SeasonTopResult(res_type, value, [arr_int[i, COL_PLAYER_ID] for i in indexes])


def _get_total_max_results(fwd_results, def_results, res_type):
    if fwd_results.value > def_results.value:
        return SeasonTopResult(res_type, fwd_results.value, fwd_results.ids)
    elif fwd_results.value < def_results.value:
        return SeasonTopResult(res_type, def_results.value, def_results.ids)
    return SeasonTopResult(res_type, fwd_results.value, fwd_results.ids + def_results.ids)


def _get_total_min_results(fwd_results, def_results, res_type):
    if fwd_results.value < def_results.value:
        return SeasonTopResult(res_type, fwd_results.value, fwd_results.ids)
    elif fwd_results.value > def_results.value:
        return SeasonTopResult(res_type, def_results.value, def_results.ids)
    return SeasonTopResult(res_type, fwd_results.value, fwd_results.ids + def_results.ids)


def _get_max_results_for_int_column(fwd_arr, def_arr, column, res_types):
    fwd_results_idx = get_indexes_max_results(fwd_arr, column)
    fwd_results = _get_top_results_from_int(fwd_arr, fwd_results_idx, column, res_types.fwd)
    def_results_idx = get_indexes_max_results(def_arr, column)
    def_results = _get_top_results_from_int(def_arr, def_results_idx, column, res_types.df)
    return [fwd_results, def_results, _get_total_max_results(fwd_results, def_results, res_types.total)]


def _get_max_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, column, res_types):
    fwd_results_idx = get_indexes_max_results(fwd_arr_fp, column)
    fwd_results = _get_top_results_from_fp(fwd_arr_fp, fwd_arr_int, fwd_results_idx, column, res_types.fwd)
    def_results_idx = get_indexes_max_results(def_arr_fp, column)
    def_results = _get_top_results_from_fp(def_arr_fp, def_arr_int, def_results_idx, column, res_types.df)
    return [fwd_results, def_results, _get_total_max_results(fwd_results, def_results, res_types.total)]


def _get_min_results_for_int_column(fwd_arr, def_arr, column, res_types):
    fwd_results_idx = get_indexes_min_results(fwd_arr, column)
    fwd_results = _get_top_results_from_int(fwd_arr, fwd_results_idx, column, res_types.fwd)
    def_results_idx = get_indexes_min_results(def_arr, column)
    def_results = _get_top_results_from_int(def_arr, def_results_idx, column, res_types.df)
    return [fwd_results, def_results, _get_total_min_results(fwd_results, def_results, res_types.total)]


def _get_min_results_for_fp_column(fwd_arr_fp, def_arr_fp, fwd_arr_int, def_arr_int, column, res_types):
    fwd_results_idx = get_indexes_min_results(fwd_arr_fp, column)
    fwd_results = _get_top_results_from_fp(fwd_arr_fp, fwd_arr_int, fwd_results_idx, column, res_types.fwd)
    def_results_idx = get_indexes_min_results(def_arr_fp, column)
    def_results = _get_top_results_from_fp(def_arr_fp, def_arr_int, def_results_idx, column, res_types.df)
    return [fwd_results, def_results, _get_total_min_results(fwd_results, def_results, res_types.total)]
