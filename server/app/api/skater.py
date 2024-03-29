from flask import Blueprint

from app.models.player_info import SkaterInfo, SkaterAllSeasonStatsCollection, SkaterCompare
from app.models.season import Season, SkaterSeasonCollection
from app.models.player_charts import SkaterPointsProgressChart, PlayerPenaltiesChart
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_OLD_SEASON_STATS, \
    CACHE_TYPE_SEASONS_DATA

skater_api = Blueprint('skater_api', __name__, url_prefix='/api/skater')


@skater_api.route('/<int:player_id>/stats')
def skater_stats(player_id):
    season = Season.create()
    skater_info = SkaterInfo(player_id, season)
    return response(skater_info.get_info(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@skater_api.route('/<int:player_id>/seasons')
def skater_seasons(player_id):
    return response(SkaterSeasonCollection(player_id).get_collection(), CACHE_TYPE_SEASONS_DATA)


@skater_api.route('/<int:player_id>/all-stats')
def skater_all_stats(player_id):
    return response(SkaterAllSeasonStatsCollection(player_id).get_collection(), CACHE_TYPE_CURRENT_SEASON_STATS)


@skater_api.route('/<int:player1_id>/compare/<int:player2_id>')
def skater_compare(player1_id, player2_id):
    season = Season.create()
    return response(SkaterCompare(player1_id, player2_id, season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@skater_api.route('/<int:player_id>/charts/points-progress')
def points_progress_chart(player_id):
    season = Season.create()
    return response(SkaterPointsProgressChart(player_id, season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@skater_api.route('/<int:player_id>/charts/penalties')
def penalties_chart(player_id):
    season = Season.create()
    return response(PlayerPenaltiesChart(player_id, season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)
