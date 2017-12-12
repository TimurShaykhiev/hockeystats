from collections import namedtuple

from marshmallow import fields
from flask import current_app

from app.database import get_db
from data_models.player import Player as PlayerDm
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.player_trade import PlayerTrade
from .player import Player, PlayerSchema
from .season import SeasonSchema
from . import ModelSchema

PlayerInfo = namedtuple('PlayerInfo', ['name', 'tid', 'pos', 'trades'])
PlayerTradeInfo = namedtuple('PlayerTradeInfo', ['date', 'from_team', 'to_team'])


def _get_all_players_info(db, data_getter_func, check_trades):
    pl_list = data_getter_func(db, ['id', 'name', 'current_team_id', 'primary_pos'])
    # Convert to dict for quick search
    info = dict((pid, PlayerInfo(name, tid, pos, [])) for pid, name, tid, pos in pl_list)
    if check_trades:
        pl_trades_list = PlayerTrade.get_all(db, order_by=['date'])
        for trade in pl_trades_list:
            if trade.player_id in info:
                info[trade.player_id].trades.append(PlayerTradeInfo(trade.date, trade.from_team, trade.to_team))
    return info


def _create_player(pid, players, season):
    pl_info = players[pid]
    pl = Player()
    pl.id = pid
    pl.name = pl_info.name
    pl.position = pl_info.pos[0].upper()
    pl.team_id = pl_info.tid
    if pl.team_id is None:
        current_app.logger.warn('Player {} has no team id.'.format(pid))
    pl.update_team_id(season, pl_info.trades)
    return pl


class PlayerSeasonStats:
    def __init__(self, player, stats_dm):
        self.player = player
        self.stats_dm = stats_dm


class PlayerSeasonStatsSchema(ModelSchema):
    player = fields.Nested(PlayerSchema)
    stats = fields.Function(lambda obj: obj.stats_dm.to_tuple()[3:], attribute='stats_dm')


class PlayerSeasonStatsCollection:
    def __init__(self, season):
        self.season = season
        self.results = []
        self.get_players_func = None
        self.get_stats_func = None

    def get_collection(self):
        db = get_db()
        players = _get_all_players_info(db, self.get_players_func, not self.season.current)
        stats = self.get_stats_func(db, self.season.id, self.season.regular)
        for st in stats:
            pl = _create_player(st.player.id, players, self.season)
            self.results.append(PlayerSeasonStats(pl, st))
        schema = PlayerSeasonStatsCollectionSchema()
        return schema.dumps(self)


class SkatersSeasonStatsCollection(PlayerSeasonStatsCollection):
    def __init__(self, season):
        super().__init__(season)
        self.get_players_func = PlayerDm.get_skaters
        self.get_stats_func = SkaterSumStat.get_season_stats


class GoaliesSeasonStatsCollection(PlayerSeasonStatsCollection):
    def __init__(self, season):
        super().__init__(season)
        self.get_players_func = PlayerDm.get_goalies
        self.get_stats_func = GoalieSumStat.get_season_stats


class PlayerSeasonStatsCollectionSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    results = fields.Nested(PlayerSeasonStatsSchema, many=True)
