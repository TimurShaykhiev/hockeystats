import MySQLdb as Db

from data_models.player import Player
from data_models.translation import prepare_player_name_translations
from data_loaders.player_loader import get_players, create_player_link
from db_utils.players import add_translations


def main(db):
    """
    This script add name translations for existed players.
    """
    players = Player.get_all(db, ['id'])
    links = [create_player_link(p[0], 'ru') for p in players]
    pl_name_translations = prepare_player_name_translations(get_players(links))
    num = add_translations(db_conn, pl_name_translations)
    print('{} new player name translations added'.format(num if num else 0))


if __name__ == '__main__':
    db_conn = Db.connect(host='localhost', user='hockstats', password='hockstats', database='NHL_STATS', charset='utf8')
    try:
        main(db_conn)
    finally:
        db_conn.close()
