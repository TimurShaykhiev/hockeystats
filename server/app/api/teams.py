from flask import Blueprint

from app.models.all_teams import AllTeamsCollection
from app.models.standings import Standings
from app.models.play_off import PlayOff
from app.models.season import Season
from .response_utils import response, CACHE_TYPE_SEASONS_DATA, CACHE_TYPE_OLD_SEASON_STATS, \
    CACHE_TYPE_CURRENT_SEASON_STATS

teams_api = Blueprint('teams_api', __name__, url_prefix='/api/teams')


@teams_api.route('')
def teams_all():
    season = Season.create()
    return response(AllTeamsCollection(season).get_collection(), CACHE_TYPE_SEASONS_DATA)


@teams_api.route('/standings')
def teams_standings():
    season = Season.create()
    return response(Standings(season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@teams_api.route('/play-off')
def teams_play_off():
    season = Season.create()
    return response(PlayOff(season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)
