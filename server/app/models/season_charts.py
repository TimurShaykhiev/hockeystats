from marshmallow import fields

from data_models.penalty import Penalty
from .season import SeasonSchema
from .charts import ChartData, TypeValueDataSchema, PIE_CHART_ELEMENTS_LIMIT
from . import ModelSchema


class _SeasonChartDataSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    data = fields.Nested(TypeValueDataSchema, attribute='chart_data', many=True)


class SeasonPenaltiesChart(ChartData):
    def __init__(self, season):
        super().__init__(season)
        self._schema_cls = _SeasonChartDataSchema
        self.chart_data = []

    def _prepare_data(self, db):
        start, end = self.season.get_dates()
        self.chart_data = Penalty.get_season_penalty_types_percentage(db, start, end, PIE_CHART_ELEMENTS_LIMIT)
