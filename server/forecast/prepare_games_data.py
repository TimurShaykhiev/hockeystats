from datetime import date

import numpy as np

from data_models.game_columns import *
from statistics import fraction
from forecast.games_dataset_features import *

BASE_DATE = date(2013, 1, 1)

GAMES_LONG_INTERVAL = 10
GAMES_SHORT_INTERVAL = 3
GAMES_H2H_INTERVAL = 5

MAX_DAYS_SINCE_LAST_GAME = 5
MAX_DAYS_SINCE_LAST_HOME_GAME = 10

# Classes for our model - how many points teams get for the game
TARGET = {
    (2, 0): 0,  # home team: 2 points, away team: 0 points
    (2, 1): 1,  # home team: 2 points, away team: 1 point
    (1, 2): 2,  # home team: 1 point,  away team: 2 points
    (0, 2): 3   # home team: 0 points, away team: 2 points
}


def _date_to_days(d):
    """ Returns number of days between 'd' and BASE_DATE """
    return (d - BASE_DATE).days


def _find_prev_games_and_days_since(arr, cur_idx):
    home_tid = arr[cur_idx, COL_HOME_TEAM_ID]
    away_tid = arr[cur_idx, COL_AWAY_TEAM_ID]
    cur_days = arr[cur_idx, COL_GAME_DATE]

    home_indexes = []
    away_indexes = []
    h2h_indexes = []
    home_last_game_day_diff = 0
    home_last_home_game_day_diff = 0
    away_last_game_day_diff = 0
    away_last_home_game_day_diff = 0

    for i in range(cur_idx - 1, -1, -1):
        game = arr[i]
        if home_last_game_day_diff == 0 and (game[COL_HOME_TEAM_ID] == home_tid or game[COL_AWAY_TEAM_ID] == home_tid):
            home_last_game_day_diff = min(cur_days - game[COL_GAME_DATE], MAX_DAYS_SINCE_LAST_GAME)
        if home_last_home_game_day_diff == 0 and game[COL_HOME_TEAM_ID] == home_tid:
            home_last_home_game_day_diff = min(cur_days - game[COL_GAME_DATE], MAX_DAYS_SINCE_LAST_HOME_GAME)
        if away_last_game_day_diff == 0 and (game[COL_HOME_TEAM_ID] == away_tid or game[COL_AWAY_TEAM_ID] == away_tid):
            away_last_game_day_diff = min(cur_days - game[COL_GAME_DATE], MAX_DAYS_SINCE_LAST_GAME)
        if away_last_home_game_day_diff == 0 and game[COL_HOME_TEAM_ID] == away_tid:
            away_last_home_game_day_diff = min(cur_days - game[COL_GAME_DATE], MAX_DAYS_SINCE_LAST_HOME_GAME)

        if len(home_indexes) < GAMES_LONG_INTERVAL and \
                (game[COL_HOME_TEAM_ID] == home_tid or game[COL_AWAY_TEAM_ID] == home_tid):
            home_indexes.insert(0, i)
        if len(away_indexes) < GAMES_LONG_INTERVAL and \
                (game[COL_HOME_TEAM_ID] == away_tid or game[COL_AWAY_TEAM_ID] == away_tid):
            away_indexes.insert(0, i)
        if len(h2h_indexes) < GAMES_H2H_INTERVAL and \
                (game[COL_HOME_TEAM_ID] == away_tid or game[COL_AWAY_TEAM_ID] == away_tid) and \
                (game[COL_HOME_TEAM_ID] == home_tid or game[COL_AWAY_TEAM_ID] == home_tid):
            h2h_indexes.insert(0, i)

        if len(home_indexes) == GAMES_LONG_INTERVAL and len(away_indexes) == GAMES_LONG_INTERVAL and \
                len(h2h_indexes) == GAMES_H2H_INTERVAL:
            break

    if home_last_game_day_diff == 0:
        home_last_game_day_diff = MAX_DAYS_SINCE_LAST_GAME
    if home_last_home_game_day_diff == 0:
        home_last_home_game_day_diff = MAX_DAYS_SINCE_LAST_HOME_GAME
    if away_last_game_day_diff == 0:
        away_last_game_day_diff = MAX_DAYS_SINCE_LAST_GAME
    if away_last_home_game_day_diff == 0:
        away_last_home_game_day_diff = MAX_DAYS_SINCE_LAST_HOME_GAME

    return home_indexes, away_indexes, h2h_indexes, home_last_game_day_diff, home_last_home_game_day_diff, \
           away_last_game_day_diff, away_last_home_game_day_diff


def _add_features(games_arr, tid, features, start_idx):
    num = games_arr.shape[0]

    # swap columns to have this team stats in the HOME columns for easier calculations
    arr = games_arr.copy()
    old_col = np.array(
        [COL_HOME_GOALS, COL_HOME_GOALS_PERIOD1, COL_HOME_GOALS_PERIOD2, COL_HOME_GOALS_PERIOD3, COL_HOME_SHOTS,
         COL_HOME_PP_GOALS, COL_HOME_PP_OPPORTUNITIES, COL_HOME_FACE_OFF_WINS, COL_HOME_BLOCKED, COL_HOME_HITS,
         COL_HOME_PENALTY_MINUTES, COL_AWAY_GOALS, COL_AWAY_GOALS_PERIOD1, COL_AWAY_GOALS_PERIOD2,
         COL_AWAY_GOALS_PERIOD3, COL_AWAY_SHOTS, COL_AWAY_PP_GOALS, COL_AWAY_PP_OPPORTUNITIES, COL_AWAY_FACE_OFF_WINS,
         COL_AWAY_BLOCKED, COL_AWAY_HITS, COL_AWAY_PENALTY_MINUTES])
    new_col = np.array(
        [COL_AWAY_GOALS, COL_AWAY_GOALS_PERIOD1, COL_AWAY_GOALS_PERIOD2, COL_AWAY_GOALS_PERIOD3, COL_AWAY_SHOTS,
         COL_AWAY_PP_GOALS, COL_AWAY_PP_OPPORTUNITIES, COL_AWAY_FACE_OFF_WINS, COL_AWAY_BLOCKED, COL_AWAY_HITS,
         COL_AWAY_PENALTY_MINUTES, COL_HOME_GOALS, COL_HOME_GOALS_PERIOD1, COL_HOME_GOALS_PERIOD2,
         COL_HOME_GOALS_PERIOD3, COL_HOME_SHOTS, COL_HOME_PP_GOALS, COL_HOME_PP_OPPORTUNITIES, COL_HOME_FACE_OFF_WINS,
         COL_HOME_BLOCKED, COL_HOME_HITS, COL_HOME_PENALTY_MINUTES])
    rows = (arr[:, COL_AWAY_TEAM_ID] == tid).nonzero()[0]  # find row indexes where this team was away team
    arr[rows[:, None], new_col] = arr[rows[:, None], old_col]  # swap away and home teams stats

    # now this team stats are home stats and opponent stats are away stats
    features[FEATURE_STAT_GOALS_PER_GAME + start_idx] = np.sum(arr[:, COL_HOME_GOALS]) / num
    features[FEATURE_STAT_GOALS_AGAINST_PER_GAME + start_idx] = np.sum(arr[:, COL_AWAY_GOALS]) / num
    features[FEATURE_STAT_PERIOD1_GOALS_DIFF_PER_GAME + start_idx] = \
        (np.sum(arr[:, COL_HOME_GOALS_PERIOD1]) - np.sum(arr[:, COL_AWAY_GOALS_PERIOD1])) / num
    features[FEATURE_STAT_PERIOD2_GOALS_DIFF_PER_GAME + start_idx] = \
        (np.sum(arr[:, COL_HOME_GOALS_PERIOD2]) - np.sum(arr[:, COL_AWAY_GOALS_PERIOD2])) / num
    features[FEATURE_STAT_PERIOD3_GOALS_DIFF_PER_GAME + start_idx] = \
        (np.sum(arr[:, COL_HOME_GOALS_PERIOD3]) - np.sum(arr[:, COL_AWAY_GOALS_PERIOD3])) / num
    features[FEATURE_STAT_SHOTS_PER_GAME + start_idx] = np.sum(arr[:, COL_HOME_SHOTS]) / num
    features[FEATURE_STAT_PP_OPP_PER_GAME + start_idx] = np.sum(arr[:, COL_HOME_PP_OPPORTUNITIES]) / num
    features[FEATURE_STAT_BLOCKS_PER_GAME + start_idx] = np.sum(arr[:, COL_HOME_BLOCKED]) / num
    features[FEATURE_STAT_HITS_PER_GAME + start_idx] = np.sum(arr[:, COL_HOME_HITS]) / num
    features[FEATURE_STAT_PIM_PER_GAME + start_idx] = np.sum(arr[:, COL_HOME_PENALTY_MINUTES]) / num
    features[FEATURE_STAT_PPP + start_idx] = \
        fraction(np.sum(arr[:, COL_HOME_PP_GOALS]), np.sum(arr[:, COL_HOME_PP_OPPORTUNITIES]))
    features[FEATURE_STAT_PKP + start_idx] = \
        1 - fraction(np.sum(arr[:, COL_AWAY_PP_GOALS]), np.sum(arr[:, COL_AWAY_PP_OPPORTUNITIES]))
    features[FEATURE_STAT_FOW_PERCENTAGE + start_idx] = \
        fraction(np.sum(arr[:, COL_HOME_FACE_OFF_WINS]), np.sum(arr[:, COL_FACE_OFF_TAKEN]))

    for st in arr:
        if st[COL_HOME_GOALS] > st[COL_AWAY_GOALS]:
            if st[COL_WIN_TYPE] == GAME_WIN_TYPE_REGULAR:
                features[FEATURE_STAT_WINS + start_idx] += 1
            else:
                features[FEATURE_STAT_WINS_OT + start_idx] += 1
        else:
            if st[COL_WIN_TYPE] == GAME_WIN_TYPE_REGULAR:
                features[FEATURE_STAT_LOSS + start_idx] += 1
            else:
                features[FEATURE_STAT_LOSS_OT + start_idx] += 1


def get_games_data(games):
    g = [(x[0], _date_to_days(x[1]), x[2], WIN_TYPE_MAP[x[3]]) + x[4:] for x in games]
    games_arr = np.array(g, dtype=np.int32)
    dataset_size = games_arr.shape[0]

    x = np.zeros((dataset_size, FEATURE_COUNT), dtype=np.float64)
    y = np.zeros(dataset_size, dtype=np.int32)

    idx = 0
    for i in range(1, games_arr.shape[0]):
        game = games_arr[i]
        home_tid = game[COL_HOME_TEAM_ID]
        away_tid = game[COL_AWAY_TEAM_ID]
        features = x[idx]

        home_indexes, away_indexes, h2h_indexes, home_days_since_last_game, home_days_since_last_home_game, \
           away_days_since_last_game, away_days_since_last_home_game = _find_prev_games_and_days_since(games_arr, i)

        if len(home_indexes) == 0 or len(away_indexes) == 0:
            continue

        features[FEATURE_IS_REGULAR] = game[COL_IS_REGULAR]
        features[FEATURE_HOME_DAYS_SINCE_LAST_GAME] = home_days_since_last_game
        features[FEATURE_HOME_DAYS_SINCE_LAST_HOME_GAME] = home_days_since_last_home_game
        features[FEATURE_AWAY_DAYS_SINCE_LAST_GAME] = away_days_since_last_game
        features[FEATURE_AWAY_DAYS_SINCE_LAST_HOME_GAME] = away_days_since_last_home_game

        _add_features(games_arr[home_indexes], home_tid, features, FEATURE_L_HOME_GOALS_PER_GAME)
        _add_features(games_arr[home_indexes[-GAMES_SHORT_INTERVAL:]], home_tid, features,
                      FEATURE_S_HOME_GOALS_PER_GAME)
        _add_features(games_arr[away_indexes], away_tid, features, FEATURE_L_AWAY_GOALS_PER_GAME)
        _add_features(games_arr[away_indexes[-GAMES_SHORT_INTERVAL:]], away_tid, features,
                      FEATURE_S_AWAY_GOALS_PER_GAME)
        if len(h2h_indexes) > 0:
            _add_features(games_arr[h2h_indexes], home_tid, features, FEATURE_H2H_HOME_GOALS_PER_GAME)
            _add_features(games_arr[h2h_indexes], away_tid, features, FEATURE_H2H_AWAY_GOALS_PER_GAME)
        else:
            # when we don't have head-to-head stats yet, use long interval stats instead
            features[FEATURE_H2H_HOME_GOALS_PER_GAME:FEATURE_AWAY_DAYS_SINCE_LAST_GAME] = \
                features[FEATURE_L_HOME_GOALS_PER_GAME:FEATURE_S_HOME_GOALS_PER_GAME]
            features[FEATURE_H2H_AWAY_GOALS_PER_GAME:] = \
                features[FEATURE_L_AWAY_GOALS_PER_GAME:FEATURE_S_AWAY_GOALS_PER_GAME]

        # expected result
        if game[COL_HOME_GOALS] > game[COL_AWAY_GOALS]:
            home_points = 2
            away_points = 0 if game[COL_WIN_TYPE] == GAME_WIN_TYPE_REGULAR else 1
        else:
            home_points = 0 if game[COL_WIN_TYPE] == GAME_WIN_TYPE_REGULAR else 1
            away_points = 2
        y[idx] = TARGET[(home_points, away_points)]
        idx += 1

    return x[:idx], y[:idx]
