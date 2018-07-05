from marshmallow import fields

from app.database import get_db
from data_models.team_sum_stat import SeasonStat
from .season import Season, get_all_seasons
from .season_stats import SeasonStats, SeasonStatsSchema
from . import ModelSchema


class _SeasonStatsCollectionSchema(ModelSchema):
    regular = fields.Nested(SeasonStatsSchema, many=True)
    po = fields.Nested(SeasonStatsSchema, many=True)


class SeasonStatsCollection:
    def __init__(self):
        self.regular = []
        self.po = []

    def get_collection(self):
        db = get_db()
        all_seasons = dict((s.id, s) for s in get_all_seasons(db))
        stats = SeasonStat.get_all_seasons_stats(db)
        for st in stats:
            season = Season()
            season.set_from_data_model(all_seasons[st[0]])
            season.regular = st[1]
            season_stats = SeasonStats(season, st[2:])
            if season.regular:
                self.regular.append(season_stats)
            else:
                self.po.append(season_stats)
        schema = _SeasonStatsCollectionSchema()
        return schema.dumps(self)
