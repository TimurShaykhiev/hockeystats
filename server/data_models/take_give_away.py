from data_models.event_model import EventModel
from data_models.team import Team
from data_models.player import Player
from data_models.game import Game
from data_models import convert_time_to_sec, get_coordinates, convert_if_none

DB_TYPE_TAKEAWAY = 'takeaway'
DB_TYPE_GIVEAWAY = 'giveaway'


def create_from_json(obj, game_id, event_date):
    tg = None
    event_type = obj['result']['eventTypeId']
    if event_type == 'TAKEAWAY':
        tg = Takeaway.from_json(obj)
    elif event_type == 'GIVEAWAY':
        tg = Giveaway.from_json(obj)
    if tg:
        tg.game = Game()
        tg.game.id = game_id
        tg.date = event_date
    return tg


def create_from_tuple(fields):
    cls = Takeaway if fields[5] == DB_TYPE_TAKEAWAY else Giveaway
    return cls.from_tuple(fields)


class _TGEvent(EventModel):
    _table_name = 'take_give_away'

    def __init__(self):
        self.id = None
        self.team = None
        self.game = None
        self.date = None
        self.player = None
        self.period_num = 0
        self.period_time = 0
        self.coord_x = None
        self.coord_y = None

    @classmethod
    def from_json(cls, obj):
        tg_event = cls()
        team = obj['team']
        tg_event.team = Team()
        tg_event.team.id = team['id']

        players = obj['players']
        tg_event.player = Player()
        tg_event.player.id = players[0]['player']['id']

        about = obj['about']
        tg_event.period_num = about['period']
        tg_event.period_time = convert_time_to_sec(about['periodTime'])

        tg_event.coord_x, tg_event.coord_y = get_coordinates(obj)
        return tg_event

    @classmethod
    def from_tuple(cls, fields):
        tg_event = cls()
        tg_event.id = fields[0]
        tg_event.team = Team()
        tg_event.team.id = fields[1]
        tg_event.game = Game()
        tg_event.game.id = fields[2]
        tg_event.date = fields[3]
        tg_event.player = Player()
        tg_event.player.id = fields[4]
        tg_event.period_num = fields[6]
        tg_event.period_time = fields[7]
        tg_event.coord_x = fields[8]
        tg_event.coord_y = fields[9]
        return tg_event

    @classmethod
    def get_all(cls, db_conn):
        if cls == Takeaway:
            query = "SELECT * FROM take_give_away WHERE type = 'takeaway'"
        else:
            query = "SELECT * FROM take_give_away WHERE type = 'giveaway'"
        return cls._get_all_from_db(db_conn, query)

    def to_tuple(self):
        raise NotImplementedError()


class Takeaway(_TGEvent):
    def __init__(self):
        super().__init__()

    def to_tuple(self):
        return (self.team.id, self.game.id, self.date, self.player.id, DB_TYPE_TAKEAWAY, self.period_num,
                self.period_time, self.coord_x, self.coord_y)

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.team.id,
            self.game.id,
            self.date,
            self.player.id,
            DB_TYPE_TAKEAWAY,
            self.period_num,
            self.period_time,
            convert_if_none(self.coord_x),
            convert_if_none(self.coord_y))


class Giveaway(_TGEvent):
    def __init__(self):
        super().__init__()

    def to_tuple(self):
        return (self.team.id, self.game.id, self.date, self.player.id, DB_TYPE_GIVEAWAY, self.period_num,
                self.period_time, self.coord_x, self.coord_y)

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.team.id,
            self.game.id,
            self.date,
            self.player.id,
            DB_TYPE_GIVEAWAY,
            self.period_num,
            self.period_time,
            convert_if_none(self.coord_x),
            convert_if_none(self.coord_y))
