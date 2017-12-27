from flask import Blueprint

from app.models.player_info import GoalieInfo
from app.models.season import Season
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_OLD_SEASON_STATS

goalie_api = Blueprint('goalie_api', __name__, url_prefix='/api/goalie')


@goalie_api.route('/<int:player_id>/stats')
def goalie_stats(player_id):
    season = Season.create()
    goalie_info = GoalieInfo(player_id, season)
    return response(goalie_info.get_info(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)
