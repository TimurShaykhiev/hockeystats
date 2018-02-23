from marshmallow import fields

from data_models.skater_stat import SkaterStat
from statistics.skater_stats import get_points_progress
from .season import SeasonSchema
from .charts import CHART_POINTS_PROGRESS_INTERVAL, ChartData
from . import ModelSchema, StatValue


class _PlayerChart(ChartData):
    def __init__(self, player_id, season=None):
        super().__init__(season)
        self.player_id = player_id


class SkaterPointsProgressChart(_PlayerChart):
    def __init__(self, player_id, season):
        super().__init__(player_id, season)
        self._schema_cls = _PlayerSeasonChartDataSchema
        self.chart_data = []
        self.interval = CHART_POINTS_PROGRESS_INTERVAL.days

    def _prepare_data(self, db):
        start, end = self.season.get_dates()
        stats = SkaterStat.get_player_stats_by_date(db, self.player_id, start, end)
        self.chart_data = get_points_progress(stats, self.season.start, CHART_POINTS_PROGRESS_INTERVAL)


class _PlayerSeasonChartDataSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    pid = fields.Integer(attribute='player_id')
    data = fields.List(StatValue(), attribute='chart_data')
    interval = fields.Integer()
