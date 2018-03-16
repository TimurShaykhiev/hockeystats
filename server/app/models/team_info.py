from marshmallow import fields

from app.database import get_db
from data_models.team_sum_stat import TeamSumStat
from data_models.game import Game
from data_models.player import Player as PlayerDm
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from statistics.skater_season import get_skaters_stats
from statistics.goalie_season import get_goalies_stats
from statistics.team_season import get_team_ext_stats, get_teams_stats
from statistics.games import get_game_stats, get_team_vs_team_stats
from .team import Team, TeamSchema
from .season import Season, SeasonSchema, get_all_seasons
from .season_stats import SeasonStats, SeasonStatsSchema, PlayerSeasonStats, PlayerSeasonStatsSchema
from .player import Player, PlayerInfo
from .utils import get_team_players
from . import ModelSchema, StatValue


def _get_team_full_stats(db, season, tid):
    stats = TeamSumStat.get_stat_tuples(db, season.id, season.regular)
    games = Game.get_team_games(db, tid, season.start, season.end, season.regular)
    return get_team_ext_stats(tid, stats, games)


class TeamInfo:
    def __init__(self, team_id, season):
        self.season = season
        self.team = Team.create(team_id)
        self.stats = []

    def get_info(self):
        db = get_db()
        self.stats = _get_team_full_stats(db, self.season, self.team.id)
        schema = _TeamInfoSchema()
        return schema.dumps(self)


class _TeamInfoSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    team = fields.Nested(TeamSchema)
    stats = fields.List(StatValue())


class TeamAllSeasonStatsCollection:
    def __init__(self, team_id):
        self.team = Team.create(team_id)
        self.results = []

    def get_collection(self):
        db = get_db()
        all_seasons = dict((s.id, s) for s in get_all_seasons(db))
        stats_from_db = TeamSumStat.get_all_seasons_stat_tuples(db, self.team.id, True)
        stats = get_teams_stats(stats_from_db)
        for st in stats:
            season = Season()
            season.set_from_data_model(all_seasons[st[1]])
            self.results.append(SeasonStats(season, st[3:]))
        schema = _TeamAllSeasonStatsCollectionSchema()
        return schema.dumps(self)


class _TeamAllSeasonStatsCollectionSchema(ModelSchema):
    team = fields.Nested(TeamSchema)
    results = fields.Nested(SeasonStatsSchema, many=True)


class TeamPlayersSeasonStatsCollection:
    def __init__(self, team_id, season):
        self.team = Team.create(team_id)
        self.season = season
        self.skaters = []
        self.goalies = []

    def get_collection(self):
        db = get_db()
        pl_ids = get_team_players(db, self.team.id, self.season)
        pl_list = PlayerDm.get_by_ids(db, pl_ids, ['id', 'name', 'primary_pos'])
        pl_info = dict((pid, PlayerInfo(name, self.team.id, pos, [])) for pid, name, pos in pl_list)

        sk_stats_from_db = SkaterSumStat.get_group_stat_tuples(db, pl_ids, self.season.id, self.season.regular)
        sk_stats = get_skaters_stats(sk_stats_from_db)
        for st in sk_stats:
            pl = Player.create(st[0], self.season, pl_info)
            self.skaters.append(PlayerSeasonStats(pl, st[3:]))

        g_stats_from_db = GoalieSumStat.get_group_stat_tuples(db, pl_ids, self.season.id, self.season.regular)
        g_stats = get_goalies_stats(g_stats_from_db)
        for st in g_stats:
            pl = Player.create(st[0], self.season, pl_info)
            self.goalies.append(PlayerSeasonStats(pl, st[3:]))

        schema = _TeamPlayersSeasonStatsCollectionSchema()
        return schema.dumps(self)


class _TeamPlayersSeasonStatsCollectionSchema(ModelSchema):
    team = fields.Nested(TeamSchema)
    season = fields.Nested(SeasonSchema)
    skaters = fields.Nested(PlayerSeasonStatsSchema, many=True)
    goalies = fields.Nested(PlayerSeasonStatsSchema, many=True)


class TeamCompare:
    def __init__(self, team1_id, team2_id, season):
        self.season = season
        self.team1 = Team.create(team1_id)
        self.team2 = Team.create(team2_id)
        self.stats1 = []
        self.stats2 = []
        self.vs = []
        self.games = []

    def get_data(self):
        db = get_db()
        self.stats1 = _get_team_full_stats(db, self.season, self.team1.id)
        self.stats2 = _get_team_full_stats(db, self.season, self.team2.id)

        games = Game.get_team_vs_team_games(db, self.team1.id, self.team2.id, self.season.regular)
        self.vs = get_team_vs_team_stats(games, self.team1.id, self.team2.id, self.season.start, self.season.end)
        self.games = get_game_stats(games)

        schema = _TeamCompareSchema()
        return schema.dumps(self)


class _GameStatsSchema(ModelSchema):
    date = fields.Date()
    stats = fields.List(StatValue())


class _TeamCompareSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    team1 = fields.Nested(TeamSchema)
    team2 = fields.Nested(TeamSchema)
    stats1 = fields.List(StatValue())
    stats2 = fields.List(StatValue())
    vs = fields.List(StatValue())
    games = fields.Nested(_GameStatsSchema, many=True)
