from marshmallow import fields

from . import ModelSchema


class Player:
    def __init__(self):
        self.id = None
        self.name = ''
        self.position = ''
        self.team_id = None

    def update_team_id(self, season, trades):
        if len(trades) == 0:
            return
        new_tid = None
        for tr in trades:
            if tr.date < season.end:
                new_tid = tr.to_team
            if tr.date >= season.end:
                new_tid = tr.from_team
                break
        self.team_id = new_tid


class PlayerSchema(ModelSchema):
    id = fields.Integer()
    name = fields.String()
    pos = fields.String(attribute='position')
    tid = fields.Integer(attribute='team_id')
