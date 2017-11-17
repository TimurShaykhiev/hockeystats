from data_models.entity_model import EntityModel
from data_models.conference import Conference
from data_models import convert_bool, convert_attr_if_none


class Division(EntityModel):
    _table_name = 'divisions'
    _query_get_by_id = 'SELECT * FROM divisions WHERE id = %s'

    def __init__(self):
        self.id = None
        self.name = ''
        self.conference = None
        self.active = False

    @classmethod
    def from_json(cls, obj):
        div = cls()
        div.id = obj['id']
        div.name = obj['name']
        div.active = obj['active']
        conf = obj.get('conference')
        if conf:
            div.conference = Conference()
            div.conference.id = conf['id']
            div.conference.name = conf['name']
        return div

    @classmethod
    def from_tuple(cls, fields):
        div = cls()
        div.id = fields[0]
        div.name = fields[1]
        conf_id = fields[2]
        if conf_id:
            div.conference = Conference()
            div.conference.id = conf_id
        div.active = bool(fields[3])
        return div

    def to_tuple(self):
        return self.id, self.name, self.conference.id if self.conference else None, self.active

    def __str__(self):
        return '{}\t{}\t{}\t{}\n'.format(
            self.id,
            self.name,
            convert_attr_if_none(self.conference, 'id'),
            convert_bool(self.active))
