from data_models.model import Model


class SumStatsModel(Model):
    @classmethod
    def get_season_stats(cls, db_conn, season_id, regular):
        query = 'SELECT * FROM {} WHERE season_id = %s AND is_regular = %s'.format(cls._table_name)
        return cls._get_all_from_db(db_conn, query, (season_id, regular))
