from data_models.team import Team
from data_models.player import Player
from data_models.game import Game
from data_models import convert_time_to_sec


class SkaterStat:
    def __init__(self):
        self.player = None
        self.team = None
        self.game = None
        self.date = None
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

    @classmethod
    def from_json(cls, obj, game_id, team_id, event_date):
        skater_stat = cls()
        skater_stat.game = Game()
        skater_stat.game.id = game_id
        skater_stat.team = Team()
        skater_stat.team.id = team_id
        skater_stat.date = event_date

        skater_stat.player = Player()
        skater_stat.player.id = obj['person']['id']

        stats = obj['stats'].get('skaterStats')
        if stats:
            skater_stat.assists = stats['assists']
            skater_stat.goals = stats['goals']
            skater_stat.shots = stats['shots']
            skater_stat.hits = stats['hits']
            skater_stat.pp_goals = stats['powerPlayGoals']
            skater_stat.pp_assists = stats['powerPlayAssists']
            skater_stat.penalty_minutes = stats['penaltyMinutes']
            skater_stat.face_off_wins = stats['faceOffWins']
            skater_stat.face_off_taken = stats['faceoffTaken']
            skater_stat.takeaways = stats['takeaways']
            skater_stat.giveaways = stats['giveaways']
            skater_stat.sh_goals = stats['shortHandedGoals']
            skater_stat.sh_assists = stats['shortHandedAssists']
            skater_stat.blocked = stats['blocked']
            skater_stat.plus_minus = stats['plusMinus']
            skater_stat.toi = convert_time_to_sec(stats['timeOnIce'])
            skater_stat.even_toi = convert_time_to_sec(stats['evenTimeOnIce'])
            skater_stat.pp_toi = convert_time_to_sec(stats['powerPlayTimeOnIce'])
            skater_stat.sh_toi = convert_time_to_sec(stats['shortHandedTimeOnIce'])
            return skater_stat
        return None

    @classmethod
    def from_tuple(cls, fields):
        skater_stat = cls()
        skater_stat.player = Player()
        skater_stat.player.id = fields[0]
        skater_stat.team = Team()
        skater_stat.team.id = fields[1]
        skater_stat.game = Game()
        skater_stat.game.id = fields[2]
        skater_stat.date = fields[3]
        skater_stat.assists = fields[4]
        skater_stat.goals = fields[5]
        skater_stat.shots = fields[6]
        skater_stat.hits = fields[7]
        skater_stat.pp_goals = fields[8]
        skater_stat.pp_assists = fields[9]
        skater_stat.penalty_minutes = fields[10]
        skater_stat.face_off_wins = fields[11]
        skater_stat.face_off_taken = fields[12]
        skater_stat.takeaways = fields[13]
        skater_stat.giveaways = fields[14]
        skater_stat.sh_goals = fields[15]
        skater_stat.sh_assists = fields[16]
        skater_stat.blocked = fields[17]
        skater_stat.plus_minus = fields[18]
        skater_stat.toi = fields[19]
        skater_stat.even_toi = fields[20]
        skater_stat.pp_toi = fields[21]
        skater_stat.sh_toi = fields[22]
        return skater_stat

    @classmethod
    def load_data_to_db(cls, db_cur, filename):
        query = "LOAD DATA INFILE '{}' INTO TABLE NHL_STATS.skater_stats".format(filename)
        return db_cur.execute(query)

    def to_tuple(self):
        return (self.player.id, self.team.id, self.game.id, self.date, self.assists, self.goals, self.shots, self.hits,
                self.pp_goals, self.pp_assists, self.penalty_minutes, self.face_off_wins, self.face_off_taken,
                self.takeaways, self.giveaways, self.sh_goals, self.sh_assists, self.blocked, self.plus_minus, self.toi,
                self.even_toi, self.pp_toi, self.sh_toi)

    def __str__(self):
        return ('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t'
                '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n').format(
            self.player.id,
            self.team.id,
            self.game.id,
            self.date,
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
            self.sh_toi)
