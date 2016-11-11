from data_models.team import Team
from data_models.player import Player
from data_models.game import Game
from data_models import convert_if_none, convert_attr_if_none, convert_bool, convert_time_to_sec, get_coordinates

# NHL strength 'code' mapping to DB 'strength' enum
GAME_STRENGTH = {
  'EVEN': 'even',
  'PPG': 'ppg',
  'SHG': 'shg'
}


class Goal:
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

        result = obj['result']
        sec_type = result.get('secondaryType')
        if sec_type:
            goal.secondary_type = sec_type
        goal.strength = GAME_STRENGTH[result['strength']['code']]
        is_empty_net = result.get('isEmptyNet')
        if is_empty_net:
            goal.empty_net = is_empty_net

        about = obj['about']
        goal.period_num = about['period']
        goal.period_time = convert_time_to_sec(about['periodTime'])

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

    @classmethod
    def load_data_to_db(cls, db_cur, filename):
        query = "LOAD DATA INFILE '{}' INTO TABLE NHL_STATS.goals " \
                "(team_id, game_id, date, scorer_id, assist1_id, assist2_id, secondary_type, empty_net, strength, " \
                "period_num, period_time, coord_x, coord_y) SET id = NULL".format(filename)
        return db_cur.execute(query)

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
