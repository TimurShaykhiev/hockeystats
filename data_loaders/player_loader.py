import requests

from data_models.player import Player
from data_loaders import NHL_STATS_DOMAIN


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
        players.append(Player.from_json(people_list[0]))
    return players
