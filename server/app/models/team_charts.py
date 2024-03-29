from marshmallow import fields

from data_models.game import Game
from data_models.penalty import Penalty
from statistics.games import get_points_progress
from .season import SeasonSchema
from .charts import CHART_POINTS_PROGRESS_INTERVAL, ChartData, TypeValueDataSchema, PIE_CHART_ELEMENTS_LIMIT
from . import ModelSchema, StatValue


class _TeamChart(ChartData):
    def __init__(self, team_id, season=None):
        super().__init__(season)
        self.team_id = team_id


class _TeamSeasonChartDataWithIntervalSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    tid = fields.Integer(attribute='team_id')
    data = fields.List(StatValue(), attribute='chart_data')
    interval = fields.Integer()


class _TeamSeasonChartDataSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    tid = fields.Integer(attribute='team_id')
    data = fields.Nested(TypeValueDataSchema, attribute='chart_data', many=True)


class TeamPointsProgressChart(_TeamChart):
    def __init__(self, team_id, season):
        super().__init__(team_id, season)
        self._schema_cls = _TeamSeasonChartDataWithIntervalSchema
        self.chart_data = []
        self.interval = CHART_POINTS_PROGRESS_INTERVAL.days

    def _prepare_data(self, db):
        games = Game.get_team_games(db, self.team_id, self.season.start, self.season.end, self.season.regular)
        self.chart_data = get_points_progress(self.team_id, games, self.season.start, CHART_POINTS_PROGRESS_INTERVAL)


class TeamPenaltiesChart(_TeamChart):
    def __init__(self, team_id, season):
        super().__init__(team_id, season)
        self._schema_cls = _TeamSeasonChartDataSchema
        self.chart_data = []

    def _prepare_data(self, db):
        start, end = self.season.get_dates()
        self.chart_data = Penalty.get_team_penalty_types_percentage(db, self.team_id, start, end,
                                                                    PIE_CHART_ELEMENTS_LIMIT)
