from marshmallow import fields
from flask import request, current_app

from database import get_db
from models import ModelSchema
from data_models.season import Season as SeasonDm
from db_utils.seasons import get_current_season
from api.response_utils import ApiError, InvalidQueryParams

SEASON_ID_QUERY_PARAM = 'sid'
SEASON_TYPE_QUERY_PARAM = 'stype'

SEASON_TYPE_REGULAR = 'reg'
SEASON_TYPE_PLAY_OFF = 'po'


class Season:
    def __init__(self):
        self.id = None
        self.year = None
        self.current = False
        self.regular = True

    @classmethod
    def create(cls):
        db = get_db()
        sid = request.args.get(SEASON_ID_QUERY_PARAM, type=int)
        s_type = request.args.get(SEASON_TYPE_QUERY_PARAM, type=str)
        if sid is None or s_type is None or (s_type != SEASON_TYPE_REGULAR and s_type != SEASON_TYPE_PLAY_OFF):
            raise InvalidQueryParams()

        dm = SeasonDm.from_db(db, sid)
        if dm is None:
            current_app.logger.error('Season id %s not found.', sid)
            raise ApiError(404, 'SEASON_NOT_FOUND')

        season = cls()
        season._set_from_data_model(dm)
        season.regular = s_type == SEASON_TYPE_REGULAR
        return season

    @classmethod
    def create_current(cls):
        db = get_db()
        dm = get_current_season(db)
        if dm is None:
            current_app.logger.error('Current season not found.')
            raise ApiError(404, 'SEASON_NOT_FOUND')

        season = cls()
        season._set_from_data_model(dm)
        season.regular = dm.status == dm.STATUS_REGULAR or dm.status == dm.STATUS_NOT_STARTED
        return season

    def _set_from_data_model(self, dm):
        self.id = dm.id
        self.current = dm.current
        self.year = dm.end.year - 1


class SeasonSchema(ModelSchema):
    id = fields.Integer()
    year = fields.Integer()
    current = fields.Boolean()
    regular = fields.Boolean()
