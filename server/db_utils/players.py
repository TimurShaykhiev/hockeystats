def add_players(db, players):
    with db as cur:
        num = cur.executemany('INSERT INTO players (id, name, birth_date, birth_city, birth_state, birth_country, '
                              'nationality, height, weight, shoots_catches, primary_pos, current_team_id) '
                              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                              [p.to_tuple() for p in players])
    cur.close()
    return num


def add_translations(db, translations):
    with db as cur:
        num = cur.executemany('INSERT INTO translations (resource_type, resource_id, ru) '
                              'VALUES (%s, %s, %s)', translations)
    cur.close()
    return num


def update_player_teams(db, player_info):
    with db as cur:
        num = cur.executemany('UPDATE players SET current_team_id = %s WHERE id = %s', player_info)
    cur.close()
    return num


def get_players_with_no_team(db):
    with db.cursor() as cur:
        cur.execute('SELECT id, primary_pos FROM players WHERE current_team_id IS NULL')
        return cur.fetchall()
