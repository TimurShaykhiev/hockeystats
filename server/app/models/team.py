from marshmallow import fields

from models import ModelSchema


class Team:
    def __init__(self):
        self.id = None
        self.name = ''
        self.abbreviation = ''
        self.division_id = None
        self.division_name = None
        self.conference_id = None
        self.conference_name = None


class TeamSchema(ModelSchema):
    id = fields.Integer()
    name = fields.String()
    abbr = fields.String(attribute='position')
    did = fields.Integer(attribute='division_id')
    division = fields.String(attribute='division_name')
    cid = fields.Integer(attribute='conference_id')
    conference = fields.String(attribute='conference_name')
