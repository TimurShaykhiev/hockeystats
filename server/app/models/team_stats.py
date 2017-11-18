from marshmallow import fields

from database import get_db
from data_models.conference import Conference
from data_models.division import Division
from data_models.team import Team
from data_models.team_sum_stat import TeamSumStat
from .team import Team, TeamSchema
from .season import SeasonSchema
from models import ModelSchema


def _create_team(tid, teams, divisions, conferences):
    t = teams[tid]
    team = Team()
    team.id = t.id
    team.name = t.name
    team.abbreviation = t.abbreviation
    if t.division is not None:
        d = divisions[t.division.id]
        team.division_id = d.id
        team.division_name = d.name
        if d.conference is not None:
            c = conferences[d.conference.id]
            team.conference_id = c.id
            team.conference_name = c.name
    return team


class TeamSeasonStats:
    def __init__(self, team, stats_dm):
        self.team = team
        self.stats_dm = stats_dm


class TeamSeasonStatsSchema(ModelSchema):
    team = fields.Nested(TeamSchema)
    stats = fields.Function(lambda obj: obj.stats_dm.to_tuple()[3:], attribute='stats_dm')


class TeamsSeasonStatsCollection:
    def __init__(self, season):
        self.season = season
        self.results = []

    def get_collection(self):
        db = get_db()
        divisions = dict((el.id, el) for el in Division.get_all(db))
        conferences = dict((el.id, el) for el in Conference.get_all(db))
        teams = dict((el.id, el) for el in Team.get_all(db))
        stats = TeamSumStat.get_season_stats(db, self.season.id, self.season.regular)
        for st in stats:
            team = _create_team(st.team.id, teams, divisions, conferences)
            self.results.append(TeamSeasonStats(team, st))
        schema = TeamsSeasonStatsCollectionSchema()
        return schema.dumps(self)


class TeamsSeasonStatsCollectionSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    results = fields.Nested(TeamSeasonStatsSchema, many=True)
