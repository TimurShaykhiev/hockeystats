from flask import Blueprint

from app.models.season import Season, SeasonSchema, SeasonCollection
from app.models.season_info import SeasonInfo
from app.models.season_charts import SeasonPenaltiesChart
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_SEASONS_DATA,\
    CACHE_TYPE_OLD_SEASON_STATS

season_api = Blueprint('season_api', __name__, url_prefix='/api/season')


@season_api.route('/current')
def current_season():
    season = Season.create_current()
    return response(SeasonSchema().dumps(season), CACHE_TYPE_CURRENT_SEASON_STATS)


@season_api.route('/all')
def all_seasons():
    seasons = SeasonCollection()
    return response(seasons.get_collection(), CACHE_TYPE_SEASONS_DATA)


@season_api.route('/stats')
def season_stats():
    season = Season.create()
    return response(SeasonInfo(season).get_data(), CACHE_TYPE_OLD_SEASON_STATS)


@season_api.route('/charts/penalties')
def penalties_chart():
    season = Season.create()
    return response(SeasonPenaltiesChart(season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)
