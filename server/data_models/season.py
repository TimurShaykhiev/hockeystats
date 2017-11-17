from data_models.entity_model import EntityModel
from data_models import convert_bool


class Season(EntityModel):
    _table_name = 'seasons'
    _query_get_by_id = 'SELECT * FROM seasons WHERE id = %s'

    STATUS_NOT_STARTED = 'not_started'
    STATUS_REGULAR = 'regular'
    STATUS_PLAY_OFF = 'play_off'
    STATUS_FINISHED = 'finished'

    def __init__(self):
        self.id = None
        self.start = None
        self.po_start = None
        self.end = None
        self.status = ''
        self.current = False

    @classmethod
    def from_tuple(cls, fields):
        season = cls()
        season.id = fields[0]
        season.start = fields[1]
        season.po_start = fields[2]
        season.end = fields[3]
        season.status = fields[4]
        season.current = bool(fields[5])
        return season

    def to_tuple(self):
        return self.id, self.start, self.po_start, self.end, self.status, self.current

    @classmethod
    def get_current(cls, db_conn):
        return cls._get_one_from_db(db_conn, 'SELECT * FROM seasons WHERE current = 1')

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.id,
            self.start,
            self.po_start,
            self.end,
            self.status,
            convert_bool(self.current))
