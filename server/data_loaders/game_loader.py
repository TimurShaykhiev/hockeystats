import requests

from data_models.penalty import Penalty
from data_models.goal import Goal
from data_models.game import Game
from data_models.skater_stat import SkaterStat
from data_models.goalie_stat import GoalieStat
from data_loaders import NHL_STATS_DOMAIN

SCHEDULE_URL = NHL_STATS_DOMAIN + '/api/v1/schedule'


def get_games_list(start, end):
    """
    Get list of games for the requested time period
    :param start: start of time period (in format yyyy-mm-dd)
    :param end: end of time period (in format yyyy-mm-dd)
    :return: List of game links
    """
    links = []
    schedule = requests.get(SCHEDULE_URL, params={'startDate': start, 'endDate': end}).json()
    dates = schedule.get('dates')
    for date in dates:
        games = date.get('games')
        for game in games:
            game_type = game.get('gameType')
            if game_type == 'R' or game_type == 'P':
                game_state = game.get('status').get('abstractGameState')
                if game_state == 'Final':
                    links.append(game.get('link'))
    return links


def get_game_info(game_link):
    """
    Download and parse game info.
    :param game_link: game URL
    :return: Tuple of:
        game - game data model
        skater_stats - list of skater stat data models
        goalie_stats - list of goalkeeper stat data models
        penalties - list of penalty data models
        goals - list of goal data models
    """
    game_obj = requests.get(NHL_STATS_DOMAIN + game_link).json()
    goals = []
    penalties = []
    skater_stats = []
    goalie_stats = []

    game = Game.from_json(game_obj)

    box_score = game_obj['liveData']['boxscore']['teams']
    _add_player_stats(game, box_score['home']['players'], game.home, goalie_stats, skater_stats)
    _add_player_stats(game, box_score['away']['players'], game.away, goalie_stats, skater_stats)
    game.face_off_taken //= 2

    events = game_obj['liveData']['plays']['allPlays']
    for evt in events:
        evt_type = evt['result']['eventTypeId']
        if evt_type == 'PENALTY':
            p = Penalty.from_json(evt, game.id, game.date)
            penalties.append(p)
            _update_team_stats_penalty(game, p)
        elif evt_type == 'GOAL':
            g = Goal.from_json(evt, game.id, game.date)
            goals.append(g)
            _update_team_stats_goal(game, g)
    return game, skater_stats, goalie_stats, penalties, goals


def _add_player_stats(game, players, team_stats, goalie_stats, skater_stats):
    for pl in players.keys():
        st = SkaterStat.from_json(players[pl], game.id, team_stats.team.id, game.date)
        if st:
            skater_stats.append(st)
            _update_team_stats(team_stats, st)
            game.face_off_taken += st.face_off_taken
        else:
            st = GoalieStat.from_json(players[pl], game.id, team_stats.team.id, game.date)
            if st:
                goalie_stats.append(st)


def _update_team_stats(team_stat, skater_stats):
    team_stat.face_off_wins += skater_stats.face_off_wins
    team_stat.shots += skater_stats.shots
    team_stat.blocked += skater_stats.blocked
    team_stat.hits += skater_stats.hits


def _update_team_stats_penalty(game, penalty):
    if game.home.team.id == penalty.team.id:
        game.home.penalty_minutes += penalty.penalty_minutes
    else:
        game.away.penalty_minutes += penalty.penalty_minutes


def _update_team_stats_goal(game, goal):
    if goal.strength == 'ppg':
        if game.home.team.id == goal.team.id:
            game.home.pp_goals += 1
        else:
            game.away.pp_goals += 1
