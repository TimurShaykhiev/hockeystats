from db_utils import get_all_from_query_result, get_one_from_query_result
from data_models.season import Season


def get_all_seasons(db):
    cur = db.cursor()
    cur.execute('SELECT * FROM seasons')
    return get_all_from_query_result(Season, cur)


def get_current_season(db):
    cur = db.cursor()
    cur.execute('SELECT * FROM seasons WHERE current = 1')
    return get_one_from_query_result(Season, cur)


def get_season_by_date(db, date):
    cur = db.cursor()
    cur.execute('SELECT * FROM seasons WHERE end >= %s AND start <= %s', [date, date])
    return get_one_from_query_result(Season, cur)
