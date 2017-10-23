from data_models import convert_bool, get_from_db


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

    @classmethod
    def from_tuple(cls, fields):
        conf = cls()
        conf.id = fields[0]
        conf.name = fields[1]
        conf.active = bool(fields[2])
        return conf

    @classmethod
    def from_db(cls, db, conf_id):
        return get_from_db(cls, db, 'SELECT * FROM conferences WHERE id = %s', [conf_id])

    def __str__(self):
        return '{}\t{}\t{}\n'.format(self.id, self.name, convert_bool(self.active))
