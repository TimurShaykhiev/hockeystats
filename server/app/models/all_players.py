from collections import namedtuple

from marshmallow import fields

from app.database import get_db
from data_models.player import Player
from .season import SeasonSchema
from . import ModelSchema

PlayerShortInfo = namedtuple('PlayerShortInfo', ['id', 'name'])


class _AllPlayersCollection:
    def __init__(self, season):
        self.season = season
        self.players = []
        self._get_players_func = None

    def get_collection(self):
        db = get_db()
        self.players = self._get_players_func(db, self.season.id, self.season.regular,
                                              columns=['id', 'name'], named_tuple_cls=PlayerShortInfo)
        schema = _AllPlayersCollectionSchema()
        return schema.dumps(self)


class AllSkatersCollection(_AllPlayersCollection):
    def __init__(self, season):
        super().__init__(season)
        self._get_players_func = Player.get_skaters_for_season


class AllGoaliesCollection(_AllPlayersCollection):
    def __init__(self, season):
        super().__init__(season)
        self._get_players_func = Player.get_goalies_for_season


class _PlayerShortSchema(ModelSchema):
    id = fields.Integer()
    name = fields.String()


class _AllPlayersCollectionSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    players = fields.Nested(_PlayerShortSchema, many=True)
