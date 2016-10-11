from data_models.player import Player
from data_models.season import Season
from data_models import convert_bool


class SkaterSumStat:
    def __init__(self):
        self.player = None
        self.season = None
        self.is_regular = True
        self.assists = 0
        self.goals = 0
        self.shots = 0
        self.hits = 0
        self.pp_goals = 0
        self.pp_assists = 0
        self.penalty_minutes = 0
        self.face_off_wins = 0
        self.face_off_taken = 0
        self.takeaways = 0
        self.giveaways = 0
        self.sh_goals = 0
        self.sh_assists = 0
        self.blocked = 0
        self.plus_minus = 0
        self.toi = 0
        self.even_toi = 0
        self.pp_toi = 0
        self.sh_toi = 0
        self.games = 0

    def __str__(self):
        return ('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t'
                '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n').format(
            self.player.id,
            self.season.id,
            convert_bool(self.is_regular),
            self.assists,
            self.goals,
            self.shots,
            self.hits,
            self.pp_goals,
            self.pp_assists,
            self.penalty_minutes,
            self.face_off_wins,
            self.face_off_taken,
            self.takeaways,
            self.giveaways,
            self.sh_goals,
            self.sh_assists,
            self.blocked,
            self.plus_minus,
            self.toi,
            self.even_toi,
            self.pp_toi,
            self.sh_toi,
            self.games)
