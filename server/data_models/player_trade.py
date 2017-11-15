from data_models import get_from_db


class PlayerTrade:
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
    def from_db(cls, db, player_id):
        return get_from_db(cls, db, 'SELECT * FROM player_trades WHERE player_id = %s', [player_id])

    def to_tuple(self):
        return self.player_id, self.date, self.from_team, self.to_team

    def __str__(self):
        return '{}\t{}\t{}\t{}\n'.format(
            self.player_id,
            self.date,
            self.from_team,
            self.to_team)
