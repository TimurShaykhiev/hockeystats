def add_player_trades(db, trades):
    with db as cur:
        num = cur.executemany('INSERT INTO player_trades VALUES (%s, %s, %s, %s)', [t.to_tuple() for t in trades])
    cur.close()
    return num
