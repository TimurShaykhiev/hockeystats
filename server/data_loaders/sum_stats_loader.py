import requests
# import json

from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.team_sum_stat import TeamSumStat

URL = 'http://www.nhl.com/stats/rest/{}?isAggregate=false&reportType={}&isGame=false&reportName={}' \
      '&cayenneExp=gameTypeId={}%20and%20seasonId%3E={}%20and%20seasonId%3C={}'

SKATER = 0
GOALIE = 1
TEAM = 3

GAME_TYPE_REGULAR = 2
GAME_TYPE_PLAYOFF = 3

REST_RESOURCE = {
    SKATER: 'skaters',
    GOALIE: 'goalies',
    TEAM: 'team',
}

REPORT_TYPE = {
    SKATER: 'basic',
    GOALIE: 'goalie_basic',
    TEAM: 'basic',
}

REPORT_NAME = {
    SKATER: 'skatersummary',
    GOALIE: 'goaliesummary',
    TEAM: 'teamsummary',
}


def _create_url(resource, season, regular):
    return URL.format(REST_RESOURCE[resource], REPORT_TYPE[resource], REPORT_NAME[resource],
                      GAME_TYPE_REGULAR if regular else GAME_TYPE_PLAYOFF, season, season)


# def _to_file(obj, filename):
#     with open(filename, 'w') as outfile:
#         json.dump(obj, outfile)
#
#
# def _from_file(filename):
#     with open(filename, 'r') as outfile:
#         return json.load(outfile)


def get_skater_sum_stats(season, regular):
    result = requests.get(_create_url(SKATER, season, regular)).json()
    sum_stats = []
    for d in result['data']:
        sum_stats.append(SkaterSumStat.from_json(d))
    return sum_stats


def get_goalie_sum_stats(season, regular):
    result = requests.get(_create_url(GOALIE, season, regular)).json()
    sum_stats = []
    for d in result['data']:
        sum_stats.append(GoalieSumStat.from_json(d))
    return sum_stats


def get_team_sum_stats(season, regular):
    result = requests.get(_create_url(TEAM, season, regular)).json()
    sum_stats = []
    for d in result['data']:
        sum_stats.append(TeamSumStat.from_json(d))
    return sum_stats
