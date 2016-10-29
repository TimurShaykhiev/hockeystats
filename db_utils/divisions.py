from db_utils import get_all_from_query_result
from data_models.division import Division


def get_all_divisions(db, active_only=True):
    cur = db.cursor()
    if active_only:
        cur.execute('SELECT * FROM divisions WHERE active = 1 AND conference_id IS NOT NULL')
    else:
        cur.execute('SELECT * FROM divisions')
    return get_all_from_query_result(Division, cur)


def get_divisions_by_conference(db, conf_id):
    cur = db.cursor()
    cur.execute('SELECT * FROM divisions WHERE conference_id = %s', [conf_id])
    return get_all_from_query_result(Division, cur)
