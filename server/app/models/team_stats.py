from marshmallow import fields

from app.database import get_db
from data_models.team_sum_stat import TeamSumStat
from statistics.team_season import get_teams_stats
from .season import SeasonSchema
from . import ModelSchema, StatValue


class TeamSeasonStats:
    def __init__(self, team_id, stats):
        self.team_id = team_id
        self.stats = stats


class TeamSeasonStatsSchema(ModelSchema):
    id = fields.Integer(attribute='team_id')
    stats = fields.List(StatValue())


class TeamsSeasonStatsCollection:
    def __init__(self, season):
        self.season = season
        self.results = []

    def get_collection(self):
        db = get_db()
        stats_from_db = TeamSumStat.get_stat_tuples(db, self.season.id, self.season.regular)
        stats = get_teams_stats(stats_from_db)
        for st in stats:
            self.results.append(TeamSeasonStats(st[0], st[1:]))
        schema = TeamsSeasonStatsCollectionSchema()
        return schema.dumps(self)


class TeamsSeasonStatsCollectionSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    results = fields.Nested(TeamSeasonStatsSchema, many=True)
