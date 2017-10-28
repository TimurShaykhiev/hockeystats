from marshmallow import fields
from flask import request

from database import get_db
from models import ModelSchema
from data_models.season import Season as SeasonDm
from db_utils.seasons import get_current_season

SEASON_ID_QUERY_PARAM = 'sid'
SEASON_REGULAR_QUERY_PARAM = 'reg'


class Season:
    def __init__(self):
        self.id = None
        self.year = None
        self.current = False
        self.regular = True

    @classmethod
    def create(cls):
        db = get_db()
        has_sid = SEASON_ID_QUERY_PARAM in request.args
        if has_sid:
            dm = SeasonDm.from_db(db, request.args.get(SEASON_ID_QUERY_PARAM, type=int))
        else:
            # Season isn't defined, return the current one. Regular query param is ignored.
            dm = get_current_season(db)
        if dm is None:
            return None

        season = cls()
        season._set_from_data_model(dm)
        if has_sid:
            # If regular is missed, set it True.
            season.regular = request.args.get(SEASON_REGULAR_QUERY_PARAM, True, type=bool)
        else:
            season._set_regular_for_current(dm)
        return season

    def _set_from_data_model(self, dm):
        self.id = dm.id
        self.current = dm.current
        self.year = dm.end.year - 1

    def _set_regular_for_current(self, dm):
        pass


class SeasonSchema(ModelSchema):
    id = fields.Integer()
    year = fields.Integer()
    current = fields.Boolean()
    regular = fields.Boolean()
