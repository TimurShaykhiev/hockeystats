from db_utils import get_all_from_query_result
from data_models.conference import Conference


def get_all_conferences(db, active_only=True):
    with db.cursor() as cur:
        if active_only:
            cur.execute('SELECT * FROM conferences WHERE active = 1')
        else:
            cur.execute('SELECT * FROM conferences')
        return get_all_from_query_result(Conference, cur)
