import MySQLdb as Db

from db_utils.players import get_players_with_no_team, update_player_teams
from db_utils.get_stats import get_team_info_from_skater_stats, get_team_info_from_goalie_stats
from data_models.player import Player


def main(db):
    """
    This script finds players with NULL in current_team_id column. It searches for games stats, gets team id from the
    last games and saves it to players table.
    """
    invalid_players = get_players_with_no_team(db)
    player_info_to_update = []
    for p in invalid_players:
        pid = p[0]
        pos = p[1]
        if pos == Player.GOALIE:
            team_info = get_team_info_from_goalie_stats(db, pid)
        else:
            team_info = get_team_info_from_skater_stats(db, pid)
        if len(team_info) > 0:
            # get team id from the last game
            player_info_to_update.append((team_info[-1][0], pid))

    if len(player_info_to_update) > 0:
        print(player_info_to_update)
        update_player_teams(db, player_info_to_update)


if __name__ == '__main__':
    db_conn = Db.connect('localhost', 'hockstats', 'hockstats', 'NHL_STATS', charset='utf8')
    try:
        main(db_conn)
    finally:
        db_conn.close()
