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

    @classmethod
    def from_tuple(cls, fields):
        skater_stat = cls()
        skater_stat.player = Player()
        skater_stat.player.id = fields[0]
        skater_stat.season = Season()
        skater_stat.season.id = fields[1]
        skater_stat.is_regular = bool(fields[2])
        skater_stat.assists = fields[3]
        skater_stat.goals = fields[4]
        skater_stat.shots = fields[5]
        skater_stat.hits = fields[6]
        skater_stat.pp_goals = fields[7]
        skater_stat.pp_assists = fields[8]
        skater_stat.penalty_minutes = fields[9]
        skater_stat.face_off_wins = fields[10]
        skater_stat.face_off_taken = fields[11]
        skater_stat.takeaways = fields[12]
        skater_stat.giveaways = fields[13]
        skater_stat.sh_goals = fields[14]
        skater_stat.sh_assists = fields[15]
        skater_stat.blocked = fields[16]
        skater_stat.plus_minus = fields[17]
        skater_stat.toi = fields[18]
        skater_stat.even_toi = fields[19]
        skater_stat.pp_toi = fields[20]
        skater_stat.sh_toi = fields[21]
        skater_stat.games = fields[22]
        return skater_stat

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
