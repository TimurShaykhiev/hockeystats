from datetime import datetime


def convert_attr_if_none(obj, attr):
    return getattr(obj, attr, '\\N')


def convert_if_none(val):
    return val if val is not None else '\\N'


def convert_bool(val):
    return 1 if val else 0


# returns True if fixed
def check_and_fix_attr_unsigned(obj, attr):
    if getattr(obj, attr) < 0:
        setattr(obj, attr, 0)
        return True
    return False


# time in format "mm:ss"
def convert_time_to_sec(time):
    m, s = time.split(':')
    return int(m) * 60 + int(s)


def convert_str_to_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date()


def get_coordinates(obj):
    x = None
    y = None
    coordinates = obj.get('coordinates')
    if coordinates:
        # sometimes data may be corrupted, for example - no 'x' coordinate
        _x = coordinates.get('x')
        _y = coordinates.get('y')
        if (_x is not None) and (_y is not None):
            x = int(float(_x))
            y = int(float(_y))
    return x, y
