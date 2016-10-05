from data_models import convert_bool


class Season:
    def __init__(self):
        self.id = None
        self.start = None
        self.end = None
        self.current = False

    def __str__(self):
        return '{}\t{}\t{}\t{}\n'.format(
            self.id,
            self.start,
            self.end,
            convert_bool(self.current))
