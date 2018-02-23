from datetime import timedelta
from abc import ABC, abstractmethod

from app.database import get_db

CHART_POINTS_PROGRESS_INTERVAL = timedelta(days=5)


class ChartData(ABC):
    def __init__(self, season=None):
        self.season = season
        self._schema_cls = None

    def get_data(self):
        db = get_db()
        self._prepare_data(db)
        schema = self._schema_cls()
        return schema.dumps(self)

    @abstractmethod
    def _prepare_data(self, db):
        pass
