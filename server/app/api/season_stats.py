from flask import Blueprint

from app.models.player_stats import SkatersSeasonStatsCollection
from app.models.season import Season
from .response_utils import response

season_stats_api = Blueprint('season_stats_api', __name__, url_prefix='/api/stats')


@season_stats_api.route('/skaters')
def skaters():
    season = Season.create()
    sk_stats = SkatersSeasonStatsCollection(season)
    return response(sk_stats.get_collection())
