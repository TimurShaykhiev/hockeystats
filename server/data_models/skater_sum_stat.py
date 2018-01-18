from logger import get_loader_logger
from data_models.sum_stats_model import SumStatsModel
from data_models.player import Player
from data_models.season import Season
from data_models import convert_bool

LOG = get_loader_logger()


class SkaterSumStat(SumStatsModel):
    _table_name = 'skater_sum_stats'
    _primary_keys = ['player_id', 'season_id', 'is_regular']
    _object_id_field = 'player_id'

    def __init__(self, player=None, season=None, regular=True):
        self.player = player
        self.season = season
        self.is_regular = regular
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
    def from_json(cls, obj):
        skater_stat = cls()
        skater_stat.player = Player()
        skater_stat.player.id = obj['playerId']

        skater_stat.games = obj['gamesPlayed']
        skater_stat.assists = obj['assists']
        skater_stat.goals = obj['goals']
        skater_stat.shots = obj['shots']
        skater_stat.pp_goals = obj['ppGoals']
        skater_stat.pp_assists = obj['ppPoints'] - obj['ppGoals']
        skater_stat.sh_goals = obj['shGoals']
        skater_stat.sh_assists = obj['shPoints'] - obj['shGoals']
        skater_stat.plus_minus = obj['plusMinus']
        skater_stat.penalty_minutes = obj['penaltyMinutes']
        return skater_stat

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

    def add_stat(self, stat, season_id, regular):
        # stat is SkaterStat
        if self.player.id != stat.player.id or self.season.id != season_id or self.is_regular != regular:
            LOG.error('SkaterSumStat.add_stat invalid parameters %s, %s, %s', stat.player.id, season_id, regular)
            raise ValueError
        self.assists += stat.assists
        self.goals += stat.goals
        self.shots += stat.shots
        self.hits += stat.hits
        self.pp_goals += stat.pp_goals
        self.pp_assists += stat.pp_assists
        self.penalty_minutes += stat.penalty_minutes
        self.face_off_wins += stat.face_off_wins
        self.face_off_taken += stat.face_off_taken
        self.takeaways += stat.takeaways
        self.giveaways += stat.giveaways
        self.sh_goals += stat.sh_goals
        self.sh_assists += stat.sh_assists
        self.blocked += stat.blocked
        self.plus_minus += stat.plus_minus
        self.toi += stat.toi
        self.even_toi += stat.even_toi
        self.pp_toi += stat.pp_toi
        self.sh_toi += stat.sh_toi
        if stat.toi > 0:
            self.games += 1

    def add_sum_stat(self, sum_stat):
        # sum_stat is SkaterSumStat
        if self.player.id != sum_stat.player.id or self.season.id != sum_stat.season.id or \
           self.is_regular != sum_stat.is_regular:
            LOG.error('SkaterSumStat.add_sum_stat invalid parameters %s, %s, %s',
                      sum_stat.player.id, sum_stat.season.id, sum_stat.is_regular)
            raise ValueError
        self.assists += sum_stat.assists
        self.goals += sum_stat.goals
        self.shots += sum_stat.shots
        self.hits += sum_stat.hits
        self.pp_goals += sum_stat.pp_goals
        self.pp_assists += sum_stat.pp_assists
        self.penalty_minutes += sum_stat.penalty_minutes
        self.face_off_wins += sum_stat.face_off_wins
        self.face_off_taken += sum_stat.face_off_taken
        self.takeaways += sum_stat.takeaways
        self.giveaways += sum_stat.giveaways
        self.sh_goals += sum_stat.sh_goals
        self.sh_assists += sum_stat.sh_assists
        self.blocked += sum_stat.blocked
        self.plus_minus += sum_stat.plus_minus
        self.toi += sum_stat.toi
        self.even_toi += sum_stat.even_toi
        self.pp_toi += sum_stat.pp_toi
        self.sh_toi += sum_stat.sh_toi
        self.games += sum_stat.games

    def to_tuple(self):
        return (self.player.id, self.season.id, self.is_regular, self.assists, self.goals, self.shots, self.hits,
                self.pp_goals, self.pp_assists, self.penalty_minutes, self.face_off_wins, self.face_off_taken,
                self.takeaways, self.giveaways, self.sh_goals, self.sh_assists, self.blocked, self.plus_minus,
                self.toi, self.even_toi, self.pp_toi, self.sh_toi, self.games)

    def compare(self, obj, print_diff=False):
        if obj.games != self.games or obj.assists != self.assists or obj.goals != self.goals or\
           obj.shots != self.shots or obj.pp_goals != self.pp_goals or obj.pp_assists != self.pp_assists or\
           obj.sh_goals != self.sh_goals or obj.sh_assists != self.sh_assists or obj.plus_minus != self.plus_minus or\
           obj.penalty_minutes != self.penalty_minutes:
            if print_diff:
                print('{} {} {} {} {} {} {} {} {} {} {}'.format(self.player.id,
                                                                obj.assists - self.assists,
                                                                obj.goals - self.goals,
                                                                obj.shots - self.shots,
                                                                obj.pp_goals - self.pp_goals,
                                                                obj.pp_assists - self.pp_assists,
                                                                obj.penalty_minutes - self.penalty_minutes,
                                                                obj.sh_goals - self.sh_goals,
                                                                obj.sh_assists - self.sh_assists,
                                                                obj.plus_minus - self.plus_minus,
                                                                obj.games - self.games))
            return (obj.assists, obj.goals, obj.shots, obj.pp_goals, obj.pp_assists, obj.penalty_minutes, obj.sh_goals,
                    obj.sh_assists, obj.plus_minus, obj.games, self.player.id, self.season.id, self.is_regular)
        return None

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
