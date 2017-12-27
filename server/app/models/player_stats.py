from marshmallow import fields

from app.database import get_db
from data_models.player import Player as PlayerDm
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.player_trade import PlayerTrade
from statistics.skater_season import get_skaters_stats
from statistics.goalie_season import get_goalies_stats
from .player import Player, PlayerSchema, PlayerInfo
from .season import SeasonSchema
from . import ModelSchema, StatValue


def _get_all_players_info(db, data_getter_func, check_trades):
    pl_list = data_getter_func(db, ['id', 'name', 'current_team_id', 'primary_pos'])
    # Convert to dict for quick search
    info = dict((pid, PlayerInfo(name, tid, pos, [])) for pid, name, tid, pos in pl_list)
    if check_trades:
        pl_trades_list = PlayerTrade.get_all(db, order_by=['date'])
        for trade in pl_trades_list:
            if trade.player_id in info:
                info[trade.player_id].trades.append(trade)
    return info


class PlayerSeasonStats:
    def __init__(self, player, stats):
        self.player = player
        self.stats = stats


class PlayerSeasonStatsSchema(ModelSchema):
    player = fields.Nested(PlayerSchema)
    stats = fields.List(StatValue())


class PlayerSeasonStatsCollection:
    def __init__(self, season):
        self.season = season
        self.results = []
        self.get_players_func = None
        self.get_stats_func = None
        self.calc_stats_func = None

    def get_collection(self):
        db = get_db()
        players = _get_all_players_info(db, self.get_players_func, not self.season.current)
        stats_from_db = self.get_stats_func(db, self.season.id, self.season.regular)
        stats = self.calc_stats_func(stats_from_db)
        for st in stats:
            pl = Player.create(st[0], self.season, players)
            self.results.append(PlayerSeasonStats(pl, st[1:]))
        schema = PlayerSeasonStatsCollectionSchema()
        return schema.dumps(self)


class SkatersSeasonStatsCollection(PlayerSeasonStatsCollection):
    def __init__(self, season):
        super().__init__(season)
        self.get_players_func = PlayerDm.get_skaters
        self.get_stats_func = SkaterSumStat.get_stat_tuples
        self.calc_stats_func = get_skaters_stats


class GoaliesSeasonStatsCollection(PlayerSeasonStatsCollection):
    def __init__(self, season):
        super().__init__(season)
        self.get_players_func = PlayerDm.get_goalies
        self.get_stats_func = GoalieSumStat.get_stat_tuples
        self.calc_stats_func = get_goalies_stats


class PlayerSeasonStatsCollectionSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    results = fields.Nested(PlayerSeasonStatsSchema, many=True)
