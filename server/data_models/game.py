from datetime import datetime, timedelta

from data_models.model import Model
from data_models.team import Team
from data_models import convert_bool


def convert_str_to_date(date_str, tz_offset):
    offset = timedelta(hours=tz_offset)
    return (datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ") + offset).date()


class Game(Model):
    _table_name = 'games'
    _query_get_by_id = 'SELECT * FROM games WHERE id = %s'

    WIN_TYPE_REGULAR = 'regular'
    WIN_TYPE_OVERTIME = 'overtime'
    WIN_TYPE_SHOOTOUT = 'shootout'

    class TeamStat:
        def __init__(self):
            self.team = None
            self.goals = 0
            self.goals_period1 = 0
            self.goals_period2 = 0
            self.goals_period3 = 0
            self.shots = 0
            self.pp_goals = 0
            self.pp_opportunities = 0
            self.face_off_wins = 0
            self.blocked = 0
            self.takeaways = 0
            self.giveaways = 0
            self.hits = 0
            self.penalty_minutes = 0

        @classmethod
        def from_json(cls, obj):
            team_stat = cls()

            team_stat.team = Team()
            team_stat.team.id = obj['team']['id']

            stats = obj['teamStats'].get('teamSkaterStats')
            team_stat.pp_opportunities = int(stats['powerPlayOpportunities'])
            # Don't read other stats because some of them can be missed. They're populated in game_loader.
            return team_stat

    def __init__(self):
        self.id = None
        self.date = None
        self.is_regular = True
        self.win_type = self.WIN_TYPE_REGULAR
        self.home = None
        self.away = None
        self.face_off_taken = 0

    @classmethod
    def from_json(cls, obj):
        game = cls()
        game.id = obj['gamePk']
        game_data = obj['gameData']
        game.is_regular = game_data['game']['type'] == 'R'
        game.date = convert_str_to_date(game_data['datetime']['dateTime'],
                                        float(game_data['teams']['home']['venue']['timeZone']['offset']))

        box_score_teams = obj['liveData']['boxscore']['teams']
        game.home = cls.TeamStat.from_json(box_score_teams['home'])
        game.away = cls.TeamStat.from_json(box_score_teams['away'])

        line_score = obj['liveData']['linescore']
        has_shootout = line_score['hasShootout']
        has_overtime = False
        game.home.goals = line_score['teams']['home']['goals']
        game.away.goals = line_score['teams']['away']['goals']
        for p in line_score['periods']:
            if p['num'] == 1:
                game.home.goals_period1 = p['home']['goals']
                game.away.goals_period1 = p['away']['goals']
            elif p['num'] == 2:
                game.home.goals_period2 = p['home']['goals']
                game.away.goals_period2 = p['away']['goals']
            elif p['num'] == 3:
                game.home.goals_period3 = p['home']['goals']
                game.away.goals_period3 = p['away']['goals']
            elif p['num'] == 4:
                has_overtime = True

        if has_shootout:
            game.win_type = cls.WIN_TYPE_SHOOTOUT
        elif has_overtime:
            game.win_type = cls.WIN_TYPE_OVERTIME

        return game

    @classmethod
    def from_tuple(cls, fields):
        game = cls()
        game.id = fields[0]
        game.date = fields[1]
        game.is_regular = bool(fields[2])
        game.win_type = fields[3]
        game.home = cls.TeamStat()
        game.home.team = Team()
        game.home.team.id = fields[4]
        game.away = cls.TeamStat()
        game.away.team = Team
        game.away.team.id = fields[5]
        game.home.goals = fields[6]
        game.home.goals_period1 = fields[7]
        game.home.goals_period2 = fields[8]
        game.home.goals_period3 = fields[9]
        game.home.shots = fields[10]
        game.home.pp_goals = fields[11]
        game.home.pp_opportunities = fields[12]
        game.home.face_off_wins = fields[13]
        game.home.blocked = fields[14]
        game.home.takeaways = fields[15]
        game.home.giveaways = fields[16]
        game.home.hits = fields[17]
        game.home.penalty_minutes = fields[18]
        game.away.goals = fields[19]
        game.away.goals_period1 = fields[20]
        game.away.goals_period2 = fields[21]
        game.away.goals_period3 = fields[22]
        game.away.shots = fields[23]
        game.away.pp_goals = fields[24]
        game.away.pp_opportunities = fields[25]
        game.away.face_off_wins = fields[26]
        game.away.blocked = fields[27]
        game.away.takeaways = fields[28]
        game.away.giveaways = fields[29]
        game.away.hits = fields[30]
        game.away.penalty_minutes = fields[31]
        game.face_off_taken = fields[32]
        return game

    def to_tuple(self):
        return (self.id, self.date, self.is_regular, self.win_type, self.home.team.id, self.away.team.id,
                self.home.goals, self.home.goals_period1, self.home.goals_period2, self.home.goals_period3,
                self.home.shots, self.home.pp_goals, self.home.pp_opportunities, self.home.face_off_wins,
                self.home.blocked, self.home.takeaways, self.home.giveaways, self.home.hits, self.home.penalty_minutes,
                self.away.goals, self.away.goals_period1, self.away.goals_period2, self.away.goals_period3,
                self.away.shots, self.away.pp_goals, self.away.pp_opportunities, self.away.face_off_wins,
                self.away.blocked, self.away.takeaways, self.away.giveaways, self.away.hits, self.away.penalty_minutes,
                self.face_off_taken)

    def __str__(self):
        return ('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t'
                '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n').format(
            self.id,
            self.date,
            convert_bool(self.is_regular),
            self.win_type,
            self.home.team.id,
            self.away.team.id,
            self.home.goals,
            self.home.goals_period1,
            self.home.goals_period2,
            self.home.goals_period3,
            self.home.shots,
            self.home.pp_goals,
            self.home.pp_opportunities,
            self.home.face_off_wins,
            self.home.blocked,
            self.home.takeaways,
            self.home.giveaways,
            self.home.hits,
            self.home.penalty_minutes,
            self.away.goals,
            self.away.goals_period1,
            self.away.goals_period2,
            self.away.goals_period3,
            self.away.shots,
            self.away.pp_goals,
            self.away.pp_opportunities,
            self.away.face_off_wins,
            self.away.blocked,
            self.away.takeaways,
            self.away.giveaways,
            self.away.hits,
            self.away.penalty_minutes,
            self.face_off_taken)
