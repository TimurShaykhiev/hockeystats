from marshmallow import fields
from flask import request, current_app

from database import get_db
from models import ModelSchema
from data_models.season import Season as SeasonDm
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
        self.start = None
        self.end = None

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
        season.set_from_data_model(dm)
        season.regular = s_type == SEASON_TYPE_REGULAR
        return season

    @classmethod
    def create_current(cls):
        db = get_db()
        dm = SeasonDm.get_current(db)
        if dm is None:
            current_app.logger.error('Current season not found.')
            raise ApiError(404, 'SEASON_NOT_FOUND')

        season = cls()
        season.set_from_data_model(dm)
        season.regular = dm.status == dm.STATUS_REGULAR or dm.status == dm.STATUS_NOT_STARTED
        return season

    def set_from_data_model(self, dm):
        self.id = dm.id
        self.current = dm.current
        self.year = dm.end.year - 1
        self.start = dm.start
        self.end = dm.end


class SeasonSchema(ModelSchema):
    id = fields.Integer()
    year = fields.Integer()
    current = fields.Boolean()
    regular = fields.Boolean()


class SeasonCollection:
    def __init__(self):
        self.seasons = []

    def get_collection(self):
        db = get_db()
        all_seasons = SeasonDm.get_all(db)
        if len(all_seasons) == 0:
            current_app.logger.error('Seasons are not found.')
            raise ApiError(404, 'SEASON_NOT_FOUND')
        for s in all_seasons:
            season = Season()
            season.set_from_data_model(s)
            self.seasons.append(season)
        self.seasons.sort(key=lambda x: x.year, reverse=True)
        schema = SeasonCollectionSchema()
        return schema.dumps(self)


class SeasonCollectionSchema(ModelSchema):
    seasons = fields.Nested(SeasonSchema, many=True)
