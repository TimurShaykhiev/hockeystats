from data_models.model import Model


class SumStatsModel(Model):
    _object_id_field = ''

    @classmethod
    def get_season_stats(cls, db_conn, season_id, regular):
        q = cls._create_query().select().filter_by(['season_id', 'is_regular'])
        return cls._get_all_from_db(db_conn, q.query, (season_id, regular))

    @classmethod
    def get_stat_tuples(cls, db_conn, season_id, regular):
        q = cls._create_query().select().filter_by(['season_id', 'is_regular'])
        return cls._get_columns_from_db(db_conn, q.query, (season_id, regular))

    @classmethod
    def get_group_stat_tuples(cls, db_conn, id_array, season_id, regular):
        q = cls._create_query().select()
        q.where('{} IN ({}) AND season_id = %s AND is_regular = %s'.format(cls._object_id_field,
                                                                           ','.join(['%s'] * len(id_array))))
        id_array.extend((season_id, regular))  # just to avoid list copy
        return cls._get_columns_from_db(db_conn, q.query, id_array)

    @classmethod
    def get_all_seasons_stat_tuples(cls, db_conn, obj_id, regular_only=False):
        q = cls._create_query().select()
        if regular_only:
            q.filter_by([cls._object_id_field, 'is_regular'])
            query_params = (obj_id, True)
        else:
            q.filter_by([cls._object_id_field])
            query_params = (obj_id,)
        return cls._get_columns_from_db(db_conn, q.query, query_params)
