import MySQLdb as Db
import numpy as np
import sys

from config.config import get_custom_config
from data_models.game import Game
from forecast.prepare_games_data import get_games_data

DEFAULT_DATASET_NAME = 'games'


def main(db, filename=DEFAULT_DATASET_NAME):
    games = Game.get_all_sorted(db)
    x, y = get_games_data(games)

    # np.savetxt(sys.stdout, x, '%5.2f')
    # print(y)

    np.save('./dataset/{}_x'.format(filename), x)
    np.save('./dataset/{}_y'.format(filename), y)


if __name__ == '__main__':
    config = get_custom_config()
    db_conn = Db.connect(host=config.DB_URL, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME,
                         charset='utf8')
    try:
        main(db_conn, 'games_10_3')
    finally:
        db_conn.close()
