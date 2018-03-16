from collections import namedtuple

import numpy as np

from data_models.game import Game
from . import INT_ARRAY_DATA_TYPE, date_to_int, percentage, fraction

COL_GAME_ID = 0
COL_GAME_DATE = 1
COL_IS_REGULAR = 2
COL_WIN_TYPE = 3
COL_HOME_TEAM_ID = 4
COL_AWAY_TEAM_ID = 5
COL_HOME_GOALS = 6
COL_HOME_GOALS_PERIOD1 = 7
COL_HOME_GOALS_PERIOD2 = 8
COL_HOME_GOALS_PERIOD3 = 9
COL_HOME_SHOTS = 10
COL_HOME_PP_GOALS = 11
COL_HOME_PP_OPPORTUNITIES = 12
COL_HOME_FACE_OFF_WINS = 13
COL_HOME_BLOCKED = 14
COL_HOME_HITS = 15
COL_HOME_PENALTY_MINUTES = 16
COL_AWAY_GOALS = 17
COL_AWAY_GOALS_PERIOD1 = 18
COL_AWAY_GOALS_PERIOD2 = 19
COL_AWAY_GOALS_PERIOD3 = 20
COL_AWAY_SHOTS = 21
COL_AWAY_PP_GOALS = 22
COL_AWAY_PP_OPPORTUNITIES = 23
COL_AWAY_FACE_OFF_WINS = 24
COL_AWAY_BLOCKED = 25
COL_AWAY_HITS = 26
COL_AWAY_PENALTY_MINUTES = 27
COL_FACE_OFF_TAKEN = 28

GAME_WIN_TYPE_REGULAR = 0
GAME_WIN_TYPE_OVERTIME = 1
GAME_WIN_TYPE_SHOOTOUT = 2

WIN_TYPE_MAP = {
    Game.WIN_TYPE_REGULAR: GAME_WIN_TYPE_REGULAR,
    Game.WIN_TYPE_OVERTIME: GAME_WIN_TYPE_OVERTIME,
    Game.WIN_TYPE_SHOOTOUT: GAME_WIN_TYPE_SHOOTOUT
}

_TeamStats = namedtuple('TeamStats', ['goals', 'shots', 'pp_goals', 'pp_opportunities', 'no_goals', 'pim'])

TeamHomeAwayStats = namedtuple('TeamHomeAwayStats',
                               ['home_goals', 'away_goals', 'home_ga', 'away_ga',
                                'home_shots', 'away_shots', 'home_sa', 'away_sa',
                                'home_pp_goals', 'away_pp_goals', 'home_pp_opp', 'away_pp_opp',
                                'home_sh_goals', 'away_sh_goals', 'home_sh_opp', 'away_sh_opp',
                                'home_shutouts', 'away_shutouts',
                                'home_opp_shutouts', 'away_opp_shutouts',
                                'home_pim', 'home_opp_pim', 'away_pim', 'away_opp_pim',
                                'home_win_percentage', 'away_win_percentage'])

GameTeams = namedtuple('GameTeams', ['home_tid', 'away_tid'])

GameStats = namedtuple('GameScore', ['date', 'stats'])


def get_team_home_away_stats(team_id, games):
    games_arr = _games_to_array(games)

    home_games_arr = games_arr[games_arr[:, COL_HOME_TEAM_ID] == team_id, :]
    away_games_arr = games_arr[games_arr[:, COL_AWAY_TEAM_ID] == team_id, :]
    home_wins = np.count_nonzero(home_games_arr[:, COL_HOME_GOALS] > home_games_arr[:, COL_AWAY_GOALS])
    away_wins = np.count_nonzero(away_games_arr[:, COL_HOME_GOALS] < away_games_arr[:, COL_AWAY_GOALS])

    team_home_stats_arr = games_arr[games_arr[:, COL_HOME_TEAM_ID] == team_id, COL_HOME_GOALS:COL_AWAY_GOALS]
    opp_home_stats_arr = games_arr[games_arr[:, COL_HOME_TEAM_ID] == team_id, COL_AWAY_GOALS:COL_FACE_OFF_TAKEN]
    team_away_stats_arr = games_arr[games_arr[:, COL_AWAY_TEAM_ID] == team_id, COL_AWAY_GOALS:COL_FACE_OFF_TAKEN]
    opp_away_stats_arr = games_arr[games_arr[:, COL_AWAY_TEAM_ID] == team_id, COL_HOME_GOALS:COL_AWAY_GOALS]

    team_home_stats = _calc_stats(team_home_stats_arr)
    opp_home_stats = _calc_stats(opp_home_stats_arr)
    team_away_stats = _calc_stats(team_away_stats_arr)
    opp_away_stats = _calc_stats(opp_away_stats_arr)

    return TeamHomeAwayStats(team_home_stats.goals, team_away_stats.goals, opp_home_stats.goals, opp_away_stats.goals,
                             team_home_stats.shots, team_away_stats.shots, opp_home_stats.shots, opp_away_stats.shots,
                             team_home_stats.pp_goals, team_away_stats.pp_goals,
                             team_home_stats.pp_opportunities, team_away_stats.pp_opportunities,
                             opp_home_stats.pp_goals, opp_away_stats.pp_goals,
                             opp_home_stats.pp_opportunities, opp_away_stats.pp_opportunities,
                             opp_home_stats.no_goals, opp_away_stats.no_goals,
                             team_home_stats.no_goals, team_away_stats.no_goals,
                             team_home_stats.pim, opp_home_stats.pim, team_away_stats.pim, opp_away_stats.pim,
                             percentage(home_wins, home_games_arr.shape[0]),
                             percentage(away_wins, away_games_arr.shape[0]))


def get_home_away_dict(games):
    return dict((g[COL_GAME_ID], GameTeams(g[COL_HOME_TEAM_ID], g[COL_AWAY_TEAM_ID])) for g in games)


def get_game_stats(games):
    return [_create_game_stats(g) for g in games]


def get_team_vs_team_stats(games, team1_id, team2_id, start_date, end_date):
    start = date_to_int(start_date)
    end = date_to_int(end_date)
    games_arr = _games_to_array(games)
    games_arr = games_arr[np.logical_and(start <= games_arr[:, COL_GAME_DATE], games_arr[:, COL_GAME_DATE] < end), :]

    home1 = games_arr[games_arr[:, COL_HOME_TEAM_ID] == team1_id, COL_HOME_GOALS:COL_AWAY_GOALS]
    away1 = games_arr[games_arr[:, COL_AWAY_TEAM_ID] == team1_id, COL_AWAY_GOALS:COL_FACE_OFF_TAKEN]
    home2 = games_arr[games_arr[:, COL_HOME_TEAM_ID] == team2_id, COL_HOME_GOALS:COL_AWAY_GOALS]
    away2 = games_arr[games_arr[:, COL_AWAY_TEAM_ID] == team2_id, COL_AWAY_GOALS:COL_FACE_OFF_TAKEN]
    team1_stats_arr = np.concatenate((home1, away1))
    team2_stats_arr = np.concatenate((home2, away2))
    team1_stats = _calc_stats(team1_stats_arr)
    team2_stats = _calc_stats(team2_stats_arr)

    team1_ppp = percentage(team1_stats.pp_goals, team1_stats.pp_opportunities)
    team2_ppp = percentage(team2_stats.pp_goals, team2_stats.pp_opportunities)
    return [team1_stats.goals, team1_stats.shots, team1_stats.pim, team1_ppp, 100 - team2_ppp,
            team2_stats.goals, team2_stats.shots, team2_stats.pim, team2_ppp, 100 - team1_ppp]


def get_points_progress(team_id, games, start_date, interval):
    # interval is timedelta
    res = [0]
    acc = 0
    end_date = start_date + interval
    for g in games:
        while g[COL_GAME_DATE] > end_date:
            res.append(acc)
            end_date += interval

        winner_team_id = g[COL_HOME_TEAM_ID] if g[COL_HOME_GOALS] > g[COL_AWAY_GOALS] else g[COL_AWAY_TEAM_ID]
        if g[COL_WIN_TYPE] == Game.WIN_TYPE_REGULAR:
            if winner_team_id == team_id:
                acc += 2
        else:
            acc += 2 if winner_team_id == team_id else 1
    return res


def _games_to_array(games):
    games_arr = [(x[0], date_to_int(x[1]), x[2], WIN_TYPE_MAP[x[3]]) + x[4:] for x in games]
    return np.array(games_arr, dtype=INT_ARRAY_DATA_TYPE)


def _calc_stats(stats):
    goals = np.sum(stats[:, 0])
    shots = np.sum(stats[:, COL_HOME_SHOTS - COL_HOME_GOALS])
    pp_goals = np.sum(stats[:, COL_HOME_PP_GOALS - COL_HOME_GOALS])
    pim = np.sum(stats[:, COL_HOME_PENALTY_MINUTES - COL_HOME_GOALS])
    pp_opportunities = np.sum(stats[:, COL_HOME_PP_OPPORTUNITIES - COL_HOME_GOALS])
    no_goals = np.count_nonzero(stats[:, 0] == 0)
    return _TeamStats(goals, shots, pp_goals, pp_opportunities, no_goals, pim)


def _create_game_stats(game):
    return GameStats(game[COL_GAME_DATE], [WIN_TYPE_MAP[game[COL_WIN_TYPE]],
         game[COL_HOME_TEAM_ID], game[COL_HOME_GOALS], game[COL_HOME_SHOTS], game[COL_HOME_PP_GOALS],
         game[COL_HOME_PP_OPPORTUNITIES], game[COL_HOME_PENALTY_MINUTES],
         fraction(game[COL_AWAY_SHOTS] - game[COL_AWAY_GOALS], game[COL_AWAY_SHOTS]),  # home save percentage
         game[COL_AWAY_TEAM_ID], game[COL_AWAY_GOALS], game[COL_AWAY_SHOTS], game[COL_AWAY_PP_GOALS],
         game[COL_AWAY_PP_OPPORTUNITIES], game[COL_AWAY_PENALTY_MINUTES],
         fraction(game[COL_HOME_SHOTS] - game[COL_HOME_GOALS], game[COL_HOME_SHOTS])])  # away save percentage
