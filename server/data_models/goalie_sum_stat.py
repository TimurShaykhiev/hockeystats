from logger import get_loader_logger
from data_models.sum_stats_model import SumStatsModel
from data_models.player import Player
from data_models.season import Season
from data_models.goalie_stat import GoalieStat
from data_models import convert_bool

LOG = get_loader_logger()


class GoalieSumStat(SumStatsModel):
    _table_name = 'goalie_sum_stats'
    _primary_keys = ['player_id', 'season_id', 'is_regular']

    def __init__(self, player=None, season=None, regular=True):
        self.player = player
        self.season = season
        self.is_regular = regular
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
    def from_json(cls, obj):
        skater_stat = cls()
        skater_stat.player = Player()
        skater_stat.player.id = obj['playerId']

        skater_stat.games = obj['gamesPlayed']
        skater_stat.assists = obj['assists']
        skater_stat.goals = obj['goals']
        skater_stat.shots = obj['shotsAgainst']
        skater_stat.saves = obj['saves']
        skater_stat.penalty_minutes = obj['penaltyMinutes']
        skater_stat.shutout = obj['shutouts']
        return skater_stat

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

    def add_stat(self, stat, season_id, regular):
        # stat is GoalieStat
        if self.player.id != stat.player.id or self.season.id != season_id or self.is_regular != regular:
            LOG.error('GoalieSumStat.add_stat invalid parameters %s, %s, %s', stat.player.id, season_id, regular)
            raise ValueError
        self.toi += stat.toi
        self.assists += stat.assists
        self.goals += stat.goals
        self.penalty_minutes += stat.penalty_minutes
        self.shots += stat.shots
        self.saves += stat.saves
        self.pp_saves += stat.pp_saves
        self.sh_saves += stat.sh_saves
        self.even_saves += stat.even_saves
        self.sh_shots_against += stat.sh_shots_against
        self.even_shots_against += stat.even_shots_against
        self.pp_shots_against += stat.pp_shots_against
        if stat.toi > 0:
            self.games += 1
        if stat.decision == GoalieStat.DECISION_WINNER:
            self.wins += 1
        if stat.shots == stat.saves and stat.toi >= 3600:
            # if two goaltenders combine for a shutout, neither receives credit for the shutout
            self.shutout += 1

    def add_sum_stat(self, sum_stat):
        # sum_stat is GoalieSumStat
        if self.player.id != sum_stat.player.id or self.season.id != sum_stat.season.id or \
           self.is_regular != sum_stat.is_regular:
            LOG.error('GoalieSumStat.add_sum_stat invalid parameters %s, %s, %s',
                      sum_stat.player.id, sum_stat.season.id, sum_stat.is_regular)
            raise ValueError
        self.toi += sum_stat.toi
        self.assists += sum_stat.assists
        self.goals += sum_stat.goals
        self.penalty_minutes += sum_stat.penalty_minutes
        self.shots += sum_stat.shots
        self.saves += sum_stat.saves
        self.pp_saves += sum_stat.pp_saves
        self.sh_saves += sum_stat.sh_saves
        self.even_saves += sum_stat.even_saves
        self.sh_shots_against += sum_stat.sh_shots_against
        self.even_shots_against += sum_stat.even_shots_against
        self.pp_shots_against += sum_stat.pp_shots_against
        self.games += sum_stat.games
        self.wins += sum_stat.wins
        self.shutout += sum_stat.shutout

    def to_tuple(self):
        return (self.player.id, self.season.id, self.is_regular, self.toi, self.assists, self.goals,
                self.penalty_minutes, self.shots, self.saves, self.pp_saves, self.sh_saves, self.even_saves,
                self.sh_shots_against, self.even_shots_against, self.pp_shots_against, self.games, self.wins,
                self.shutout)

    def compare(self, obj, print_diff=False):
        if obj.games != self.games or obj.assists != self.assists or obj.goals != self.goals or\
           obj.shots != self.shots or obj.saves != self.saves or obj.penalty_minutes != self.penalty_minutes or\
           obj.shutout != self.shutout:
            if print_diff:
                print('{} {} {} {} {} {} {} {}'.format(self.player.id,
                                                       obj.assists - self.assists,
                                                       obj.goals - self.goals,
                                                       obj.shots - self.shots,
                                                       obj.saves - self.saves,
                                                       obj.penalty_minutes - self.penalty_minutes,
                                                       obj.shutout - self.shutout,
                                                       obj.games - self.games))
            return (obj.assists, obj.goals, obj.penalty_minutes, obj.shots, obj.saves, obj.games, obj.shutout,
                    self.player.id, self.season.id, self.is_regular)
        return None

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
