import requests

from data_models.conference import Conference
from data_models.division import Division
from data_models.team import Team
from data_loaders import NHL_STATS_DOMAIN

TEAMS_URL = NHL_STATS_DOMAIN + '/api/v1/teams/{}'
CONFERENCES_URL = NHL_STATS_DOMAIN + '/api/v1/conferences/{}'
DIVISIONS_URL = NHL_STATS_DOMAIN + '/api/v1/divisions/{}'


def get_conferences():
    """
    Get NHL conferences data
    :return: List of Conference data models
    """
    conferences = []
    for confId in range(1, 8):
        c = requests.get(CONFERENCES_URL.format(confId)).json()
        conf_list = c.get('conferences')
        if conf_list is None or len(conf_list) == 0:
            continue
        conferences.append(Conference.from_json(conf_list[0]))
    return conferences


def get_divisions():
    """
    Get NHL divisions data
    :return: List of Division data models
    """
    divisions = []
    for divId in range(1, 19):
        d = requests.get(DIVISIONS_URL.format(divId)).json()
        div_list = d.get('divisions')
        if div_list is None or len(div_list) == 0:
            continue
        divisions.append(Division.from_json(div_list[0]))
    return divisions


def get_teams():
    """
    Get NHL teams data
    :return: List of Team data models
    """
    teams = []
    for teamId in range(1, 68):
        t = requests.get(TEAMS_URL.format(teamId)).json()
        team_list = t.get('teams')
        if team_list is None or len(team_list) == 0:
            continue
        teams.append(Team.from_json(team_list[0]))
    return teams
