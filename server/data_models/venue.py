class Venue:
    def __init__(self):
        self.name = ''
        self.city = ''

    @classmethod
    def from_json(cls, obj):
        venue = cls()
        venue.name = obj['name']
        venue.city = obj['city']
        return venue
