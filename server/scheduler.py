import sys
import MySQLdb as Db
from datetime import timedelta, datetime

from logger import create_loader_logger
from config import DB_URL, DB_USER, DB_PASSWORD, DB_NAME
from load import load, LOAD_RESULT_SUCCESS, LOAD_RESULT_TRY_AGAIN
from db_utils.updates import get_last_stat_update, set_last_stat_update

LOG = None


# I don't want to do real timezone-aware calculations. Just make sure we don't download game info before
# midnight in PST. No need in precise time here.
def _is_in_future(end_date):
    pst_utc_offset = -8
    pst_time = datetime.utcnow() + timedelta(hours=pst_utc_offset)
    end_date = end_date + timedelta(days=1)
    end_date_midnight = datetime(year=end_date.year, month=end_date.month, day=end_date.day)
    return end_date_midnight > pst_time


def main():
    db_conn = Db.connect(DB_URL, DB_USER, DB_PASSWORD, DB_NAME)
    try:
        LOG.info('Scheduler start.')
        update = get_last_stat_update(db_conn)
        if update is None or not update.successful:
            LOG.error('Cannot process. Fix errors from prev load.')
            return
        new_start = new_end = update.end + timedelta(days=1)
        if _is_in_future(new_end):
            LOG.warning('New date is in the future.')
            return
        load_result = load(new_start, new_end, db_conn)
        if load_result != LOAD_RESULT_TRY_AGAIN:
            set_last_stat_update(db_conn, new_start, new_end, load_result == LOAD_RESULT_SUCCESS)
    finally:
        db_conn.close()
    LOG.info('Scheduler end.')
    sys.exit(load_result)


if __name__ == '__main__':
    LOG = create_loader_logger()
    main()
