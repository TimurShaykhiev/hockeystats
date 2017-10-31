from flask import Blueprint

from app.models.season import Season, SeasonSchema
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS

season_api = Blueprint('season_api', __name__, url_prefix='/api/season')


@season_api.route('/current')
def current_season():
    season = Season.create_current()
    return response(SeasonSchema().dumps(season), CACHE_TYPE_CURRENT_SEASON_STATS)
