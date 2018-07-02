from data_models.event_model import EventModel
from data_models.team import Team
from data_models.player import Player
from data_models.game import Game
from data_models import convert_if_none, convert_attr_if_none, convert_time_to_sec, get_coordinates, NameValue


class Penalty(EventModel):
    _table_name = 'penalty'

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

    @classmethod
    def from_tuple(cls, fields):
        penalty = cls()
        penalty.id = fields[0]
        penalty.team = Team()
        penalty.team.id = fields[1]
        penalty.game = Game()
        penalty.game.id = fields[2]
        penalty.date = fields[3]
        penalty.penalty_on = Player()
        penalty.penalty_on.id = fields[4]
        drew_by_id = fields[5]
        if drew_by_id:
            penalty.drew_by = Player()
            penalty.drew_by.id = drew_by_id
        penalty.penalty_minutes = fields[6]
        penalty.secondary_type = fields[7]
        penalty.period_num = fields[8]
        penalty.period_time = fields[9]
        penalty.coord_x = fields[10]
        penalty.coord_y = fields[11]
        return penalty

    def to_tuple(self):
        return (self.team.id, self.game.id, self.date, self.penalty_on.id,
                self.drew_by.id if self.drew_by is not None else None, self.penalty_minutes, self.secondary_type,
                self.period_num, self.period_time, self.coord_x, self.coord_y)

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

    @classmethod
    def get_drew_by_top(cls, db_conn, start, end, limit, lang=None):
        if lang is None:
            query = ('SELECT pl.name, COUNT(pen.id) FROM penalty pen JOIN players pl ON pen.drew_by_id = pl.id '
                     'WHERE pen.date >= %s AND pen.date < %s AND pen.drew_by_id IS NOT NULL '
                     'GROUP BY pen.drew_by_id ORDER BY COUNT(pen.id) DESC LIMIT %s')
        else:
            query = ('SELECT tr.{}, COUNT(pen.id) FROM penalty pen '
                     'JOIN translations tr ON pen.drew_by_id = tr.resource_id '
                     'WHERE pen.date >= %s AND pen.date < %s AND pen.drew_by_id IS NOT NULL AND '
                     'tr.resource_type = "player_name" '
                     'GROUP BY pen.drew_by_id ORDER BY COUNT(pen.id) DESC LIMIT %s').format(lang)
        return cls._get_columns_from_db(db_conn, query, (start, end, limit), named_tuple_cls=NameValue)
