from marshmallow import fields

from models import ModelSchema


class Player:
    def __init__(self):
        self.id = None
        self.name = ''
        self.position = ''
        self.team_id = None
        self.team_name = None


class PlayerSchema(ModelSchema):
    id = fields.Integer()
    name = fields.String()
    pos = fields.String(attribute='position')
    tid = fields.Integer(attribute='team_id')
    team = fields.String(attribute='team_name')
