from data_models.entity_model import EntityModel
from data_models.division import Division
from data_models.venue import Venue
from data_models.query import Query
from data_models import convert_bool, convert_attr_if_none


class Team(EntityModel):
    _table_name = 'teams'

    def __init__(self):
        self.id = None
        self.name = ''
        self.abbreviation = ''
        self.location = ''
        self.venue = None
        self.division = None
        self.active = False

    @classmethod
    def from_json(cls, obj):
        team = cls()
        team.id = obj['id']
        team.name = obj['name']
        team.abbreviation = obj['abbreviation']
        team.location = obj['locationName']
        venue = obj.get('venue')
        if venue:
            team.venue = Venue.from_json(venue)
        div = obj.get('division')
        if div:
            team.division = Division()
            team.division.id = div['id']
            team.division.name = div['name']
        team.active = obj['active']
        return team

    @classmethod
    def from_tuple(cls, fields):
        team = cls()
        team.id = fields[0]
        team.name = fields[1]
        team.abbreviation = fields[2]
        team.location = fields[3]
        v_name = fields[4]
        v_city = fields[5]
        if v_name or v_city:
            team.venue = Venue()
            team.venue.name = v_name
            team.venue.city = v_city
        div_id = fields[6]
        if div_id:
            team.division = Division()
            team.division.id = div_id
        team.active = bool(fields[7])
        return team

    @classmethod
    def get_for_season(cls, db_conn, season_id, regular, columns=None, named_tuple_cls=None):
        col_list = Query.get_col_list(columns, 't')
        query = 'SELECT {} FROM teams t JOIN team_sum_stats s ON t.id = s.team_id ' \
                'WHERE s.season_id = %s AND s.is_regular = %s'.format(col_list)
        if columns is None:
            return cls._get_all_from_db(db_conn, query, (season_id, regular))
        return cls._get_columns_from_db(db_conn, query, (season_id, regular), named_tuple_cls=named_tuple_cls)

    def to_tuple(self):
        return (self.id, self.name, self.abbreviation, self.location,
                self.venue.name if self.venue else None,
                self.venue.city if self.venue else None,
                self.division.id if self.division else None,
                self.active)

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.id,
            self.name,
            self.abbreviation,
            self.location,
            convert_attr_if_none(self.venue, 'name'),
            convert_attr_if_none(self.venue, 'city'),
            convert_attr_if_none(self.division, 'id'),
            convert_bool(self.active))
