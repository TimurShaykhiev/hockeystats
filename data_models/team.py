from data_models.division import Division
from data_models.venue import Venue
from data_models import convert_bool, convert_attr_if_none


class Team:
    def __init__(self):
        self.id = None
        self.name = ''
        self.abbreviation = ''
        self.location = ''
        self.venue = None
        self.division = None
        self.conference = None
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
