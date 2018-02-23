from marshmallow import fields

from data_models.game import Game
from statistics.games import get_points_progress
from .season import SeasonSchema
from .charts import CHART_POINTS_PROGRESS_INTERVAL, ChartData
from . import ModelSchema, StatValue


class _TeamChart(ChartData):
    def __init__(self, team_id, season=None):
        super().__init__(season)
        self.team_id = team_id


class TeamPointsProgressChart(_TeamChart):
    def __init__(self, team_id, season):
        super().__init__(team_id, season)
        self._schema_cls = _TeamSeasonChartDataSchema
        self.chart_data = []
        self.interval = CHART_POINTS_PROGRESS_INTERVAL.days

    def _prepare_data(self, db):
        games = Game.get_team_games(db, self.team_id, self.season.start, self.season.end, self.season.regular)
        self.chart_data = get_points_progress(self.team_id, games, self.season.start, CHART_POINTS_PROGRESS_INTERVAL)


class _TeamSeasonChartDataSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    tid = fields.Integer(attribute='team_id')
    data = fields.List(StatValue(), attribute='chart_data')
    interval = fields.Integer()
