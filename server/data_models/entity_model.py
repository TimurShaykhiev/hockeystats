from data_models.model import Model


class EntityModel(Model):
    @classmethod
    def get_all(cls, db_conn):
        query = "SELECT * FROM {}".format(cls._table_name)
        return cls._get_all_from_db(db_conn, query)

    @classmethod
    def get_fields(cls, db_conn, columns):
        query = 'SELECT {} FROM {}'.format(', '.join(columns), cls._table_name)
        with db_conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
