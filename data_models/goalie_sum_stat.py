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
