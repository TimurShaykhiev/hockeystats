from logger import get_loader_logger
from db_utils.seasons import get_2_last_seasons, set_new_current_season, update_season_status

LOG = get_loader_logger()


def check_season(db_conn, today):
    last, prev = get_2_last_seasons(db_conn)
    with db_conn as cur:
        if last.status == last.STATUS_NOT_STARTED:
            if last.start <= today:
                set_new_current_season(cur, prev.id, last.id)
                LOG.info('New season is started. Set new current season.')
        elif last.current:
            if last.po_start <= today and last.status == last.STATUS_REGULAR:
                update_season_status(cur, last.id, last.STATUS_PLAY_OFF)
                LOG.info('Play-off is started.')
            elif last.end <= today and last.status == last.STATUS_PLAY_OFF:
                update_season_status(cur, last.id, last.STATUS_FINISHED)
                LOG.info('Season is finished.')
        else:
            LOG.warn('Check seasons table. Last season is not current as expected.')
    cur.close()
