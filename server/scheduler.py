import sys
import os
import MySQLdb as Db
from datetime import timedelta, datetime

import config
from logger import create_loader_logger
from load import load, LOAD_RESULT_SUCCESS, LOAD_RESULT_TRY_AGAIN
from check_season import check_season
from db_utils.updates import get_last_stat_update, set_last_stat_update

LOG = None


def _get_custom_config():
    """Read custom settings from file and update config variables in the config module."""
    config_path = os.environ.get('HOCKEYSTATS_CONFIG')
    if config_path is not None:
        try:
            with open(config_path, mode='rb') as config_file:
                exec(compile(config_file.read(), config_path, 'exec'), config.__dict__)
        except Exception:
            pass


# I don't want to do real timezone-aware calculations. Just make sure we don't download game info before
# midnight in PST. No need in precise time here.
def _is_in_future(end_date):
    pst_utc_offset = -8
    pst_time = datetime.utcnow() + timedelta(hours=pst_utc_offset)
    end_date = end_date + timedelta(days=1)
    end_date_midnight = datetime(year=end_date.year, month=end_date.month, day=end_date.day)
    return end_date_midnight > pst_time


def main():
    db_conn = Db.connect(config.DB_URL, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
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
            check_season(db_conn, new_end)
    finally:
        db_conn.close()
    LOG.info('Scheduler end.')
    sys.exit(load_result)


if __name__ == '__main__':
    _get_custom_config()
    LOG = create_loader_logger(config.LOADER_LOG_FILE)
    main()
