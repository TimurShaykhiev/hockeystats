from data_models.event_model import EventModel
from data_models.team import Team
from data_models.player import Player
from data_models.game import Game
from data_models import convert_if_none, convert_attr_if_none, convert_time_to_sec, get_coordinates, NameValue, \
    TypeValue

PENALTY_TYPES = {
  'Abuse of Officials': 1,
  'Abusive language': 2,
  'Aggressor': 3,
  'Bench': 4,
  'Boarding': 5,
  'Broken stick': 6,
  'Butt ending': 7,
  'Charging': 8,
  'Checking from behind': 9,
  'Clipping': 10,
  'Closing hand on puck': 11,
  'Coach or Manager on the ice': 12,
  'Concealing puck': 13,
  'Cross check - double minor': 14,
  'Cross checking': 15,
  'Delay Gm - Face-off Violation': 16,
  'Delay of game': 17,
  'Delaying Game - Illegal play by goalie': 18,
  'Delaying Game - Puck over glass': 19,
  'Delaying Game - Smothering puck': 20,
  'Delaying the game': 21,
  'Diving': 22,
  'Elbowing': 23,
  'Embellishment': 24,
  'Face-off violation': 25,
  'Face-off violation-bench': 26,
  'Fighting': 27,
  'Game misconduct': 28,
  'Game Misconduct - Head coach': 29,
  'Game Misconduct - Team staff': 30,
  'Goalie leave crease': 31,
  'Head butting': 32,
  'Head butting - double minor': 33,
  'Hi stick - double minor': 34,
  'Hi-sticking': 35,
  'Holding': 36,
  'Holding the stick': 37,
  'Hooking': 38,
  'Illegal check to head': 39,
  'Illegal equipment': 40,
  'Illegal stick': 41,
  'Illegal substitution': 42,
  'Instigator': 43,
  'Instigator - face shield': 44,
  'Instigator - Misconduct': 45,
  'Interference': 46,
  'Interference - Goalkeeper': 47,
  'Kneeing': 48,
  'Leaving penalty box': 49,
  'Major': 50,
  'Match penalty': 51,
  'Misconduct': 52,
  'Objects on ice': 53,
  'Player leaves bench': 54,
  'PS - Covering puck in crease': 55,
  'PS - Goalkeeper displaced net': 56,
  'PS - Holding on breakaway': 57,
  'PS - Hooking on breakaway': 58,
  'PS - Net displaced': 59,
  'PS - Slash on breakaway': 60,
  'PS - Thow object at puck': 61,
  'PS - Tripping on breakaway': 62,
  'PS-Holding on breakaway': 63,
  'PS-Hooking on breakaway': 64,
  'PS-Slash on breakaway': 65,
  'PS-Thow object at puck': 66,
  'PS-Tripping on breakaway': 67,
  'Roughing': 68,
  'Slashing': 69,
  'Spearing': 70,
  'Spearing - double minor': 71,
  'Throwing stick': 72,
  'Too many men on the ice': 73,
  'Tripping': 74,
  'Unsportsmanlike conduct': 75
}


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

    @classmethod
    def get_season_penalty_types_percentage(cls, db_conn, start, end, limit):
        where_str = 'p.date >= %s AND p.date < %s AND p.secondary_type IS NOT NULL'
        return cls._get_penalty_types_percentage(db_conn, where_str, (start, end), limit)

    @classmethod
    def get_team_penalty_types_percentage(cls, db_conn, team_id, start, end, limit):
        where_str = 'p.date >= %s AND p.date < %s AND p.secondary_type IS NOT NULL AND team_id = %s'
        return cls._get_penalty_types_percentage(db_conn, where_str, (start, end, team_id), limit)

    @classmethod
    def get_player_penalty_types_percentage(cls, db_conn, player_id, start, end, limit):
        where_str = 'p.date >= %s AND p.date < %s AND p.secondary_type IS NOT NULL AND penalty_on_id = %s'
        return cls._get_penalty_types_percentage(db_conn, where_str, (start, end, player_id), limit)

    @classmethod
    def _get_penalty_types_percentage(cls, db_conn, where_str, where_params, limit):
        """
        :type where_params: tuple
        :type limit: integer
        """
        query = ('SELECT COUNT(p.secondary_type) * 100 / t.total AS count, p.secondary_type '
                 'FROM penalty p, (SELECT COUNT(secondary_type) AS total FROM penalty p WHERE {}) t '
                 'WHERE {} GROUP BY p.secondary_type ORDER BY count DESC LIMIT %s').format(where_str, where_str)
        query_params = where_params * 2 + (limit,)
        res = cls._get_columns_from_db(db_conn, query, query_params)
        return [TypeValue(PENALTY_TYPES[r[1]], r[0]) for r in res]
