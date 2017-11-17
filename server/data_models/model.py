from db_utils import get_one_from_query_result


class Model:
    _table_name = ''
    _query_get_by_id = ''

    @classmethod
    def from_tuple(cls, fields):
        raise NotImplementedError()

    @classmethod
    def from_db(cls, db_conn, *query_params):
        return cls._get_one_from_db(db_conn, cls._query_get_by_id, query_params)

    def to_tuple(self):
        raise NotImplementedError()

    @classmethod
    def _get_all_from_db(cls, db_conn, query, query_params=None):
        """
         Return all query results as a list of data models.
         This utility function is for 'SELECT * FROM' queries only.
         """
        with db_conn.cursor() as cur:
            cur.execute(query, query_params)
            return [cls.from_tuple(row) for row in cur.fetchall()]

    @classmethod
    def _get_one_from_db(cls, db_conn, query, query_params=None):
        """
         Return first query result as data model or None if nothing is found.
         This utility function is for 'SELECT * FROM' queries only.
         """
        with db_conn.cursor() as cur:
            cur.execute(query, query_params)
            return get_one_from_query_result(cls, cur)
