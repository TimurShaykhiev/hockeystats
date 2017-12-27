from data_models.entity_model import EntityModel


class PlayerTrade(EntityModel):
    _table_name = 'player_trades'
    _primary_keys = ['player_id']

    def __init__(self, player_id=None, date=None, from_team=None, to_team=None):
        self.player_id = player_id
        self.date = date
        self.from_team = from_team
        self.to_team = to_team

    @classmethod
    def from_tuple(cls, fields):
        trade = cls()
        trade.player_id = fields[0]
        trade.date = fields[1]
        trade.from_team = fields[2]
        trade.to_team = fields[3]
        return trade

    @classmethod
    def get_for_team(cls, db, team_id):
        q = cls._create_query().select()
        q.where('from_team_id = %s OR to_team_id = %s')
        q.order_by(['date'])
        return cls._get_all_from_db(db, q.query, [team_id, team_id])

    def to_tuple(self):
        return self.player_id, self.date, self.from_team, self.to_team

    def __str__(self):
        return '{}\t{}\t{}\t{}\n'.format(
            self.player_id,
            self.date,
            self.from_team,
            self.to_team)
