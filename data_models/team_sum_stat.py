from data_models.team import Team
from data_models.season import Season
from data_models import convert_bool


class TeamSumStat:
    def __init__(self):
        self.team = None
        self.season = None
        self.is_regular = True
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
