from db_utils import get_all_from_query_result
from data_models.player import Player


def get_all_players(db, active_only=True):
    with db.cursor() as cur:
        if active_only:
            cur.execute('SELECT * FROM players WHERE current_team_id IS NOT NULL')
        else:
            cur.execute('SELECT * FROM players')
        return get_all_from_query_result(Player, cur)


def get_players_by_team(db, team_id):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM players WHERE current_team_id = %s', [team_id])
        return get_all_from_query_result(Player, cur)


def get_player_team_info(db):
    with db.cursor() as cur:
        cur.execute('SELECT id, current_team_id FROM players')
        return cur.fetchall()


def get_all_skaters_short_info(db):
    with db.cursor() as cur:
        cur.execute('SELECT id, name, current_team_id, primary_pos FROM players WHERE primary_pos != \'goalie\'')
        return cur.fetchall()


def get_all_goalies_short_info(db):
    with db.cursor() as cur:
        cur.execute('SELECT id, name, current_team_id, primary_pos FROM players WHERE primary_pos = \'goalie\'')
        return cur.fetchall()


def add_players(db, players):
    with db as cur:
        num = cur.executemany('INSERT INTO players VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                              [p.to_tuple() for p in players])
    cur.close()
    return num


def update_player_teams(db, player_info):
    with db as cur:
        num = cur.executemany('UPDATE players SET current_team_id = %s WHERE id = %s', player_info)
    cur.close()
    return num
