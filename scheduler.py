import sys
import MySQLdb as Db
from datetime import timedelta

from config import CONFIG
from load import load
from db_utils.updates import get_last_stat_update, set_last_stat_update


def main():
    db_conn = Db.connect('localhost', CONFIG['db_user'], CONFIG['db_password'], CONFIG['db_name'])
    try:
        update = get_last_stat_update(db_conn)
        if update is None or not update.successful:
            sys.exit(-1)
        new_start = new_end = update.end + timedelta(days=1)
        successful_load = load(new_start, new_end, db_conn)
        set_last_stat_update(db_conn, new_start, new_end, successful_load)
    finally:
        db_conn.close()

if __name__ == '__main__':
    main()
