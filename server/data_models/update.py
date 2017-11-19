from data_models import convert_bool
from data_models.entity_model import EntityModel


class Update(EntityModel):
    _table_name = 'updates'
    _primary_keys = ['type']

    STAT_UPDATE_TYPE = 0

    def __init__(self):
        self.type = None
        self.description = ''
        self.start = None
        self.end = None
        self.successful = False

    @classmethod
    def from_tuple(cls, fields):
        upd = cls()
        upd.type = fields[0]
        upd.description = fields[1]
        upd.start = fields[2]
        upd.end = fields[3]
        upd.successful = bool(fields[4])
        return upd

    def to_tuple(self):
        return self.type, self.description, self.start, self.end, self.successful

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\n'.format(
            self.type,
            self.description,
            self.start,
            self.end,
            convert_bool(self.successful))
