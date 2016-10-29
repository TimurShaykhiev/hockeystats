from data_models.player import Player
from data_models.season import Season
from data_models import convert_bool


class GoalieSumStat:
    def __init__(self):
        self.player = None
        self.season = None
        self.is_regular = True
        self.toi = 0
        self.assists = 0
        self.goals = 0
        self.penalty_minutes = 0
        self.shots = 0
        self.saves = 0
        self.pp_saves = 0
        self.sh_saves = 0
        self.even_saves = 0
        self.sh_shots_against = 0
        self.even_shots_against = 0
        self.pp_shots_against = 0
        self.games = 0
        self.wins = 0
        self.shutout = 0

    @classmethod
    def from_tuple(cls, fields):
        goalie_stat = cls()
        goalie_stat.player = Player()
        goalie_stat.player.id = fields[0]
        goalie_stat.season = Season()
        goalie_stat.season.id = fields[1]
        goalie_stat.is_regular = fields[2]
        goalie_stat.toi = fields[3]
        goalie_stat.assists = fields[4]
        goalie_stat.goals = fields[5]
        goalie_stat.penalty_minutes = fields[6]
        goalie_stat.shots = fields[7]
        goalie_stat.saves = fields[8]
        goalie_stat.pp_saves = fields[9]
        goalie_stat.sh_saves = fields[10]
        goalie_stat.even_saves = fields[11]
        goalie_stat.sh_shots_against = fields[12]
        goalie_stat.even_shots_against = fields[13]
        goalie_stat.pp_shots_against = fields[14]
        goalie_stat.games = fields[15]
        goalie_stat.wins = fields[16]
        goalie_stat.shutout = fields[17]
        return goalie_stat

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.player.id,
            self.season.id,
            convert_bool(self.is_regular),
            self.toi,
            self.assists,
            self.goals,
            self.penalty_minutes,
            self.shots,
            self.saves,
            self.pp_saves,
            self.sh_saves,
            self.even_saves,
            self.sh_shots_against,
            self.even_shots_against,
            self.pp_shots_against,
            self.games,
            self.wins,
            self.shutout)
