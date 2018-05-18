import sys
import MySQLdb as Db
from datetime import timedelta, datetime

from config.config import get_custom_config
from logger import create_logger, LOADER_LOGGER_NAME, create_smtp_handler
from load import load, LOAD_RESULT_SUCCESS, LOAD_RESULT_TRY_AGAIN
from check_season import check_season
from correct_sum_stats import fix_sum_stats
from db_utils.updates import get_last_stat_update, set_last_stat_update

LOG = None
LOADER_LOG_FILE = 'loader.log'
config = None


# I don't want to do real timezone-aware calculations. Just make sure we don't download game info before
# midnight in PST. No need in precise time here.
def _is_in_future(end_date):
    pst_utc_offset = -8
    pst_time = datetime.utcnow() + timedelta(hours=pst_utc_offset)
    end_date = end_date + timedelta(days=1)
    end_date_midnight = datetime(year=end_date.year, month=end_date.month, day=end_date.day)
    return end_date_midnight > pst_time


def main():
    db_conn = Db.connect(host=config.DB_URL, user=config.DB_USER, password=config.DB_PASSWORD, database=config.DB_NAME,
                         charset='utf8')
    try:
        LOG.info('Scheduler start.')
        update = get_last_stat_update(db_conn)
        if update is None or not update.successful:
            LOG.error('Cannot process. Fix errors from prev load.')
            return
        new_date = update.end + timedelta(days=1)
        if _is_in_future(new_date):
            LOG.warning('New date is in the future.')
            return
        load_result = load(new_date, db_conn)
        if load_result != LOAD_RESULT_TRY_AGAIN:
            set_last_stat_update(db_conn, new_date, new_date, load_result == LOAD_RESULT_SUCCESS)
        if load_result == LOAD_RESULT_SUCCESS:
            check_season(db_conn, new_date)
            fix_sum_stats(db_conn, new_date)
    finally:
        db_conn.close()
    LOG.info('Scheduler end.')
    sys.exit(load_result)


if __name__ == '__main__':
    config = get_custom_config()
    email_handler = create_smtp_handler(config, 'Loader:Error')
    LOG = create_logger(LOADER_LOGGER_NAME, config.LOG_DIR + LOADER_LOG_FILE, email_handler=email_handler)
    main()
