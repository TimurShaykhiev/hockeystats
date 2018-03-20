from logger import get_loader_logger
from data_loaders.sum_stats_loader import get_skater_sum_stats, get_goalie_sum_stats, get_team_sum_stats
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.team_sum_stat import TeamSumStat
from data_models.season import Season
from db_utils.fix_sum_stats import fix_skater_summary_stats, fix_goalie_summary_stats, fix_team_summary_stats
from db_utils.seasons import get_season_by_date

LOG = get_loader_logger()


def _get_changes(db, loader_func, data_model_class, get_id_func, season, nhl_season):
    regular = season.status == Season.STATUS_REGULAR
    loaded_stats = loader_func(nhl_season, regular)
    db_stats_list = data_model_class.get_filtered(db, ['season_id', 'is_regular'], [season.id, regular])
    LOG.info('Loaded {} from DB'.format(len(db_stats_list)))
    db_stats = dict((get_id_func(st), st) for st in db_stats_list)
    to_update = []
    for s in loaded_stats:
        if get_id_func(s) in db_stats:
            changed = db_stats[get_id_func(s)].compare(s)
            if changed is not None:
                to_update.append(changed)
    LOG.info('Find diffs in {} rows'.format(len(to_update)))
    return to_update


def fix_sum_stats(db, today):
    if today.day % 5 != 0:
        return

    season = get_season_by_date(db, today)
    year = season.end.year
    nhl_season = '{}{}'.format(year - 1, year)

    LOG.info('Skater loader')
    sk_to_update = _get_changes(db, get_skater_sum_stats, SkaterSumStat, lambda x: x.player.id, season, nhl_season)
    LOG.info('Goalie loader')
    g_to_update = _get_changes(db, get_goalie_sum_stats, GoalieSumStat, lambda x: x.player.id, season, nhl_season)
    LOG.info('Team loader')
    teams_to_update = _get_changes(db, get_team_sum_stats, TeamSumStat, lambda x: x.team.id, season, nhl_season)

    LOG.info('DB update started')
    with db as cur:
        if len(sk_to_update) > 0:
            num = fix_skater_summary_stats(cur, sk_to_update)
            LOG.info('{} rows updated in skater_sum_stats'.format(num if num else 0))
        if len(g_to_update) > 0:
            num = fix_goalie_summary_stats(cur, g_to_update)
            LOG.info('{} rows updated in goalie_sum_stats'.format(num if num else 0))
        if len(teams_to_update) > 0:
            num = fix_team_summary_stats(cur, teams_to_update)
            LOG.info('{} rows updated in team_sum_stats'.format(num if num else 0))
    LOG.info('DB updates commit')
    cur.close()
