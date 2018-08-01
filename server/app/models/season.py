from marshmallow import fields
from flask import request, current_app

from app.database import get_db
from . import ModelSchema
from data_models.season import Season as SeasonDm
from data_models.team_sum_stat import TeamSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.skater_sum_stat import SkaterSumStat
from app.api.response_utils import ApiError, InvalidQueryParams

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
        self.po_start = None
        self.end = None
        self.status = None

    @classmethod
    def create(cls):
        db = get_db()
        sid = request.args.get(SEASON_ID_QUERY_PARAM, type=int)
        s_type = request.args.get(SEASON_TYPE_QUERY_PARAM, type=str)
        if sid is None or s_type is None or (s_type != SEASON_TYPE_REGULAR and s_type != SEASON_TYPE_PLAY_OFF):
            raise InvalidQueryParams()

        dm = SeasonDm.from_db(db, sid)
        if dm is None:
            current_app.logger.info('Season id %s not found.', sid)
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
            current_app.logger.info('Current season not found.')
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
        self.po_start = dm.po_start
        self.end = dm.end
        self.status = dm.status

    def get_dates(self):
        start = self.start if self.regular else self.po_start
        end = self.po_start if self.regular else self.end
        return start, end

    def is_finished(self):
        return self.status == SeasonDm.STATUS_FINISHED or (self.regular and self.status == SeasonDm.STATUS_PLAY_OFF)


class SeasonSchema(ModelSchema):
    id = fields.Integer()
    year = fields.Integer()
    current = fields.Boolean()
    regular = fields.Boolean()
    start = fields.Date()
    end = fields.Date()
    poStart = fields.Date(attribute='po_start')


class SeasonCollection:
    def __init__(self):
        self.seasons = []

    def get_collection(self):
        db = get_db()
        all_seasons = get_all_seasons(db)
        for s in all_seasons:
            if s.status == SeasonDm.STATUS_PLAY_OFF or s.status == SeasonDm.STATUS_FINISHED:
                season = Season()
                season.set_from_data_model(s)
                season.regular = False
                self.seasons.append(season)
            season = Season()
            season.set_from_data_model(s)
            self.seasons.append(season)
        schema = _SeasonCollectionSchema()
        return schema.dumps(self)


class _SeasonCollectionSchema(ModelSchema):
    seasons = fields.Nested(SeasonSchema, many=True)


class _FilteredSeasonCollection:
    def __init__(self, object_id, object_dm_cls, object_id_field):
        self.seasons = []
        self.obj_id = object_id
        self._obj_dm_cls = object_dm_cls
        self._obj_id_field = object_id_field

    def get_collection(self):
        db = get_db()
        all_seasons = get_all_seasons(db)
        seasons = self._get_obj_seasons(db)
        self._set_seasons(all_seasons, seasons)
        schema = _FilteredSeasonCollectionSchema()
        return schema.dumps(self)

    def _set_seasons(self, all_seasons, obj_seasons):
        seasons = dict(((sid, regular), True) for sid, regular in obj_seasons)
        for s in all_seasons:
            if (s.id, False) in seasons:
                season = Season()
                season.set_from_data_model(s)
                season.regular = False
                self.seasons.append(season)
            if (s.id, True) in seasons:
                season = Season()
                season.set_from_data_model(s)
                self.seasons.append(season)

    def _get_obj_seasons(self, db):
        return self._obj_dm_cls.get_filtered(db, [self._obj_id_field], [self.obj_id],
                                             columns=['season_id', 'is_regular'])


class TeamSeasonCollection(_FilteredSeasonCollection):
    def __init__(self, team_id):
        super().__init__(team_id, TeamSumStat, 'team_id')


class SkaterSeasonCollection(_FilteredSeasonCollection):
    def __init__(self, player_id):
        super().__init__(player_id, SkaterSumStat, 'player_id')


class GoalieSeasonCollection(_FilteredSeasonCollection):
    def __init__(self, player_id):
        super().__init__(player_id, GoalieSumStat, 'player_id')


class _FilteredSeasonCollectionSchema(ModelSchema):
    id = fields.Integer(attribute='obj_id')
    seasons = fields.Nested(SeasonSchema, many=True)


def get_all_seasons(db):
    all_seasons = SeasonDm.get_all(db, order_by=['-start'])
    if len(all_seasons) == 0:
        current_app.logger.info('Seasons are not found.')
        raise ApiError(404, 'SEASON_NOT_FOUND')
    return all_seasons
