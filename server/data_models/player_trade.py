from data_models.model import Model


class PlayerTrade(Model):
    _table_name = 'player_trades'
    _query_get_by_id = 'SELECT * FROM player_trades WHERE player_id = %s'

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

    def to_tuple(self):
        return self.player_id, self.date, self.from_team, self.to_team

    def __str__(self):
        return '{}\t{}\t{}\t{}\n'.format(
            self.player_id,
            self.date,
            self.from_team,
            self.to_team)