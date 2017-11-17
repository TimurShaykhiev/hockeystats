from data_models.model import Model


class EntityModel(Model):
    @classmethod
    def get_all(cls, db_conn):
        query = "SELECT * FROM {}".format(cls._table_name)
        return cls._get_all_from_db(db_conn, query)
