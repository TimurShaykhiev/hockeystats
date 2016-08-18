def convert_if_none(obj, attr):
    return getattr(obj, attr, '\\N')


def convert_bool(val):
    return 1 if val else 0
