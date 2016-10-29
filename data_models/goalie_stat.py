from data_models.team import Team
from data_models.player import Player
from data_models.game import Game
from data_models import convert_time_to_sec

# NHL 'decision' mapping to DB 'decision' enum
DECISION = {
  'W': 'winner',
  'L': 'loser'
}


class GoalieStat:
    DECISION_WINNER = 'winner'
    DECISION_LOSER = 'loser'
    DECISION_NONE = 'none'

    def __init__(self):
        self.player = None
        self.team = None
        self.game = None
        self.date = None
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
        self.decision = self.DECISION_NONE

    @classmethod
    def from_json(cls, obj, game_id, team_id, event_date):
        goalie_stat = cls()
        goalie_stat.game = Game()
        goalie_stat.game.id = game_id
        goalie_stat.team = Team()
        goalie_stat.team.id = team_id
        goalie_stat.date = event_date

        goalie_stat.player = Player()
        goalie_stat.player.id = obj['person']['id']

        stats = obj['stats'].get('goalieStats')
        if stats:
            goalie_stat.toi = convert_time_to_sec(stats['timeOnIce'])
            goalie_stat.assists = stats['assists']
            goalie_stat.goals = stats['goals']
            goalie_stat.penalty_minutes = stats['pim']
            goalie_stat.shots = stats['shots']
            goalie_stat.saves = stats['saves']
            goalie_stat.pp_saves = stats['powerPlaySaves']
            goalie_stat.sh_saves = stats['shortHandedSaves']
            goalie_stat.even_saves = stats['evenSaves']
            goalie_stat.sh_shots_against = stats['shortHandedShotsAgainst']
            goalie_stat.even_shots_against = stats['evenShotsAgainst']
            goalie_stat.pp_shots_against = stats['powerPlayShotsAgainst']
            if stats['decision']:
                goalie_stat.decision = DECISION[stats['decision']]
            return goalie_stat
        return None

    @classmethod
    def from_tuple(cls, fields):
        goalie_stat = cls()
        goalie_stat.player = Player()
        goalie_stat.player.id = fields[0]
        goalie_stat.team = Team()
        goalie_stat.team.id = fields[1]
        goalie_stat.game = Game()
        goalie_stat.game.id = fields[2]
        goalie_stat.date = fields[3]
        goalie_stat.toi = fields[4]
        goalie_stat.assists = fields[5]
        goalie_stat.goals = fields[6]
        goalie_stat.penalty_minutes = fields[7]
        goalie_stat.shots = fields[8]
        goalie_stat.saves = fields[9]
        goalie_stat.pp_saves = fields[10]
        goalie_stat.sh_saves = fields[11]
        goalie_stat.even_saves = fields[12]
        goalie_stat.sh_shots_against = fields[13]
        goalie_stat.even_shots_against = fields[14]
        goalie_stat.pp_shots_against = fields[15]
        goalie_stat.decision = fields[16]
        return goalie_stat

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.player.id,
            self.team.id,
            self.game.id,
            self.date,
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
            self.decision)
