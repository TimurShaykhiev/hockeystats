from db_utils import get_all_from_query_result, get_one_from_query_result
from data_models.season import Season


def get_season_by_date(db, date):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM seasons WHERE end >= %s AND start <= %s', [date, date])
        return get_one_from_query_result(Season, cur)


def get_2_last_seasons(db):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM seasons ORDER BY start DESC LIMIT 2')
        return get_all_from_query_result(Season, cur)


def set_new_current_season(db_cur, current_sid, new_current_sid):
    db_cur.execute('UPDATE seasons SET current = 0 WHERE id = %s', [current_sid])
    db_cur.execute('UPDATE seasons SET current = 1, status = \'regular\' WHERE id = %s', [new_current_sid])


def update_season_status(db_cur, sid, status):
    db_cur.execute('UPDATE seasons SET status = %s WHERE id = %s', (status, sid))
