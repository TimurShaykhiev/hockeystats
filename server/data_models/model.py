from abc import ABC, abstractmethod

from db_utils import get_one_from_query_result
from data_models.query import Query


class Model(ABC):
    _table_name = ''
    _primary_keys = ['id']

    @classmethod
    @abstractmethod
    def from_tuple(cls, fields):
        pass

    @classmethod
    def from_db(cls, db_conn, *query_params):
        q = cls._create_query()
        q.select().filter_by(cls._primary_keys)
        return cls._get_one_from_db(db_conn, q.query, query_params)

    @abstractmethod
    def to_tuple(self):
        pass

    @classmethod
    def get_filtered(cls, db_conn, filter_columns, query_params, columns=None, named_tuple_cls=None, order_by=None):
        """
        Get filtered results from DB.
        :param db_conn: DB connection object
        :param filter_columns: list of column names used in WHERE clause
        :param query_params: list of query parameters
        :param columns: list of column names to return
        :param named_tuple_cls: named tuple to returns
        :param order_by: list of column names to sort by
        :return: List of data models or tuples(named tuples)
        """
        q = cls._create_query().select(columns).filter_by(filter_columns)
        if order_by is not None:
            q.order_by(order_by)
        if columns is None:
            return cls._get_all_from_db(db_conn, q.query, query_params)
        return cls._get_columns_from_db(db_conn, q.query, query_params, named_tuple_cls)

    @classmethod
    def _create_query(cls):
        return Query(cls._table_name)

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

    @classmethod
    def _get_columns_from_db(cls, db_conn, query, query_params=None, named_tuple_cls=None):
        """
         Return all query results as a list of tuples(or named tuples if passed).
         """
        with db_conn.cursor() as cur:
            cur.execute(query, query_params)
            if named_tuple_cls is not None:
                return [named_tuple_cls(*i) for i in cur.fetchall()]
            return cur.fetchall()
