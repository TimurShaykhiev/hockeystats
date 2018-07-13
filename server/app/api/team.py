from flask import Blueprint

from app.models.team_info import TeamInfo, TeamAllSeasonStatsCollection, TeamPlayersSeasonStatsCollection, TeamCompare
from app.models.season import Season, TeamSeasonCollection
from app.models.team_charts import TeamPointsProgressChart, TeamPenaltiesChart
from .response_utils import response, CACHE_TYPE_CURRENT_SEASON_STATS, CACHE_TYPE_OLD_SEASON_STATS, \
    CACHE_TYPE_SEASONS_DATA

team_api = Blueprint('team_api', __name__, url_prefix='/api/team')


@team_api.route('/<int:team_id>/stats')
def team_stats(team_id):
    season = Season.create()
    team_info = TeamInfo(team_id, season)
    return response(team_info.get_info(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@team_api.route('/<int:team_id>/seasons')
def team_seasons(team_id):
    return response(TeamSeasonCollection(team_id).get_collection(), CACHE_TYPE_SEASONS_DATA)


@team_api.route('/<int:team_id>/all-stats')
def team_all_stats(team_id):
    return response(TeamAllSeasonStatsCollection(team_id).get_collection(), CACHE_TYPE_CURRENT_SEASON_STATS)


@team_api.route('/<int:team_id>/players/stats')
def team_players_stats(team_id):
    season = Season.create()
    return response(TeamPlayersSeasonStatsCollection(team_id, season).get_collection(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@team_api.route('/<int:team1_id>/compare/<int:team2_id>')
def team_compare(team1_id, team2_id):
    season = Season.create()
    return response(TeamCompare(team1_id, team2_id, season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@team_api.route('/<int:team_id>/charts/points-progress')
def points_progress_chart(team_id):
    season = Season.create()
    return response(TeamPointsProgressChart(team_id, season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)


@team_api.route('/<int:team_id>/charts/penalties')
def penalties_chart(team_id):
    season = Season.create()
    return response(TeamPenaltiesChart(team_id, season).get_data(),
                    CACHE_TYPE_CURRENT_SEASON_STATS if season.current else CACHE_TYPE_OLD_SEASON_STATS)
