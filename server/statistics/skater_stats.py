from collections import namedtuple

from . import fraction

COL_PLAYER_ID = 0
COL_TEAM_ID = 1
COL_GAME_ID = 2
COL_DATE = 3
COL_ASSISTS = 4
COL_GOALS = 5
COL_SHOTS = 6
COL_HITS = 7
COL_PP_GOALS = 8
COL_PP_ASSISTS = 9
COL_PENALTY_MINUTES = 10
COL_FACE_OFF_WINS = 11
COL_FACE_OFF_TAKEN = 12
COL_TAKEAWAYS = 13
COL_GIVEAWAYS = 14
COL_SH_GOALS = 15
COL_SH_ASSISTS = 16
COL_BLOCKED = 17
COL_PLUS_MINUS = 18
COL_TOI = 19
COL_EVEN_TOI = 20
COL_PP_TOI = 21
COL_SH_TOI = 22


SkaterHomeAwayStats = namedtuple('SkaterHomeAwayStats',
                                 ['home_goals', 'away_goals', 'home_assists', 'away_assists',
                                  'home_plus_minus', 'away_plus_minus', 'home_turnover', 'away_turnover',
                                  'home_points_per_game', 'away_points_per_game', 'home_pim', 'away_pim'])


def get_skater_home_away_stats(skater_home_stats, skater_away_stats):
    home_stats = _SkaterStats()
    away_stats = _SkaterStats()
    for s in skater_home_stats:
        home_stats.add(s)
    for s in skater_away_stats:
        away_stats.add(s)
    home_stats.complete()
    away_stats.complete()
    return SkaterHomeAwayStats(home_stats.goals, away_stats.goals, home_stats.assists, away_stats.assists,
                               home_stats.plus_minus, away_stats.plus_minus, home_stats.turnover, away_stats.turnover,
                               home_stats.points_per_games, away_stats.points_per_games,
                               home_stats.pim, away_stats.pim)


def get_points_progress(stats, start_date, interval):
    # interval is timedelta
    res = [0]
    acc = 0
    end_date = start_date + interval
    for s in stats:
        while s[COL_DATE] > end_date:
            res.append(acc)
            end_date += interval

        acc += s[COL_GOALS] + s[COL_ASSISTS]
    return res


class _SkaterStats:
    def __init__(self):
        self.goals = 0
        self.assists = 0
        self.plus_minus = 0
        self.turnover = 0
        self.points_per_games = 0
        self.pim = 0
        self.games = 0

    def add(self, stats):
        self.games += 1
        self.goals += stats[COL_GOALS]
        self.assists += stats[COL_ASSISTS]
        self.plus_minus += stats[COL_PLUS_MINUS]
        self.turnover += stats[COL_TAKEAWAYS] - stats[COL_GIVEAWAYS]
        self.pim += stats[COL_PENALTY_MINUTES]

    def complete(self):
        self.points_per_games = fraction(self.goals + self.assists, self.games)
