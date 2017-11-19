from data_models.model import Model


class EntityModel(Model):
    @classmethod
    def get_all(cls, db_conn, columns=None, named_tuple_cls=None):
        q = cls._create_query().select(columns)
        if columns is None:
            return cls._get_all_from_db(db_conn, q.query)
        return cls._get_columns_from_db(db_conn, q.query, named_tuple_cls=named_tuple_cls)
