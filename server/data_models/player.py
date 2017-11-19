from logger import get_loader_logger
from data_models.entity_model import EntityModel
from data_models.team import Team
from data_models import convert_attr_if_none, convert_str_to_date

LOG = get_loader_logger()

# NHL position 'code' mapping to DB 'primary_pos' enum
PLAYER_POSITION = {
  'C': 'center',
  'R': 'right wing',
  'L': 'left wing',
  'D': 'defenseman',
  'G': 'goalie'
}

# NHL 'shootsCatches' mapping to DB 'shoots_catches' enum
PLAYER_SHOOTS = {
  'R': 'right',
  'L': 'left'
}


# convert height from string <6' 2"> to inches
def convert_height(value):
    v = value.split(' ')
    feet = int(v[0][:-1])
    inches = int(v[1][:-1])
    return feet * 12 + inches


class Player(EntityModel):
    _table_name = 'players'

    CENTER = 'center'
    RIGHT_WING = 'right wing'
    LEFT_WING = 'left wing'
    DEFENSEMAN = 'defenseman'
    GOALIE = 'goalie'

    def __init__(self):
        self.id = None
        self.name = ''
        self.birth_date = None
        self.birth_city = ''
        self.birth_state = ''
        self.birth_country = ''
        self.nationality = ''
        self.height = 0
        self.weight = 0
        self.shoots_catches = ''
        self.primary_pos = ''
        self.current_team = None

    @classmethod
    def from_json(cls, obj):
        player = cls()
        player.id = obj['id']
        player.name = obj['fullName']
        player.birth_date = convert_str_to_date(obj.get('birthDate', '1900-01-01'))
        player.birth_city = obj.get('birthCity', player.birth_city)
        player.birth_country = obj.get('birthCountry', player.birth_country)
        player.birth_state = obj.get('birthStateProvince', player.birth_state)
        player.nationality = obj.get('nationality', player.nationality)
        height = obj.get('height')
        if height:
            player.height = convert_height(obj.get('height'))
        player.weight = obj.get('weight', player.weight)
        shoots_catches = obj.get('shootsCatches')
        if shoots_catches is None:
            # This field is mandatory, but in rare cases it is missed in server response. Set it to 'L'.
            shoots_catches = 'L'
            LOG.warning('Player %s: shootsCatches is missed. Set to L.', player.id)
        player.shoots_catches = PLAYER_SHOOTS[shoots_catches]
        player.primary_pos = PLAYER_POSITION[obj['primaryPosition']['code']]
        team = obj.get('currentTeam')
        if team:
            player.current_team = Team()
            player.current_team.id = team['id']
        return player

    @classmethod
    def from_tuple(cls, fields):
        player = cls()
        player.id = fields[0]
        player.name = fields[1]
        player.birth_date = fields[2]
        player.birth_city = fields[3]
        player.birth_state = fields[4]
        player.birth_country = fields[5]
        player.nationality = fields[6]
        player.height = fields[7]
        player.weight = fields[8]
        player.shoots_catches = fields[9]
        player.primary_pos = fields[10]
        team_id = fields[11]
        if team_id:
            player.current_team = Team()
            player.current_team.id = team_id
        return player

    def to_tuple(self):
        return (self.id, self.name, self.birth_date, self.birth_city, self.birth_state, self.birth_country,
                self.nationality, self.height, self.weight, self.shoots_catches, self.primary_pos,
                self.current_team.id if self.current_team else None)

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.id,
            self.name,
            self.birth_date,
            self.birth_city,
            self.birth_state,
            self.birth_country,
            self.nationality,
            self.height,
            self.weight,
            self.shoots_catches,
            self.primary_pos,
            convert_attr_if_none(self.current_team, 'id'))

    @classmethod
    def get_skaters(cls, db_conn, columns=None, named_tuple_cls=None):
        q = cls._create_query().select(columns).where('primary_pos != \'goalie\'')
        if columns is None:
            return cls._get_all_from_db(db_conn, q.query)
        return cls._get_columns_from_db(db_conn, q.query, named_tuple_cls=named_tuple_cls)

    @classmethod
    def get_goalies(cls, db_conn, columns=None, named_tuple_cls=None):
        return cls.get_filtered(db_conn, ['primary_pos'], ['goalie'], columns, named_tuple_cls)
