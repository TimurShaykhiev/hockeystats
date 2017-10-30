from data_models import convert_bool, get_from_db


class Season:
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

    @classmethod
    def from_db(cls, db, season_id):
        return get_from_db(cls, db, 'SELECT * FROM seasons WHERE id = %s', [season_id])

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.id,
            self.start,
            self.po_start,
            self.end,
            self.status,
            convert_bool(self.current))
