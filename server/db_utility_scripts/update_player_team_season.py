from collections import namedtuple

import MySQLdb as Db

from data_models.season import Season
from data_models.player import Player
from data_models.player_trade import PlayerTrade
from db_utils.add_player_team_season import add_player_team_season

SEASON_ID = 4

PlayerInfo = namedtuple('PlayerInfo', ['tid', 'trades'])


def main(db):
    """
    This script updates player_team_season table for finished season. This is an utility table to find
     what team player played for in the season.
    """
    season = Season.from_db(db, SEASON_ID)
    pl_list = Player.get_all_players_for_season(db, SEASON_ID, ['id', 'current_team_id'])
    # Convert to dict for quick search
    info = dict((pid, PlayerInfo(tid, [])) for pid, tid in pl_list)
    pl_trades_list = PlayerTrade.get_all(db, order_by=['date'])
    for trade in pl_trades_list:
        if trade.player_id in info:
            info[trade.player_id].trades.append(trade)

    to_add = []
    for pid in info:
        pl = info[pid]
        new_tid = pl.tid
        if len(pl.trades) > 0:
            for tr in pl.trades:
                if tr.date < season.end:
                    new_tid = tr.to_team
                if tr.date >= season.end:
                    new_tid = tr.from_team
                    break
        to_add.append((pid, SEASON_ID, new_tid))

    print('Adding {} records to player_team_season'.format(len(to_add)))
    with db as cur:
        if len(to_add) > 0:
            num = add_player_team_season(cur, to_add)
            print('{} rows updated in player_team_season'.format(num if num else 0))
    print('DB updates commit')
    cur.close()


if __name__ == '__main__':
    db_conn = Db.connect('localhost', 'hockstats', 'hockstats', 'NHL_STATS', charset='utf8')
    try:
        main(db_conn)
    finally:
        db_conn.close()
