from collections import namedtuple

from logger import get_loader_logger
from data_models.event_model import EventModel
from data_models.team import Team
from data_models.player import Player
from data_models.game import Game
from data_models import convert_if_none, convert_attr_if_none, convert_bool, convert_time_to_sec, get_coordinates

LOG = get_loader_logger()

# NHL strength 'code' mapping to DB 'strength' enum
GAME_STRENGTH = {
  'EVEN': 'even',
  'PPG': 'ppg',
  'SHG': 'shg'
}

ScorerDuo = namedtuple('ScorerDuo', ['goals', 'pid1', 'pid2'])


class Goal(EventModel):
    _table_name = 'goals'

    STRENGTH_EVEN = 'even'
    STRENGTH_PPG = 'ppg'
    STRENGTH_SHG = 'shg'

    def __init__(self):
        self.id = None
        self.team = None
        self.game = None
        self.date = None
        self.scorer = None
        self.assist1 = None
        self.assist2 = None
        self.secondary_type = ''
        self.empty_net = False
        self.strength = ''
        self.period_num = 0
        self.period_time = 0
        self.coord_x = None
        self.coord_y = None

    @classmethod
    def from_json(cls, obj, game_id, event_date):
        goal = cls()
        goal.game = Game()
        goal.game.id = game_id
        goal.date = event_date

        team = obj['team']
        goal.team = Team()
        goal.team.id = team['id']

        players = obj['players']
        for pl in players:
            p = Player()
            p.id = pl['player']['id']
            if pl['playerType'] == 'Scorer':
                goal.scorer = p
            elif pl['playerType'] == 'Assist':
                if goal.assist1 is None:
                    goal.assist1 = p
                else:
                    goal.assist2 = p

        about = obj['about']
        goal.period_num = about['period']
        goal.period_time = convert_time_to_sec(about['periodTime'])

        result = obj['result']
        sec_type = result.get('secondaryType')
        if sec_type:
            goal.secondary_type = sec_type
        strength = result.get('strength')
        if strength is None or strength.get('code') is None:
            # This field is mandatory, but in rare cases it is missed in server response. Set it to 'EVEN'.
            goal.strength = goal.STRENGTH_EVEN
            LOG.warning('Goal %s, %s, %s : strength is missed. Set to EVEN.',
                        goal.game.id, goal.period_num, goal.period_time)
        else:
            goal.strength = GAME_STRENGTH[strength['code']]
        is_empty_net = result.get('isEmptyNet')
        if is_empty_net:
            goal.empty_net = is_empty_net

        goal.coord_x, goal.coord_y = get_coordinates(obj)
        return goal

    @classmethod
    def from_tuple(cls, fields):
        goal = cls()
        goal.id = fields[0]
        goal.team = Team()
        goal.team.id = fields[1]
        goal.game = Game()
        goal.game.id = fields[2]
        goal.date = fields[3]
        goal.scorer = Player()
        goal.scorer.id = fields[4]
        assist_id = fields[5]
        if assist_id:
            goal.assist1 = Player()
            goal.assist1.id = assist_id
        assist_id = fields[6]
        if assist_id:
            goal.assist2 = Player()
            goal.assist2.id = assist_id
        goal.secondary_type = fields[7]
        goal.empty_net = bool(fields[8])
        goal.strength = fields[9]
        goal.period_num = fields[10]
        goal.period_time = fields[11]
        goal.coord_x = fields[12]
        goal.coord_y = fields[13]
        return goal

    def to_tuple(self):
        return (self.team.id, self.game.id, self.date, self.scorer.id,
                self.assist1.id if self.assist1 is not None else None,
                self.assist2.id if self.assist2 is not None else None,
                self.secondary_type, self.empty_net, self.strength, self.period_num, self.period_time,
                self.coord_x, self.coord_y)

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.team.id,
            self.game.id,
            self.date,
            self.scorer.id,
            convert_attr_if_none(self.assist1, 'id'),
            convert_attr_if_none(self.assist2, 'id'),
            self.secondary_type,
            convert_bool(self.empty_net),
            self.strength,
            self.period_num,
            self.period_time,
            convert_if_none(self.coord_x),
            convert_if_none(self.coord_y))

    @classmethod
    def get_scorer_duos(cls, db_conn, start, end, limit):
        query = ('SELECT COUNT(*), tbl.pl1, tbl.pl2 '
                 'FROM (SELECT LEAST(g.scorer_id, g.assist1_id) AS pl1, GREATEST(g.scorer_id, g.assist1_id) AS pl2 '
                 'FROM goals g WHERE g.date >= %s AND g.date < %s AND g.assist1_id IS NOT NULL) AS tbl '
                 'GROUP BY tbl.pl1, tbl.pl2 ORDER BY COUNT(*) DESC LIMIT %s')
        return cls._get_columns_from_db(db_conn, query, (start, end, limit), named_tuple_cls=ScorerDuo)
