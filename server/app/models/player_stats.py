from marshmallow import fields

from app.database import get_db
from data_models.player import Player as PlayerDm
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from statistics.skater_season import get_skaters_stats
from statistics.goalie_season import get_goalies_stats
from .player import Player
from .season import SeasonSchema
from .season_stats import PlayerSeasonStats, PlayerSeasonStatsSchema
from . import ModelSchema, get_locale, DEFAULT_LOCALE


def _get_all_players_info(db, data_getter_func, season, lang):
    pl_list = data_getter_func(db, season.id, season.regular, season.current, False, lang)
    # Convert to dict for quick search
    return dict((p.id, p) for p in pl_list)


class _PlayerSeasonStatsCollection:
    def __init__(self, season):
        self.season = season
        self.results = []
        self.get_players_func = None
        self.get_stats_func = None
        self.calc_stats_func = None

    def get_collection(self):
        locale = get_locale()
        if locale == DEFAULT_LOCALE:
            locale = None

        db = get_db()
        players = _get_all_players_info(db, self.get_players_func, self.season, locale)
        stats_from_db = self.get_stats_func(db, self.season.id, self.season.regular)
        stats = self.calc_stats_func(stats_from_db)
        for st in stats:
            pl = Player.create(st[0], season=self.season, players=players)
            self.results.append(PlayerSeasonStats(pl, st[3:]))
        schema = _PlayerSeasonStatsCollectionSchema()
        return schema.dumps(self)


class SkatersSeasonStatsCollection(_PlayerSeasonStatsCollection):
    def __init__(self, season):
        super().__init__(season)
        self.get_players_func = PlayerDm.get_skaters_for_season
        self.get_stats_func = SkaterSumStat.get_stat_tuples
        self.calc_stats_func = get_skaters_stats


class GoaliesSeasonStatsCollection(_PlayerSeasonStatsCollection):
    def __init__(self, season):
        super().__init__(season)
        self.get_players_func = PlayerDm.get_goalies_for_season
        self.get_stats_func = GoalieSumStat.get_stat_tuples
        self.calc_stats_func = get_goalies_stats


class _PlayerSeasonStatsCollectionSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    results = fields.Nested(PlayerSeasonStatsSchema, many=True)
