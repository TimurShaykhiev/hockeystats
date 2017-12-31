from flask import Blueprint

from app.models.all_teams import AllTeamsCollection
from .response_utils import response, CACHE_TYPE_SEASONS_DATA

teams_api = Blueprint('teams_api', __name__, url_prefix='/api/teams')


@teams_api.route('')
def team_stats():
    teams = AllTeamsCollection()
    return response(teams.get_collection(), CACHE_TYPE_SEASONS_DATA)
