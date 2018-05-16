from datetime import date

from marshmallow import fields
from flask import current_app

from app.api.response_utils import ApiError
from app.database import get_db
from data_models.player import Player as PlayerDm
from . import ModelSchema, get_locale, DEFAULT_LOCALE


class Player:
    def __init__(self):
        self.id = None
        self.name = ''
        self.position = ''
        self.team_id = None
        self._season = None

    @classmethod
    def create(cls, player_id, season=None, players=None):
        pl = cls()
        pl.id = player_id
        pl._season = season
        if players is not None:
            pl_info = players[player_id]
            pl.name = pl_info.name
            pl.position = pl_info.pos[0].upper()
            pl.team_id = pl_info.tid
            if pl.team_id is None:
                current_app.logger.warn('Player {} has no team id.'.format(player_id))
        else:
            db = get_db()
            pl._get_from_db(db)
        return pl

    def _get_from_db(self, db):
        locale = get_locale()
        if locale == DEFAULT_LOCALE:
            locale = None
        if self._season is None:
            pl_dm = PlayerDm.get_player(db, self.id, locale)
        else:
            pl_dm = PlayerDm.get_player_for_season(db, self.id, self._season.id, self._season.current, locale)
        if pl_dm is None:
            current_app.logger.error('Player id %s not found.', self.id)
            raise ApiError(404, 'PLAYER_NOT_FOUND')
        self._set_from_data_model(pl_dm)

    def _set_from_data_model(self, model):
        self.name = model.name
        self.position = model.primary_pos[0].upper()
        if model.current_team is not None:
            self.team_id = model.current_team.id


class PlayerSchema(ModelSchema):
    id = fields.Integer()
    name = fields.String()
    pos = fields.String(attribute='position')
    tid = fields.Integer(attribute='team_id')


class PlayerFullInfo(Player):
    def __init__(self):
        super().__init__()
        self.shoots = ''
        self.height = ''
        self.weight = ''
        self.age = None

    def _set_from_data_model(self, model):
        super()._set_from_data_model(model)
        self.shoots = model.shoots_catches[0].upper()
        locale = get_locale()
        if model.height is not None and model.height != 0:
            self.height = _convert_height(model.height, locale != 'en')
        if model.weight is not None and model.weight != 0:
            self.weight = _convert_weight(model.weight, locale != 'en')
        if model.birth_date is not None:
            self.age = _calculate_age(model.birth_date)


class PlayerFullInfoSchema(ModelSchema):
    id = fields.Integer()
    name = fields.String()
    pos = fields.String(attribute='position')
    tid = fields.Integer(attribute='team_id')
    shoots = fields.String()
    height = fields.String()
    weight = fields.String()
    age = fields.Integer()


def _convert_height(h, metric):
    # height is stored in inches
    if metric:
        return str(int(h * 2.54))
    return '{}\' {}"'.format(h // 12, h % 12)


def _convert_weight(w, metric):
    # weight is stored in pounds
    if metric:
        return str(int(w * 0.45359237))
    return str(w)


def _calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
