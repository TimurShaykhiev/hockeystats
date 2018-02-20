from data_models.model import Model


class StatsModel(Model):
    @classmethod
    def get_player_stats_by_date(cls, db_conn, player_id, from_date, to_date):
        q = cls._create_query().select()
        q.where('player_id = %s AND date >= %s AND date < %s')
        return cls._get_columns_from_db(db_conn, q.query, (player_id, from_date, to_date))
