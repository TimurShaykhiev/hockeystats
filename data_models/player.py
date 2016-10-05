from data_models.team import Team
from data_models import convert_attr_if_none, convert_str_to_date

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


class Player:
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
        player.birth_date = convert_str_to_date(obj['birthDate'])
        player.birth_city = obj['birthCity']
        player.birth_country = obj['birthCountry']
        state = obj.get('birthStateProvince')
        if state:
            player.birth_state = state
        nationality = obj.get('nationality')
        if nationality:
            player.nationality = nationality
        player.height = convert_height(obj['height'])
        player.weight = obj['weight']
        player.shoots_catches = PLAYER_SHOOTS[obj['shootsCatches']]
        player.primary_pos = PLAYER_POSITION[obj['primaryPosition']['code']]
        team = obj['currentTeam']
        if team:
            player.current_team = Team()
            player.current_team.id = team['id']
        return player

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
