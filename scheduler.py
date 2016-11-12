import MySQLdb as Db
from datetime import timedelta, date

from logger import create_loader_logger
from config import CONFIG
from load import load
from db_utils.updates import get_last_stat_update, set_last_stat_update

LOG = None


def main():
    db_conn = Db.connect('localhost', CONFIG['db_user'], CONFIG['db_password'], CONFIG['db_name'])
    try:
        LOG.info('Scheduler start.')
        update = get_last_stat_update(db_conn)
        if update is None or not update.successful:
            LOG.error('Cannot process. Fix errors from prev load.')
            return
        new_start = new_end = update.end + timedelta(days=1)
        if new_start > date.today():
            LOG.warning('New date is in the future.')
            return
        successful_load = load(new_start, new_end, db_conn)
        set_last_stat_update(db_conn, new_start, new_end, successful_load)
    finally:
        db_conn.close()
    LOG.info('Scheduler end.')

if __name__ == '__main__':
    LOG = create_loader_logger()
    main()
