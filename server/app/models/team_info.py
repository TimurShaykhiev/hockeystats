from marshmallow import fields

from app.database import get_db
from data_models.team_sum_stat import TeamSumStat
from data_models.game import Game
from statistics.team_season import get_team_ext_stats
from .team import Team, TeamSchema
from .season import SeasonSchema
from . import ModelSchema, StatValue


class TeamInfo:
    def __init__(self, team_id, season):
        self.season = season
        self.team = Team.create(team_id)
        self.stats = []

    def get_info(self):
        db = get_db()
        stats = TeamSumStat.get_stat_tuples(db, self.season.id, self.season.regular)
        games = Game.get_team_games(db, self.team.id, self.season.start, self.season.end, self.season.regular)
        self.stats = get_team_ext_stats(self.team.id, stats, games)
        schema = TeamInfoSchema()
        return schema.dumps(self)


class TeamInfoSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    team = fields.Nested(TeamSchema)
    stats = fields.List(StatValue())
