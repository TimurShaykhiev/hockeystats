import itertools
from collections import namedtuple

import numpy as np

from data_models.game_columns import *
from . import INT_ARRAY_DATA_TYPE, date_to_int, percentage, fraction


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

GameStats = namedtuple('GameStats', ['date', 'stats'])


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


def get_game_stats(games):
    return [_create_game_stats(g) for g in games]


def get_team_vs_team_stats(games, team1_id, team2_id, start_date, end_date):
    start = date_to_int(start_date)
    end = date_to_int(end_date)
    games_arr = _games_to_array(games)
    games_arr = games_arr[np.logical_and(start <= games_arr[:, COL_GAME_DATE], games_arr[:, COL_GAME_DATE] < end), :]
    if len(games_arr) == 0:
        return []

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


def get_tie_breaking_info(games, teams_ids):
    GameInfo = namedtuple('GameInfo', ['home_tid', 'away_tid', 'home_points', 'away_points'])

    class TeamInfo:
        def __init__(self):
            self.games = 0
            self.home_games = 0

    g_info = []
    t_info = dict((x, TeamInfo()) for x in itertools.chain.from_iterable(teams_ids))
    for g in games:
        home_tid = g[COL_HOME_TEAM_ID]
        away_tid = g[COL_AWAY_TEAM_ID]
        if g[COL_HOME_GOALS] > g[COL_AWAY_GOALS]:
            home_points = 2
            away_points = 0 if g[COL_WIN_TYPE] == Game.WIN_TYPE_REGULAR else 1
        else:
            home_points = 0 if g[COL_WIN_TYPE] == Game.WIN_TYPE_REGULAR else 1
            away_points = 2
        g_info.append(GameInfo(home_tid, away_tid, home_points, away_points))
        t_info[home_tid].games += 1
        t_info[home_tid].home_games += 1
        t_info[away_tid].games += 1

    result = dict((x, 0) for x in itertools.chain.from_iterable(teams_ids))
    for ids in teams_ids:
        is_pair = len(ids) == 2
        # find min number of games to take into account (ignore "odd" games)
        if is_pair:
            games_number = min([t_info[k].home_games for k in t_info if k in ids])
        else:
            games_number = min([t_info[k].games for k in t_info if k in ids])
        if games_number == 0:
            continue

        # set games counter to minimum value
        for t in t_info:
            if t in ids:
                if is_pair:
                    t_info[t].home_games = games_number
                else:
                    t_info[t].games = games_number

        # count point in the right games only
        for g in g_info:
            if is_pair:
                if g.home_tid in ids and t_info[g.home_tid].home_games > 0:
                    result[g.home_tid] += g.home_points
                    result[g.away_tid] += g.away_points
                    t_info[g.home_tid].home_games -= 1
            else:
                if g.home_tid in ids and t_info[g.home_tid].games > 0 and t_info[g.away_tid].games > 0:
                    result[g.home_tid] += g.home_points
                    result[g.away_tid] += g.away_points
                    t_info[g.home_tid].games -= 1
                    t_info[g.away_tid].games -= 1
        if not is_pair:
            for r in result:
                if r in ids:
                    result[r] = result[r] / (games_number * 2)
    return result


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
