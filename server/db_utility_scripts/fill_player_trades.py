import MySQLdb as Db

from db_utils.get_stats import get_team_info_from_skater_stats, get_team_info_from_goalie_stats
from db_utils.player_trades import add_player_trades
from data_models.player import Player
from data_models.player_trade import PlayerTrade


def main(db):
    """
    This script finds player trades(team id is changed) and saves them to player_trades table.
    """
    players = Player.get_fields(db, ['id', 'current_team_id', 'primary_pos'])
    player_trades = []
    for p in players:
        pid, current_tid, pos = p
        if pos == Player.GOALIE:
            team_info = get_team_info_from_goalie_stats(db, pid)
        else:
            team_info = get_team_info_from_skater_stats(db, pid)
        tid = team_info[0][0]
        for i_tid, i_date in team_info:
            if i_tid != tid:
                # team id is changed
                player_trades.append(PlayerTrade(pid, i_date, tid, i_tid))
                tid = i_tid

    if len(player_trades) > 0:
        res = add_player_trades(db, player_trades)
        print('{} player trades added'.format(res))


if __name__ == '__main__':
    db_conn = Db.connect('localhost', 'hockstats', 'hockstats', 'NHL_STATS')
    try:
        main(db_conn)
    finally:
        db_conn.close()
