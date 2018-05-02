from marshmallow import fields

from app.database import get_db
from data_models.conference import Conference
from data_models.division import Division
from data_models.team import Team as TeamDm
from data_models.translation import Translation
from .team import Team, TeamSchema
from .season import SeasonSchema
from . import ModelSchema, get_locale, DEFAULT_LOCALE


class AllTeamsCollection:
    def __init__(self, season):
        self.season = season
        self.teams = []

    def get_collection(self):
        db = get_db()
        divisions = dict((el.id, el) for el in Division.get_all(db))
        conferences = dict((el.id, el) for el in Conference.get_all(db))
        teams = dict((el.id, el) for el in TeamDm.get_for_season(db, self.season.id, self.season.regular))
        team_strings = None

        locale = get_locale()
        if locale != DEFAULT_LOCALE:
            team_strings = Translation.get_all_teams_strings(db, locale)

        for t in teams.keys():
            team = Team.create(t, teams, divisions, conferences, team_strings)
            self.teams.append(team)
        schema = _AllTeamsCollectionSchema()
        return schema.dumps(self)


class _AllTeamsCollectionSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    teams = fields.Nested(TeamSchema, many=True)
