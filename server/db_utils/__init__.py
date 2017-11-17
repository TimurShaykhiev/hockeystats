def get_all_from_query_result(cls, cur):
    return [cls.from_tuple(row) for row in cur.fetchall()]


def get_one_from_query_result(cls, cur):
    fields = cur.fetchone()
    if fields:
        return cls.from_tuple(fields)
    return None


def get_columns_from_table(db_conn, table_name, columns):
    query = 'SELECT {} FROM {}'.format(', '.join(columns), table_name)
    with db_conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
