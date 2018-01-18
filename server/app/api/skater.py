from flask import Blueprint

from app.models.player_info import SkaterInfo, SkaterAllSeasonStatsCollection
from app.models.season import Season, SkaterSeasonCollection
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
