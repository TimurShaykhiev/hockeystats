def get_all_from_query_result(cls, cur):
    return [cls.from_tuple(row) for row in cur.fetchall()]


def get_one_from_query_result(cls, cur):
    fields = cur.fetchone()
    if fields:
        return cls.from_tuple(fields)
    return None
