from data_models import convert_bool


class Conference:
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

    def __str__(self):
        return '{}\t{}\t{}\n'.format(self.id, self.name, convert_bool(self.active))
