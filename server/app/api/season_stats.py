from flask import Blueprint

from app.models.player_stats import SkatersSeasonStatsCollection
from app.models.season import Season
from .error_codes import API_ERRORS
from .response_utils import response, error

season_stats_api = Blueprint('season_stats_api', __name__, url_prefix='/api/stats')


@season_stats_api.route('/skaters')
def skaters():
    season = Season.create()
    if season is None:
        return error(404, API_ERRORS['SEASON_NOT_FOUND'])
    sk_stats = SkatersSeasonStatsCollection(season)
    return response(sk_stats.get_collection())
