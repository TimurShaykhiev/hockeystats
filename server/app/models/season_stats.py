from marshmallow import fields

from .season import SeasonSchema
from .player import PlayerSchema
from . import ModelSchema, StatValue


class SeasonStats:
    def __init__(self, season, stats):
        self.season = season
        self.stats = stats


class SeasonStatsSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    stats = fields.List(StatValue())


class PlayerSeasonStats:
    def __init__(self, player, stats):
        self.player = player
        self.stats = stats


class PlayerSeasonStatsSchema(ModelSchema):
    player = fields.Nested(PlayerSchema)
    stats = fields.List(StatValue())
