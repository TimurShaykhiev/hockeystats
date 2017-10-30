from flask import Blueprint

from app.models.season import Season, SeasonSchema
from .response_utils import response

season_api = Blueprint('season_api', __name__, url_prefix='/api/season')


@season_api.route('/current')
def current_season():
    season = Season.create_current()
    return response(SeasonSchema().dumps(season))
