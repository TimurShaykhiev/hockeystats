from data_models.team import Team
from data_models.player import Player
from data_models.game import Game
from data_models import convert_if_none, convert_attr_if_none, convert_time_to_sec, get_coordinates


class Penalty:
    def __init__(self):
        self.id = None
        self.team = None
        self.game = None
        self.date = None
        self.penalty_on = None
        self.drew_by = None
        self.penalty_minutes = 0
        self.secondary_type = ''
        self.period_num = 0
        self.period_time = 0
        self.coord_x = None
        self.coord_y = None

    @classmethod
    def from_json(cls, obj, game_id, event_date):
        penalty = cls()
        penalty.game = Game()
        penalty.game.id = game_id
        penalty.date = event_date

        team = obj['team']
        penalty.team = Team()
        penalty.team.id = team['id']

        players = obj['players']
        for pl in players:
            p = Player()
            p.id = pl['player']['id']
            if pl['playerType'] == 'PenaltyOn':
                penalty.penalty_on = p
            elif pl['playerType'] == 'DrewBy':
                penalty.drew_by = p

        result = obj['result']
        penalty.secondary_type = result['secondaryType']
        penalty.penalty_minutes = result['penaltyMinutes']

        about = obj['about']
        penalty.period_num = about['period']
        penalty.period_time = convert_time_to_sec(about['periodTime'])

        penalty.coord_x, penalty.coord_y = get_coordinates(obj)
        return penalty

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.team.id,
            self.game.id,
            self.date,
            self.penalty_on.id,
            convert_attr_if_none(self.drew_by, 'id'),
            self.penalty_minutes,
            self.secondary_type,
            self.period_num,
            self.period_time,
            convert_if_none(self.coord_x),
            convert_if_none(self.coord_y))
