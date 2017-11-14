def get_team_info_from_skater_stats(db, pid):
    with db.cursor() as cur:
        cur.execute('SELECT team_id, date FROM skater_stats WHERE player_id = %s ORDER BY date', [pid])
        return cur.fetchall()


def get_team_info_from_goalie_stats(db, pid):
    with db.cursor() as cur:
        cur.execute('SELECT team_id, date FROM goalie_stats WHERE player_id = %s ORDER BY date', [pid])
        return cur.fetchall()
