from flask import Blueprint

from app.models.player_info import GoalieInfo, GoalieAllSeasonStatsCollection, GoalieCompare
from app.models.season import Season, GoalieSeasonCollection
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_OLD_SEASON_STATS, \
    CACHE_TYPE_SEASONS_DATA

goalie_api = Blueprint('goalie_api', __name__, url_prefix='/api/goalie')


@goalie_api.route('/<int:player_id>/stats')
def goalie_stats(player_id):
    season = Season.create()
    goalie_info = GoalieInfo(player_id, season)
    return response(goalie_info.get_info(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@goalie_api.route('/<int:player_id>/seasons')
def goalie_seasons(player_id):
    return response(GoalieSeasonCollection(player_id).get_collection(), CACHE_TYPE_SEASONS_DATA)


@goalie_api.route('/<int:player1_id>/compare/<int:player2_id>')
def goalie_compare(player1_id, player2_id):
    season = Season.create()
    return response(GoalieCompare(player1_id, player2_id, season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@goalie_api.route('/<int:player_id>/all-stats')
def goalie_all_stats(player_id):
    return response(GoalieAllSeasonStatsCollection(player_id).get_collection(), CACHE_TYPE_CURRENT_SEASON_STATS)
