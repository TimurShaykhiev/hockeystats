from data_models.model import Model


class StatsModel(Model):
    @classmethod
    def get_player_stats_by_date(cls, db_conn, player_id, from_date, to_date):
        q = cls._create_query().select()
        q.where('player_id = %s AND date >= %s AND date < %s')
        return cls._get_columns_from_db(db_conn, q.query, (player_id, from_date, to_date))

    @classmethod
    def get_player_home_stats_by_date(cls, db_conn, player_id, from_date, to_date):
        query = ('SELECT s.* FROM {} s JOIN games g ON s.game_id = g.id AND s.team_id = g.home_team_id '
                 'WHERE s.player_id = %s AND s.date >= %s AND s.date < %s').format(cls._table_name)
        return cls._get_columns_from_db(db_conn, query, (player_id, from_date, to_date))

    @classmethod
    def get_player_away_stats_by_date(cls, db_conn, player_id, from_date, to_date):
        query = ('SELECT s.* FROM {} s JOIN games g ON s.game_id = g.id AND s.team_id = g.away_team_id '
                 'WHERE s.player_id = %s AND s.date >= %s AND s.date < %s').format(cls._table_name)
        return cls._get_columns_from_db(db_conn, query, (player_id, from_date, to_date))
