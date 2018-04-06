from marshmallow import fields

from app.database import get_db
from data_models.game import Game
from data_models.player import Player as PlayerDm
from data_models.skater_stat import SkaterStat
from data_models.goalie_stat import GoalieStat
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from statistics.skater_season import get_skaters_stats, get_skater_ext_stats
from statistics.goalie_season import get_goalies_stats, get_goalie_ext_stats
from .player import PlayerFullInfo, PlayerFullInfoSchema, Player, PlayerSchema
from .season import Season, SeasonSchema, get_all_seasons
from . import ModelSchema, StatValue


def _get_skater_full_stats(db, season, pid, tid):
    start, end = season.get_dates()
    sum_stats = SkaterSumStat.get_stat_tuples(db, season.id, season.regular)
    stats = SkaterStat.get_player_stats_by_date(db, pid, start, end)
    games = Game.get_season_games(db, start, end, season.regular)
    team_players = [p[0] for p in PlayerDm.get_team_players(db, tid, season.id, season.current, columns=['id'])]
    return get_skater_ext_stats(pid, sum_stats, team_players, stats, games)


def _get_goalie_full_stats(db, season, pid):
    start, end = season.get_dates()
    sum_stats = GoalieSumStat.get_stat_tuples(db, season.id, season.regular)
    stats = GoalieStat.get_player_stats_by_date(db, pid, start, end)
    games = Game.get_season_games(db, start, end, season.regular)
    return get_goalie_ext_stats(pid, sum_stats, stats, games)


class _PlayerInfo:
    def __init__(self, player_id, season):
        self.season = season
        self.player = PlayerFullInfo.create(player_id, season=season)
        self.stats = []


class _PlayerInfoSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    player = fields.Nested(PlayerFullInfoSchema)
    stats = fields.List(StatValue())


class SkaterInfo(_PlayerInfo):
    def get_info(self):
        db = get_db()
        self.stats = _get_skater_full_stats(db, self.season, self.player.id, self.player.team_id)
        schema = _PlayerInfoSchema()
        return schema.dumps(self)


class GoalieInfo(_PlayerInfo):
    def get_info(self):
        db = get_db()
        self.stats = _get_goalie_full_stats(db, self.season, self.player.id)
        schema = _PlayerInfoSchema()
        return schema.dumps(self)


class _SeasonStats:
    def __init__(self, season, team_id, stats):
        self.season = season
        self.team_id = team_id
        self.stats = stats


class _SeasonStatsSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    tid = fields.Integer(attribute='team_id')
    stats = fields.List(StatValue())


class _PlayerAllSeasonStatsCollection:
    def __init__(self, player_id):
        self.player = Player.create(player_id)
        self.results = []
        self.sum_stat_cls = None
        self.calc_stats_func = None

    def get_collection(self):
        db = get_db()
        seasons = get_all_seasons(db)
        all_seasons = dict((s.id, s) for s in seasons)
        stats_from_db = self.sum_stat_cls.get_all_seasons_stat_tuples(db, self.player.id)
        stats = self.calc_stats_func(stats_from_db)
        season_teams = PlayerDm.get_player_season_team_map(db, self.player.id, seasons)
        for st in stats:
            sid = st[1]
            season = Season()
            season.set_from_data_model(all_seasons[sid])
            season.regular = st[2]
            self.results.append(_SeasonStats(season, season_teams[sid], st[3:]))
        schema = _PlayerAllSeasonStatsCollectionSchema()
        return schema.dumps(self)


class _PlayerAllSeasonStatsCollectionSchema(ModelSchema):
    player = fields.Nested(PlayerSchema)
    results = fields.Nested(_SeasonStatsSchema, many=True)


class SkaterAllSeasonStatsCollection(_PlayerAllSeasonStatsCollection):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.sum_stat_cls = SkaterSumStat
        self.calc_stats_func = get_skaters_stats


class GoalieAllSeasonStatsCollection(_PlayerAllSeasonStatsCollection):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.sum_stat_cls = GoalieSumStat
        self.calc_stats_func = get_goalies_stats


class _PlayerCompare:
    def __init__(self, player1_id, player2_id, season):
        self.season = season
        self.player1 = PlayerFullInfo.create(player1_id, season=season)
        self.player2 = PlayerFullInfo.create(player2_id, season=season)
        self.stats1 = []
        self.stats2 = []


class SkaterCompare(_PlayerCompare):
    def get_data(self):
        db = get_db()
        self.stats1 = _get_skater_full_stats(db, self.season, self.player1.id, self.player1.team_id)
        self.stats2 = _get_skater_full_stats(db, self.season, self.player2.id, self.player2.team_id)
        schema = _PlayerCompareSchema()
        return schema.dumps(self)


class GoalieCompare(_PlayerCompare):
    def get_data(self):
        db = get_db()
        self.stats1 = _get_goalie_full_stats(db, self.season, self.player1.id)
        self.stats2 = _get_goalie_full_stats(db, self.season, self.player2.id)
        schema = _PlayerCompareSchema()
        return schema.dumps(self)


class _PlayerCompareSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    player1 = fields.Nested(PlayerFullInfoSchema)
    player2 = fields.Nested(PlayerFullInfoSchema)
    stats1 = fields.List(StatValue())
    stats2 = fields.List(StatValue())
