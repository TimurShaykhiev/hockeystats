from data_models.update import Update


def get_last_stat_update(db):
    return Update.from_db(db, Update.STAT_UPDATE_TYPE)


def set_last_stat_update(db, start, end, successful):
    with db as cur:
        num = cur.execute(
            'UPDATE updates SET start = %s, end = %s, successful = %s WHERE type = %s',
            (start, end, successful, Update.STAT_UPDATE_TYPE))
    cur.close()
    return num
