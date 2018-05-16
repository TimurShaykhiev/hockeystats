import requests

from logger import get_loader_logger
from data_models.player import Player
from data_loaders import NHL_STATS_DOMAIN

LOG = get_loader_logger()


def create_player_link(player_id, lang=None):
    link = '/api/v1/people/' + str(player_id)
    if lang is not None:
        link += '?site={}_nhl'.format(lang)
    return link


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
