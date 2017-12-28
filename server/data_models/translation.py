from collections import namedtuple

from data_models.model import Model

RESOURCE_TYPE_CONF_NAME = 'conf_name'
RESOURCE_TYPE_DIV_NAME = 'div_name'
RESOURCE_TYPE_TEAM_NAME = 'team_name'
RESOURCE_TYPE_TEAM_ABBR = 'team_abbr'
RESOURCE_TYPE_TEAM_VENUE_NAME = 'team_venue_name'
RESOURCE_TYPE_PLAYER_NAME = 'player_name'

TeamStrings = namedtuple('TeamStrings', ['team_names', 'team_abbr', 'conf_names', 'div_names'])


def _prepare_result(translations):
    result = TeamStrings({}, {}, {}, {})
    for r_type, r_id, value in translations:
        if r_type == RESOURCE_TYPE_TEAM_NAME:
            result.team_names[r_id] = value
        elif r_type == RESOURCE_TYPE_TEAM_ABBR:
            result.team_abbr[r_id] = value
        elif r_type == RESOURCE_TYPE_CONF_NAME:
            result.conf_names[r_id] = value
        elif r_type == RESOURCE_TYPE_DIV_NAME:
            result.div_names[r_id] = value
    return result


class Translation(Model):
    _table_name = 'translations'

    def __init__(self):
        self.res_type = None
        self.res_id = None
        self.value = None

    @classmethod
    def get_team_strings(cls, db, team_id, lang):
        q = cls._create_query().select(['resource_type', 'resource_id', lang])
        q.where('(resource_type IN (%s, %s) AND resource_id = %s) OR resource_type IN (%s, %s)')
        translations = cls._get_columns_from_db(db, q.query, [RESOURCE_TYPE_TEAM_NAME, RESOURCE_TYPE_TEAM_ABBR,
                                                              team_id, RESOURCE_TYPE_CONF_NAME, RESOURCE_TYPE_DIV_NAME])
        return _prepare_result(translations)

    @classmethod
    def get_all_teams_strings(cls, db, lang):
        q = cls._create_query().select(['resource_type', 'resource_id', lang])
        types = [RESOURCE_TYPE_CONF_NAME, RESOURCE_TYPE_DIV_NAME, RESOURCE_TYPE_TEAM_NAME, RESOURCE_TYPE_TEAM_ABBR]
        q.where('resource_type IN ({})'.format(','.join(['%s'] * len(types))))
        translations = cls._get_columns_from_db(db, q.query, types)
        return _prepare_result(translations)

    @classmethod
    def from_tuple(cls, fields):
        pass

    def to_tuple(self):
        pass
