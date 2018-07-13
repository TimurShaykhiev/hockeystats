from marshmallow import fields

from data_models.penalty import Penalty
from .season import SeasonSchema
from .charts import ChartData, NameValueDataSchema, BAR_CHART_ELEMENTS_LIMIT
from . import ModelSchema, get_locale, DEFAULT_LOCALE


class SkaterPenaltyDrewByChart(ChartData):
    def __init__(self, season):
        super().__init__(season)
        self._schema_cls = _SkatersChartDataSchema
        self.chart_data = []

    def _prepare_data(self, db):
        locale = get_locale()
        if locale == DEFAULT_LOCALE:
            locale = None
        start, end = self.season.get_dates()
        self.chart_data = Penalty.get_drew_by_top(db, start, end, BAR_CHART_ELEMENTS_LIMIT, locale)


class _SkatersChartDataSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    data = fields.Nested(NameValueDataSchema, attribute='chart_data', many=True)
