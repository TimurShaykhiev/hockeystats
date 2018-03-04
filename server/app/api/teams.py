from flask import Blueprint

from app.models.all_teams import AllTeamsCollection
from app.models.season import Season
from .response_utils import response, CACHE_TYPE_SEASONS_DATA

teams_api = Blueprint('teams_api', __name__, url_prefix='/api/teams')


@teams_api.route('')
def teams_all():
    season = Season.create()
    return response(AllTeamsCollection(season).get_collection(), CACHE_TYPE_SEASONS_DATA)
