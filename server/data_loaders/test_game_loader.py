from datetime import datetime
from collections import namedtuple
from random import randrange

from data_models.penalty import Penalty
from data_models.goal import Goal
from data_models.game import Game
from data_models.team import Team
from data_models.skater_stat import SkaterStat
from data_models.goalie_stat import GoalieStat
from data_loaders.test_player_loader import TEAMS, create_player


GameData = namedtuple('GameData', 'id, home, away')
GAMES = [
    GameData(id=21, home=TEAMS[0], away=TEAMS[1]),
    GameData(id=22, home=TEAMS[2], away=TEAMS[3]),
    GameData(id=23, home=TEAMS[4], away=TEAMS[7]),
    GameData(id=24, home=TEAMS[4], away=TEAMS[5]),
    GameData(id=25, home=TEAMS[6], away=TEAMS[7]),
    GameData(id=26, home=TEAMS[8], away=TEAMS[0])
]


def _get_skater_stat(game, player):
    st = SkaterStat()
    st.game = game
    st.date = game.date
    st.team = player.current_team
    st.player = player
    st.assists = randrange(0, 3)
    st.goals = randrange(0, 3)
    st.shots = randrange(0, 8)
    st.hits = randrange(0, 5)
    st.pp_goals = randrange(0, 2)
    st.pp_assists = randrange(0, 2)
    st.penalty_minutes = randrange(0, 4)
    st.face_off_wins = randrange(0, 4)
    st.face_off_taken = st.face_off_wins + randrange(2, 6)
    st.takeaways = randrange(0, 3)
    st.giveaways = randrange(0, 3)
    st.sh_goals = randrange(0, 2)
    st.sh_assists = randrange(0, 2)
    st.blocked = randrange(0, 5)
    st.plus_minus = randrange(-3, 4)
    st.even_toi = randrange(0, 600)
    st.pp_toi = randrange(0, 120)
    st.sh_toi = randrange(0, 120)
    st.toi = st.even_toi + st.pp_toi + st.sh_toi
    return st


def _get_goalie_stat(game, player):
    st = GoalieStat()
    st.game = game
    st.date = game.date
    st.team = player.current_team
    st.player = player
    st.toi = 3600
    st.assists = 0
    st.goals = 0
    st.penalty_minutes = randrange(0, 3)
    st.pp_saves = randrange(0, 30)
    st.sh_saves = randrange(0, 5)
    st.even_saves = randrange(0, 5)
    st.saves = st.even_saves + st.pp_saves + st.sh_saves
    st.sh_shots_against = st.sh_saves + randrange(0, 2)
    st.even_shots_against = st.even_saves + randrange(0, 3)
    st.pp_shots_against = st.pp_saves + randrange(0, 2)
    st.shots = st.even_shots_against + st.sh_shots_against + st.pp_shots_against
    st.decision = 'winner' if randrange(0, 2) == 1 else 'loser'
    return st


def _create_game_stat(link):
    date = datetime(2016, 4, 30).date()
    home = Team()
    home.id = GAMES[link].home.id
    away = Team()
    away.id = GAMES[link].away.id

    game = Game()
    game.id = GAMES[link].id
    game.date = date
    game.home = Game.TeamStat()
    game.home.team = home
    game.home.goals_period1 = randrange(0, 3)
    game.home.goals_period2 = randrange(0, 3)
    game.home.goals_period3 = randrange(0, 3)
    game.home.goals = game.home.goals_period1 + game.home.goals_period2 + game.home.goals_period3
    game.home.shots = randrange(10, 40)
    game.home.pp_goals = randrange(0, 2)
    game.home.pp_opportunities = game.home.pp_goals + randrange(0, 3)
    game.home.face_off_wins = randrange(10, 30)
    game.home.blocked = randrange(5, 15)
    game.home.hits = randrange(5, 15)
    game.home.penalty_minutes = randrange(0, 20)
    game.away = Game.TeamStat()
    game.away.team = away
    game.away.goals_period1 = randrange(0, 3)
    game.away.goals_period2 = randrange(0, 3)
    game.away.goals_period3 = randrange(0, 3)
    game.away.goals = game.away.goals_period1 + game.away.goals_period2 + game.away.goals_period3
    game.away.shots = randrange(10, 40)
    game.away.pp_goals = randrange(0, 2)
    game.away.pp_opportunities = game.away.pp_goals + randrange(0, 3)
    game.away.face_off_wins = randrange(10, 30)
    game.away.blocked = randrange(5, 15)
    game.away.hits = randrange(5, 15)
    game.away.penalty_minutes = randrange(0, 20)
    game.is_regular = True
    game.win_type = 'regular'
    if game.home.goals == game.away.goals:
        game.home.goals += 1
        game.home.goals_period3 += 1
    game.face_off_taken = game.home.face_off_wins + game.away.face_off_wins
    return game


def get_games_list(start, end):
    return list(range(0, 6))


def get_game_info(link):
    goals = []
    penalties = []
    skater_stats = []
    goalie_stats = []

    skaters = []
    goalies = []

    home = Team()
    home.id = GAMES[link].home.id
    away = Team()
    away.id = GAMES[link].away.id

    for i in GAMES[link].home.players:
        p = create_player(i)
        skaters.append(p)
    for i in GAMES[link].home.goalies:
        p = create_player(i)
        goalies.append(p)

    for i in GAMES[link].away.players:
        p = create_player(i)
        skaters.append(p)
    for i in GAMES[link].away.goalies:
        p = create_player(i)
        goalies.append(p)

    game = _create_game_stat(link)

    for pl in skaters:
        skater_stats.append(_get_skater_stat(game, pl))

    for pl in goalies:
        goalie_stats.append(_get_goalie_stat(game, pl))

    for i in range(0, 10):
        n = randrange(0, 20)
        pl = skaters[n]
        goal = Goal()
        goal.date = game.date
        goal.game = game
        goal.team = pl.current_team
        goal.scorer = pl
        goal.strength = 'even'
        goal.coord_x = randrange(-99, 100)
        goal.coord_y = randrange(-42, 43)
        goals.append(goal)

    for i in range(0, 10):
        n = randrange(0, 20)
        pl = skaters[n]
        pen = Penalty()
        pen.date = game.date
        pen.game = game
        pen.team = pl.current_team
        pen.penalty_on = pl
        pen.penalty_minutes = 2
        pen.coord_x = randrange(-99, 100)
        pen.coord_y = randrange(-42, 43)
        penalties.append(pen)

    return game, skater_stats, goalie_stats, penalties, goals
