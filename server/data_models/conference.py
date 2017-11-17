from data_models.entity_model import EntityModel
from data_models import convert_bool


class Conference(EntityModel):
    _table_name = 'conferences'
    _query_get_by_id = 'SELECT * FROM conferences WHERE id = %s'

    def __init__(self):
        self.id = None
        self.name = ''
        self.active = False

    @classmethod
    def from_json(cls, obj):
        conf = cls()
        conf.id = obj['id']
        conf.name = obj['name']
        conf.active = obj['active']
        return conf

    @classmethod
    def from_tuple(cls, fields):
        conf = cls()
        conf.id = fields[0]
        conf.name = fields[1]
        conf.active = bool(fields[2])
        return conf

    def to_tuple(self):
        return self.id, self.name, self.active

    def __str__(self):
        return '{}\t{}\t{}\n'.format(self.id, self.name, convert_bool(self.active))
