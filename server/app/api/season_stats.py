from flask import Blueprint

from app.models.player_stats import SkatersSeasonStatsCollection, GoaliesSeasonStatsCollection
from app.models.team_stats import TeamsSeasonStatsCollection
from app.models.season_info import SeasonStatsCollection
from app.models.season import Season
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_OLD_SEASON_STATS,\
    CACHE_TYPE_SEASONS_DATA

season_stats_api = Blueprint('season_stats_api', __name__, url_prefix='/api/stats')


@season_stats_api.route('/skaters')
def skaters_season_stats():
    season = Season.create()
    sk_stats = SkatersSeasonStatsCollection(season)
    return response(sk_stats.get_collection(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@season_stats_api.route('/goalies')
def goalies_season_stats():
    season = Season.create()
    g_stats = GoaliesSeasonStatsCollection(season)
    return response(g_stats.get_collection(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@season_stats_api.route('/teams')
def teams_season_stats():
    season = Season.create()
    t_stats = TeamsSeasonStatsCollection(season)
    return response(t_stats.get_collection(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@season_stats_api.route('/seasons')
def seasons_stats():
    return response(SeasonStatsCollection().get_collection(), CACHE_TYPE_SEASONS_DATA)
