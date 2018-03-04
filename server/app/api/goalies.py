from flask import Blueprint

from app.models.all_players import AllGoaliesCollection
from app.models.season import Season
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_OLD_SEASON_STATS

goalies_api = Blueprint('goalies_api', __name__, url_prefix='/api/goalies')


@goalies_api.route('')
def goalies_all():
    season = Season.create()
    return response(AllGoaliesCollection(season).get_collection(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)
