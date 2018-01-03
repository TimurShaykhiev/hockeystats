from collections import namedtuple

import numpy as np

from data_models.game import Game
from . import INT_ARRAY_DATA_TYPE

COL_IS_REGULAR = 0
COL_WIN_TYPE = 1
COL_HOME_TEAM_ID = 2
COL_AWAY_TEAM_ID = 3
COL_HOME_GOALS = 4
COL_HOME_GOALS_PERIOD1 = 5
COL_HOME_GOALS_PERIOD2 = 6
COL_HOME_GOALS_PERIOD3 = 7
COL_HOME_SHOTS = 8
COL_HOME_PP_GOALS = 9
COL_HOME_PP_OPPORTUNITIES = 10
COL_HOME_FACE_OFF_WINS = 11
COL_HOME_BLOCKED = 12
COL_HOME_HITS = 13
COL_HOME_PENALTY_MINUTES = 14
COL_AWAY_GOALS = 15
COL_AWAY_GOALS_PERIOD1 = 16
COL_AWAY_GOALS_PERIOD2 = 17
COL_AWAY_GOALS_PERIOD3 = 18
COL_AWAY_SHOTS = 19
COL_AWAY_PP_GOALS = 20
COL_AWAY_PP_OPPORTUNITIES = 21
COL_AWAY_FACE_OFF_WINS = 22
COL_AWAY_BLOCKED = 23
COL_AWAY_HITS = 24
COL_AWAY_PENALTY_MINUTES = 25
COL_FACE_OFF_TAKEN = 26

GAME_WIN_TYPE_REGULAR = 0
GAME_WIN_TYPE_OVERTIME = 1
GAME_WIN_TYPE_SHOOTOUT = 2

_TeamStats = namedtuple('TeamStats', ['goals', 'shots', 'pp_goals', 'pp_opportunities', 'no_goals', 'pim'])

TeamHomeAwayStats = namedtuple('TeamHomeAwayStats',
                               ['home_goals', 'away_goals', 'home_ga', 'away_ga',
                                'home_shots', 'away_shots', 'home_sa', 'away_sa',
                                'home_pp_goals', 'away_pp_goals', 'home_pp_opp', 'away_pp_opp',
                                'home_sh_goals', 'away_sh_goals', 'home_sh_opp', 'away_sh_opp',
                                'home_shutouts', 'away_shutouts',
                                'home_pim', 'home_opp_pim', 'away_pim', 'away_opp_pim'])


def get_team_home_away_stats(team_id, games):
    games_arr = _games_to_array(games)

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
                             team_home_stats.pim, opp_home_stats.pim, team_away_stats.pim, opp_away_stats.pim)


def _games_to_array(games):
    win_type_map = {
        Game.WIN_TYPE_REGULAR: GAME_WIN_TYPE_REGULAR,
        Game.WIN_TYPE_OVERTIME: GAME_WIN_TYPE_OVERTIME,
        Game.WIN_TYPE_SHOOTOUT: GAME_WIN_TYPE_SHOOTOUT
    }
    games_arr = [(x[2], win_type_map[x[3]]) + x[4:] for x in games]
    return np.array(games_arr, dtype=INT_ARRAY_DATA_TYPE)


def _calc_stats(stats):
    goals = np.sum(stats[:, 0])
    shots = np.sum(stats[:, COL_HOME_SHOTS - COL_HOME_GOALS])
    pp_goals = np.sum(stats[:, COL_HOME_PP_GOALS - COL_HOME_GOALS])
    pim = np.sum(stats[:, COL_HOME_PENALTY_MINUTES - COL_HOME_GOALS])
    pp_opportunities = np.sum(stats[:, COL_HOME_PP_OPPORTUNITIES - COL_HOME_GOALS])
    no_goals = np.count_nonzero(stats[:, 0] == 0)
    return _TeamStats(goals, shots, pp_goals, pp_opportunities, no_goals, pim)