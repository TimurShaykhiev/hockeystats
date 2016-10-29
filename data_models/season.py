from data_models import convert_bool, get_from_db


class Season:
    def __init__(self):
        self.id = None
        self.start = None
        self.end = None
        self.current = False

    @classmethod
    def from_tuple(cls, fields):
        season = cls()
        season.id = fields[0]
        season.start = fields[1]
        season.end = fields[2]
        season.current = bool(fields[3])
        return season

    @classmethod
    def from_db(cls, db, season_id):
        return get_from_db(cls, db, 'SELECT * FROM seasons WHERE id = %s', [season_id])

    def __str__(self):
        return '{}\t{}\t{}\t{}\n'.format(
            self.id,
            self.start,
            self.end,
            convert_bool(self.current))
