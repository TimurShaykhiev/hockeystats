from marshmallow import fields
from flask import current_app

from database import get_db
from db_utils.players import get_all_skaters_short_info, get_all_goalies_short_info
from db_utils.get_sum_stats import get_all_skaters_sum_stats, get_all_goalies_sum_stats
from .player import Player, PlayerSchema
from .season import SeasonSchema
from models import ModelSchema


def _get_all_players_info(db, data_getter_func):
    pl_list = data_getter_func(db)
    # Convert to dict for quick search
    return dict((pid, (name, tid, pos)) for pid, name, tid, pos in pl_list)


def _create_player(pid, players):
    pl = Player()
    pl.id = pid
    pl.name = players[pid][0]
    pl.position = players[pid][2][0].upper()
    pl.team_id = players[pid][1]
    if pl.team_id is None:
        current_app.logger.warn('Player {} has no team id.'.format(pid))
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
        players = _get_all_players_info(db, self.get_players_func)
        stats = self.get_stats_func(db, self.season.id, self.season.regular)
        for st in stats:
            pl = _create_player(st.player.id, players)
            self.results.append(PlayerSeasonStats(pl, st))
        schema = PlayerSeasonStatsCollectionSchema()
        return schema.dumps(self)


class SkatersSeasonStatsCollection(PlayerSeasonStatsCollection):
    def __init__(self, season):
        super().__init__(season)
        self.get_players_func = get_all_skaters_short_info
        self.get_stats_func = get_all_skaters_sum_stats


class GoaliesSeasonStatsCollection(PlayerSeasonStatsCollection):
    def __init__(self, season):
        super().__init__(season)
        self.get_players_func = get_all_goalies_short_info
        self.get_stats_func = get_all_goalies_sum_stats


class PlayerSeasonStatsCollectionSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    results = fields.Nested(PlayerSeasonStatsSchema, many=True)
