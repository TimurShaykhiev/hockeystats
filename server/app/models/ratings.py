from collections import namedtuple

from marshmallow import fields

from app.database import get_db
from data_models.goal import Goal
from data_models.player import Player as PlayerDm
from data_models.skater_sum_stat import SkaterSumStat
from .season import SeasonSchema
from .player import Player, PlayerSchema
from . import ModelSchema, get_locale, DEFAULT_LOCALE

RATING_ELEMENTS_LIMIT = 20

ScorerDuoData = namedtuple('ScorerDuoData', ['goals', 'pid1', 'pid2', 'pp1', 'pp2'])


class _ScorerDuoSchema(ModelSchema):
    pid1 = fields.Integer()
    pid2 = fields.Integer()
    pp1 = fields.Integer()
    pp2 = fields.Integer()
    g = fields.Integer(attribute='goals')


class _ScorerDuosRatingSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    players = fields.Nested(PlayerSchema, many=True)
    rating = fields.Nested(_ScorerDuoSchema, many=True)


class ScorerDuos:
    def __init__(self, season):
        self.season = season
        self.players = []
        self.rating = []

    def get_data(self):
        db = get_db()
        start, end = self.season.get_dates()
        locale = get_locale()
        if locale == DEFAULT_LOCALE:
            locale = None

        scorer_duos = Goal.get_scorer_duos(db, start, end, RATING_ELEMENTS_LIMIT)
        pl_ids = set()
        for sd in scorer_duos:
            pl_ids.add(sd.pid1)
            pl_ids.add(sd.pid2)
        pl_ids = list(pl_ids)

        pl_list = PlayerDm.get_players(db, pl_ids, self.season.id, self.season.current, False, locale)
        pl_dict = dict((p.id, p) for p in pl_list)
        for p in pl_ids:
            pl = Player.create(p, season=self.season, players=pl_dict)
            self.players.append(pl)

        stat_list = SkaterSumStat.get_group_stat_tuples(db, pl_ids, self.season.id, self.season.regular,
                                                        ['player_id', 'goals', 'assists'])
        stats = dict((st[0], st[1] + st[2]) for st in stat_list)
        for sd in scorer_duos:
            self.rating.append(ScorerDuoData(sd.goals, sd.pid1, sd.pid2, stats[sd.pid1], stats[sd.pid2]))

        schema = _ScorerDuosRatingSchema()
        return schema.dumps(self)
