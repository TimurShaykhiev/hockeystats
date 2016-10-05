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
        self.decision = 'none'

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
