def add_player_team_season(db_cur, pts_records):
    num = db_cur.executemany('INSERT INTO player_team_season (player_id, season_id, team_id) VALUES (%s, %s, %s)',
                             pts_records)
    return num
