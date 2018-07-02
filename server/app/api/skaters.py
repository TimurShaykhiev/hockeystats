from flask import Blueprint

from app.models.all_players import AllSkatersCollection
from app.models.skaters_charts import SkaterPenaltyDrewByChart
from app.models.season import Season
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_OLD_SEASON_STATS

skaters_api = Blueprint('skaters_api', __name__, url_prefix='/api/skaters')


@skaters_api.route('')
def skaters_all():
    season = Season.create()
    return response(AllSkatersCollection(season).get_collection(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@skaters_api.route('/charts/penalty-drew-by')
def skaters_penalty_drew_by():
    season = Season.create()
    return response(SkaterPenaltyDrewByChart(season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)
