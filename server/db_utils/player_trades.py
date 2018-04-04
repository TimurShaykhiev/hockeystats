def add_player_trades(db, trades):
    with db as cur:
        num = cur.executemany('INSERT INTO player_trades (player_id, date, from_team_id, to_team_id) '
                              'VALUES (%s, %s, %s, %s)', [t.to_tuple() for t in trades])
    cur.close()
    return num
