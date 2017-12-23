from marshmallow import fields

from app.database import get_db
from data_models.conference import Conference
from data_models.division import Division
from data_models.team import Team as TeamDm
from data_models.team_sum_stat import TeamSumStat
from statistics.team_season import get_teams_stats
from .team import Team, TeamSchema
from .season import SeasonSchema
from . import ModelSchema, StatValue


class TeamSeasonStats:
    def __init__(self, team, stats):
        self.team = team
        self.stats = stats


class TeamSeasonStatsSchema(ModelSchema):
    team = fields.Nested(TeamSchema)
    stats = fields.List(StatValue())


class TeamsSeasonStatsCollection:
    def __init__(self, season):
        self.season = season
        self.results = []

    def get_collection(self):
        db = get_db()
        divisions = dict((el.id, el) for el in Division.get_all(db))
        conferences = dict((el.id, el) for el in Conference.get_all(db))
        teams = dict((el.id, el) for el in TeamDm.get_all(db))
        stats_from_db = TeamSumStat.get_stat_tuples(db, self.season.id, self.season.regular)
        stats = get_teams_stats(stats_from_db)
        for st in stats:
            team = Team.create(st[0], teams, divisions, conferences)
            self.results.append(TeamSeasonStats(team, st[1:]))
        schema = TeamsSeasonStatsCollectionSchema()
        return schema.dumps(self)


class TeamsSeasonStatsCollectionSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    results = fields.Nested(TeamSeasonStatsSchema, many=True)
