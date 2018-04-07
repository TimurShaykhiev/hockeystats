from collections import namedtuple

from data_models.goalie_stat import GoalieStat
from . import fraction, percentage

COL_PLAYER_ID = 0
COL_TEAM_ID = 1
COL_GAME_ID = 2
COL_DATE = 3
COL_TOI = 4
COL_ASSISTS = 5
COL_GOALS = 6
COL_PENALTY_MINUTES = 7
COL_SHOTS = 8
COL_SAVES = 9
COL_PP_SAVES = 10
COL_SH_SAVES = 11
COL_EVEN_SAVES = 12
COL_SH_SHOTS_AGAINST = 13
COL_EVEN_SHOTS_AGAINST = 14
COL_PP_SHOTS_AGAINST = 15
COL_DECISION = 16

GoalieHomeAwayStats = namedtuple('GoalieHomeAwayStats',
                                 ['home_gaa', 'away_gaa', 'home_svp', 'away_svp',
                                  'home_win_percentage', 'away_win_percentage', 'home_wins', 'away_wins'])


def get_goalie_home_away_stats(goalie_home_stats, goalie_away_stats):
    home_stats = _GoalieStats()
    away_stats = _GoalieStats()
    for s in goalie_home_stats:
        home_stats.add(s)
    for s in goalie_away_stats:
        away_stats.add(s)
    home_stats.complete()
    away_stats.complete()
    return GoalieHomeAwayStats(home_stats.gaa, away_stats.gaa, home_stats.svp, away_stats.svp,
                               home_stats.win_percentage, away_stats.win_percentage, home_stats.wins, away_stats.wins)


class _GoalieStats:
    def __init__(self):
        self.saves = 0
        self.shots = 0
        self.wins = 0
        self.gaa = 0
        self.svp = 0
        self.win_percentage = 0
        self.games = 0
        self.toi = 0

    def add(self, stats):
        self.games += 1
        self.toi += stats[COL_TOI]
        self.saves += stats[COL_SAVES]
        self.shots += stats[COL_SHOTS]
        self.wins += 1 if stats[COL_DECISION] == GoalieStat.DECISION_WINNER else 0

    def complete(self):
        self.gaa = fraction((self.shots - self.saves) * 60, round(self.toi / 60))
        self.svp = fraction(self.saves, self.shots)
        self.win_percentage = percentage(self.wins, self.games)
