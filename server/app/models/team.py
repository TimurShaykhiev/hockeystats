from marshmallow import fields
from flask import current_app

from app.database import get_db
from data_models.conference import Conference
from data_models.division import Division
from data_models.team import Team as TeamDm
from app.api.response_utils import ApiError
from . import ModelSchema


class Team:
    def __init__(self):
        self.id = None
        self.name = ''
        self.abbreviation = ''
        self.division_id = None
        self.division_name = None
        self.conference_id = None
        self.conference_name = None

    @classmethod
    def create(cls, team_id, teams=None, divisions=None, conferences=None):
        team = cls()
        team.id = team_id
        if teams is not None and divisions is not None and conferences is not None:
            t = teams[team_id]
            team.name = t.name
            if t.division is not None:
                d = divisions[t.division.id]
                team.division_id = d.id
                team.division_name = d.name
                if d.conference is not None:
                    c = conferences[d.conference.id]
                    team.conference_id = c.id
                    team.conference_name = c.name
        else:
            team._get_from_db()
        return team

    def _get_from_db(self):
        db = get_db()
        team_dm = TeamDm.from_db(db, self.id)
        if team_dm is None:
            current_app.logger.error('Team id %s not found.', self.id)
            raise ApiError(404, 'TEAM_NOT_FOUND')

        self.name = team_dm.name
        self.abbreviation = team_dm.abbreviation
        if team_dm.division is not None:
            div_dm = Division.from_db(db, team_dm.division.id)
            if div_dm is not None:
                self.division_id = div_dm.id
                self.division_name = div_dm.name
                if div_dm.conference is not None:
                    conf_dm = Conference.from_db(db, div_dm.conference.id)
                    if conf_dm is not None:
                        self.conference_id = conf_dm.id
                        self.conference_name = conf_dm.name


class TeamSchema(ModelSchema):
    id = fields.Integer()
    name = fields.String()
    abbr = fields.String(attribute='abbreviation')
    did = fields.Integer(attribute='division_id')
    division = fields.String(attribute='division_name')
    cid = fields.Integer(attribute='conference_id')
    conference = fields.String(attribute='conference_name')
