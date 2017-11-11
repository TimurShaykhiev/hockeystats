from db_utils import get_all_from_query_result
from data_models.team import Team


def get_all_teams(db, active_only=True):
    with db.cursor() as cur:
        if active_only:
            cur.execute('SELECT * FROM teams WHERE active = 1 AND division_id IS NOT NULL')
        else:
            cur.execute('SELECT * FROM teams')
        return get_all_from_query_result(Team, cur)


def get_teams_by_division(db, div_id):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM teams WHERE division_id = %s', [div_id])
        return get_all_from_query_result(Team, cur)
