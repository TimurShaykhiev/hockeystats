from datetime import datetime
from collections import namedtuple

from data_models.player import Player
from data_models.team import Team


PLAYER_BDAY = datetime(2000, 3, 25).date()
TeamData = namedtuple('TeamData', 'id, players, goalies')
TEAMS = [
    TeamData(id=100, players=[100100, 100101, 100102, 100103, 100104, 100105, 100106, 100107, 100108, 100109], goalies=[100150, 100151]),
    TeamData(id=200, players=[100200, 100201, 100202, 100203, 100204, 100205, 100206, 100207, 100208, 100209], goalies=[100250, 100251]),
    TeamData(id=300, players=[100300, 100301, 100302, 100303, 100304, 100305, 100306, 100307, 100308, 100309], goalies=[100350, 100351]),
    TeamData(id=400, players=[100400, 100401, 100402, 100403, 100404, 100405, 100406, 100407, 100408, 100409], goalies=[100450, 100451]),
    TeamData(id=500, players=[100500, 100501, 100502, 100503, 100504, 100505, 100506, 100507, 100508, 100509], goalies=[100550, 100551]),
    TeamData(id=600, players=[100600, 100601, 100602, 100603, 100604, 100605, 100606, 100607, 100608, 100609], goalies=[100650, 100651]),
    TeamData(id=700, players=[100700, 100701, 100702, 100703, 100704, 100705, 100706, 100707, 100708, 100709], goalies=[100750, 100751]),
    TeamData(id=800, players=[100800, 100801, 100802, 100803, 100804, 100805, 100806, 100807, 100808, 100809], goalies=[100850, 100851]),
    TeamData(id=900, players=[100900, 100901, 100902, 100903, 100904, 100905, 100906, 100907, 100908, 100909], goalies=[100950, 100951])
]


def _find_team_and_pos(pid):
    for t_data in TEAMS:
        if pid in t_data.players:
            t = Team()
            t.id = t_data.id
            return t, 'center'
        if pid in t_data.goalies:
            t = Team()
            t.id = t_data.id
            return t, 'goalie'


def create_player(pid):
    p = Player()
    p.id = pid
    p.name = 'Player_' + str(pid)
    p.birth_city = 'Toronto'
    p.birth_country = 'CAN'
    p.height = 175
    p.weight = 200
    p.birth_date = PLAYER_BDAY
    p.shoots_catches = 'right'
    p.current_team, p.primary_pos = _find_team_and_pos(pid)
    return p


def get_players(links):
    players = []
    for link in links:
        p = create_player(link)
        players.append(p)
    return players
