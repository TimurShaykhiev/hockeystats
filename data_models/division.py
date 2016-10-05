from data_models.conference import Conference
from data_models import convert_bool, convert_attr_if_none


class Division:
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

    def __str__(self):
        return '{}\t{}\t{}\t{}\n'.format(
            self.id,
            self.name,
            convert_attr_if_none(self.conference, 'id'),
            convert_bool(self.active))
