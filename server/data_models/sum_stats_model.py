from data_models.model import Model


class SumStatsModel(Model):
    @classmethod
    def get_season_stats(cls, db_conn, season_id, regular):
        q = cls._create_query().select().filter_by(['season_id', 'is_regular'])
        return cls._get_all_from_db(db_conn, q.query, (season_id, regular))

    @classmethod
    def get_stat_tuples(cls, db_conn, season_id, regular):
        q = cls._create_query().select().filter_by(['season_id', 'is_regular'])
        return cls._get_columns_from_db(db_conn, q.query, (season_id, regular))
