from flask import Blueprint

from app.models.team_info import TeamInfo
from app.models.season import Season
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_OLD_SEASON_STATS

team_api = Blueprint('team_api', __name__, url_prefix='/api/team')


@team_api.route('/<int:team_id>/stats')
def team_stats(team_id):
    season = Season.create()
    team_info = TeamInfo(team_id, season)
    return response(team_info.get_info(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)
