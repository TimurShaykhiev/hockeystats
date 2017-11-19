from logger import get_loader_logger
from data_models.sum_stats_model import SumStatsModel
from data_models.team import Team
from data_models.season import Season
from data_models.game import Game
from data_models import convert_bool

LOG = get_loader_logger()


class TeamSumStat(SumStatsModel):
    _table_name = 'team_sum_stats'
    _primary_keys = ['team_id', 'season_id', 'is_regular']

    def __init__(self, team=None, season=None, regular=True):
        self.team = team
        self.season = season
        self.is_regular = regular
        self.goals_for = 0
        self.goals_against = 0
        self.shots = 0
        self.pp_goals = 0
        self.pp_opportunities = 0
        self.sh_goals_against = 0
        self.sh_opportunities = 0
        self.face_off_wins = 0
        self.face_off_taken = 0
        self.blocked = 0
        self.takeaways = 0
        self.giveaways = 0
        self.hits = 0
        self.penalty_minutes = 0
        self.games = 0
        self.win_regular = 0
        self.win_overtime = 0
        self.win_shootout = 0
        self.lose_regular = 0
        self.lose_overtime = 0
        self.lose_shootout = 0

    @classmethod
    def from_tuple(cls, fields):
        team_stat = cls()
        team_stat.team = Team()
        team_stat.team.id = fields[0]
        team_stat.season = Season()
        team_stat.season.id = fields[1]
        team_stat.is_regular = bool(fields[2])
        team_stat.goals_for = fields[3]
        team_stat.goals_against = fields[4]
        team_stat.shots = fields[5]
        team_stat.pp_goals = fields[6]
        team_stat.pp_opportunities = fields[7]
        team_stat.sh_goals_against = fields[8]
        team_stat.sh_opportunities = fields[9]
        team_stat.face_off_wins = fields[10]
        team_stat.face_off_taken = fields[11]
        team_stat.blocked = fields[12]
        team_stat.takeaways = fields[13]
        team_stat.giveaways = fields[14]
        team_stat.hits = fields[15]
        team_stat.penalty_minutes = fields[16]
        team_stat.games = fields[17]
        team_stat.win_regular = fields[18]
        team_stat.win_overtime = fields[19]
        team_stat.win_shootout = fields[20]
        team_stat.lose_regular = fields[21]
        team_stat.lose_overtime = fields[22]
        team_stat.lose_shootout = fields[23]
        return team_stat

    def add_stat(self, game, team_id, season_id):
        if self.team.id != team_id or self.season.id != season_id or self.is_regular != game.is_regular:
            LOG.error('TeamSumStat.add_stat invalid parameters %s, %s, %s', team_id, season_id, game.is_regular)
            raise ValueError
        if game.home.team.id != team_id and game.away.team.id != team_id:
            LOG.error('TeamSumStat.add_stat invalid team_id %s: %s, %s', team_id, game.home.team.id, game.away.team.id)
            raise ValueError

        if team_id == game.home.team.id:
            my_team_stat, opp_team_stat = game.home, game.away
        else:
            my_team_stat, opp_team_stat = game.away, game.home
        self.goals_for += my_team_stat.goals_period1 + my_team_stat.goals_period2 + my_team_stat.goals_period3
        self.goals_against += opp_team_stat.goals_period1 + opp_team_stat.goals_period2 + opp_team_stat.goals_period3
        self.shots += my_team_stat.shots
        self.pp_goals += my_team_stat.pp_goals
        self.pp_opportunities += my_team_stat.pp_opportunities
        self.sh_goals_against += opp_team_stat.pp_goals
        self.sh_opportunities += opp_team_stat.pp_opportunities
        self.face_off_wins += my_team_stat.face_off_wins
        self.face_off_taken += game.face_off_taken
        self.blocked += my_team_stat.blocked
        self.takeaways += my_team_stat.takeaways
        self.giveaways += my_team_stat.giveaways
        self.hits += my_team_stat.hits
        self.penalty_minutes += my_team_stat.penalty_minutes
        self.games += 1
        if my_team_stat.goals > opp_team_stat.goals:
            if game.win_type == Game.WIN_TYPE_REGULAR:
                self.win_regular += 1
            elif game.win_type == Game.WIN_TYPE_OVERTIME:
                self.win_overtime += 1
            else:
                self.win_shootout += 1
        else:
            if game.win_type == Game.WIN_TYPE_REGULAR:
                self.lose_regular += 1
            elif game.win_type == Game.WIN_TYPE_OVERTIME:
                self.lose_overtime += 1
            else:
                self.lose_shootout += 1

    def add_sum_stat(self, sum_stat):
        # sum_stat is TeamSumStat
        if self.team.id != sum_stat.team.id or self.season.id != sum_stat.season.id or \
           self.is_regular != sum_stat.is_regular:
            LOG.error('TeamSumStat.add_sum_stat invalid parameters %s, %s, %s',
                      sum_stat.team.id, sum_stat.season.id, sum_stat.is_regular)
            raise ValueError
        self.goals_for += sum_stat.goals_for
        self.goals_against += sum_stat.goals_against
        self.shots += sum_stat.shots
        self.pp_goals += sum_stat.pp_goals
        self.pp_opportunities += sum_stat.pp_opportunities
        self.sh_goals_against += sum_stat.sh_goals_against
        self.sh_opportunities += sum_stat.sh_opportunities
        self.face_off_wins += sum_stat.face_off_wins
        self.face_off_taken += sum_stat.face_off_taken
        self.blocked += sum_stat.blocked
        self.takeaways += sum_stat.takeaways
        self.giveaways += sum_stat.giveaways
        self.hits += sum_stat.hits
        self.penalty_minutes += sum_stat.penalty_minutes
        self.games += sum_stat.games
        self.win_regular += sum_stat.win_regular
        self.win_overtime += sum_stat.win_overtime
        self.win_shootout += sum_stat.win_shootout
        self.lose_regular += sum_stat.lose_regular
        self.lose_overtime += sum_stat.lose_overtime
        self.lose_shootout += sum_stat.lose_shootout

    def to_tuple(self):
        return (self.team.id, self.season.id, self.is_regular, self.goals_for, self.goals_against, self.shots,
                self.pp_goals, self.pp_opportunities, self.sh_goals_against, self.sh_opportunities, self.face_off_wins,
                self.face_off_taken, self.blocked, self.takeaways, self.giveaways, self.hits, self.penalty_minutes,
                self.games, self.win_regular, self.win_overtime, self.win_shootout, self.lose_regular,
                self.lose_overtime, self.lose_shootout)

    def __str__(self):
        return ('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t'
                '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n').format(
            self.team.id,
            self.season.id,
            convert_bool(self.is_regular),
            self.goals_for,
            self.goals_against,
            self.shots,
            self.pp_goals,
            self.pp_opportunities,
            self.sh_goals_against,
            self.sh_opportunities,
            self.face_off_wins,
            self.face_off_taken,
            self.blocked,
            self.takeaways,
            self.giveaways,
            self.hits,
            self.penalty_minutes,
            self.games,
            self.win_regular,
            self.win_overtime,
            self.win_shootout,
            self.lose_regular,
            self.lose_overtime,
            self.lose_shootout)
