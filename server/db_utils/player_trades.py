from db_utils import get_all_from_query_result
from data_models.player_trade import PlayerTrade


def add_player_trades(db, trades):
    with db as cur:
        num = cur.executemany('INSERT INTO player_trades VALUES (%s, %s, %s, %s)', [t.to_tuple() for t in trades])
    cur.close()
    return num


def get_all_player_trades(db):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM player_trades')
        return get_all_from_query_result(PlayerTrade, cur)
