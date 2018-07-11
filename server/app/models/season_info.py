from marshmallow import fields
from flask import current_app

from app.database import get_db
from app.api.response_utils import ApiError
from data_models.player import Player as PlayerDm
from data_models.team_sum_stat import SeasonStat, TeamSumStat
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from statistics.skater_season import get_skaters_season_top_results
from statistics.goalie_season import get_goalies_season_top_results
from statistics.team_season import get_teams_season_top_results
from .season import Season, SeasonSchema, get_all_seasons
from .season_stats import SeasonStats, SeasonStatsSchema
from .player import Player, PlayerSchema
from . import ModelSchema, StatValue, get_locale, DEFAULT_LOCALE


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


class _SeasonSkatersTopResultSchema(ModelSchema):
    type = fields.String()
    pid = fields.Integer()
    value = StatValue()


class _SeasonTeamsTopResultSchema(ModelSchema):
    type = fields.String()
    tid = fields.Integer()
    value = StatValue()


class _SeasonInfoSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    stats = fields.List(StatValue())
    players = fields.Nested(PlayerSchema, many=True)
    tops = fields.Nested(_SeasonSkatersTopResultSchema, many=True)
    teamTops = fields.Nested(_SeasonTeamsTopResultSchema, many=True, attribute='team_tops')


class SeasonInfo:
    def __init__(self, season):
        if not season.is_finished():
            current_app.logger.error('Season (id: %s, regular: %s) not finished.', season.id, season.regular)
            raise ApiError(422, 'SEASON_NOT_FINISHED')
        self.season = season
        self.stats = []
        self.players = []
        self.tops = []
        self.team_tops = []

    def get_data(self):
        db = get_db()
        locale = get_locale()
        if locale == DEFAULT_LOCALE:
            locale = None

        self.stats = SeasonStat.get_season_sum_stats(db, self.season.id, self.season.regular)[0]

        fwd_stats = SkaterSumStat.get_forwards_season_stats(db, self.season.id, self.season.regular)
        def_stats = SkaterSumStat.get_defensemen_season_stats(db, self.season.id, self.season.regular)
        self.tops = get_skaters_season_top_results(fwd_stats, def_stats)

        goalie_stats = GoalieSumStat.get_stat_tuples(db, self.season.id, self.season.regular)
        self.tops.extend(get_goalies_season_top_results(goalie_stats))

        team_stats = TeamSumStat.get_stat_tuples(db, self.season.id, self.season.regular)
        self.team_tops = get_teams_season_top_results(team_stats)

        pl_ids = set()
        for res in self.tops:
            pl_ids.add(res.pid)
        pl_ids = list(pl_ids)
        pl_list = PlayerDm.get_players(db, pl_ids, self.season.id, self.season.current, False, locale)
        pl_dict = dict((p.id, p) for p in pl_list)
        for p in pl_ids:
            pl = Player.create(p, season=self.season, players=pl_dict)
            self.players.append(pl)

        schema = _SeasonInfoSchema()
        return schema.dumps(self)
