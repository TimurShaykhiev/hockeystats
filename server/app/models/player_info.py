from marshmallow import fields

from app.database import get_db
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from statistics.skater_season import get_skater_ext_stats
from statistics.goalie_season import get_goalie_ext_stats
from .player import PlayerFullInfo, PlayerFullInfoSchema
from .season import SeasonSchema
from .utils import get_team_players
from . import ModelSchema, StatValue


class _PlayerInfo:
    def __init__(self, player_id, season):
        self.season = season
        self.player = PlayerFullInfo.create(player_id, season)
        self.stats = []


class _PlayerInfoSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    player = fields.Nested(PlayerFullInfoSchema)
    stats = fields.List(StatValue())


class SkaterInfo(_PlayerInfo):
    def get_info(self):
        db = get_db()
        team_players = get_team_players(db, self.player.team_id, self.season)
        stats = SkaterSumStat.get_stat_tuples(db, self.season.id, self.season.regular)
        self.stats = get_skater_ext_stats(self.player.id, stats, team_players)
        schema = _PlayerInfoSchema()
        return schema.dumps(self)


class GoalieInfo(_PlayerInfo):
    def get_info(self):
        db = get_db()
        stats = GoalieSumStat.get_stat_tuples(db, self.season.id, self.season.regular)
        self.stats = get_goalie_ext_stats(self.player.id, stats)
        schema = _PlayerInfoSchema()
        return schema.dumps(self)
