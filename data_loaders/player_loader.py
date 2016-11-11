import requests
import logging as LOG

from data_models.player import Player
from data_loaders import NHL_STATS_DOMAIN


def create_player_link(player_id):
    return '/api/v1/people/' + str(player_id)


def get_players(links):
    """
    Get NHL players data
    :type links: player URLS list
    :return: List of Player data models
    """
    players = []
    for link in links:
        p = requests.get(NHL_STATS_DOMAIN + link).json()
        people_list = p.get('people')
        if people_list is None or len(people_list) == 0:
            continue
        LOG.info('Get player from %s', link)
        players.append(Player.from_json(people_list[0]))
    return players
