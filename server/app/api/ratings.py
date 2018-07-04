from flask import Blueprint

from app.models.ratings import ScorerDuos
from app.models.season import Season
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_OLD_SEASON_STATS

ratings_api = Blueprint('ratings_api', __name__, url_prefix='/api/ratings')


@ratings_api.route('/scorer-duos')
def ratings_scorer_duos():
    season = Season.create()
    return response(ScorerDuos(season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)
