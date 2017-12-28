import MySQLdb as Db

from data_loaders.sum_stats_loader import get_skater_sum_stats, get_goalie_sum_stats, get_team_sum_stats
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.team_sum_stat import TeamSumStat
from db_utils.fix_sum_stats import fix_skater_summary_stats, fix_goalie_summary_stats, fix_team_summary_stats

SEASON_ID = 5
NHL_SEASON = '20172018'
REGULAR = True

DIFF_ONLY = True


def _get_changes(db, loader_func, data_model_class, get_id_func):
    loaded_stats = loader_func(NHL_SEASON, REGULAR)
    db_stats_list = data_model_class.get_filtered(db, ['season_id', 'is_regular'], [SEASON_ID, REGULAR])
    print('Loaded {} from DB'.format(len(db_stats_list)))
    db_stats = dict((get_id_func(st), st) for st in db_stats_list)
    to_update = []
    for s in loaded_stats:
        if get_id_func(s) in db_stats:
            changed = db_stats[get_id_func(s)].compare(s)
            if changed is not None:
                to_update.append(changed)
    print('Find diffs in {} rows'.format(len(to_update)))
    return to_update


def main(db):
    """
    This script fixes skaters, goalies and teams summary statistics.
    """
    print('Skater loader')
    sk_to_update = _get_changes(db, get_skater_sum_stats, SkaterSumStat, lambda x: x.player.id)
    print('\nGoalie loader')
    g_to_update = _get_changes(db, get_goalie_sum_stats, GoalieSumStat, lambda x: x.player.id)
    print('\nTeam loader')
    teams_to_update = _get_changes(db, get_team_sum_stats, TeamSumStat, lambda x: x.team.id)

    if not DIFF_ONLY:
        print('\nDB update started')
        with db as cur:
            if len(sk_to_update) > 0:
                num = fix_skater_summary_stats(cur, sk_to_update)
                print('{} rows updated in skater_sum_stats'.format(num if num else 0))
            if len(g_to_update) > 0:
                num = fix_goalie_summary_stats(cur, g_to_update)
                print('{} rows updated in goalie_sum_stats'.format(num if num else 0))
            if len(teams_to_update) > 0:
                num = fix_team_summary_stats(cur, teams_to_update)
                print('{} rows updated in team_sum_stats'.format(num if num else 0))
        print('DB updates commit')
        cur.close()


if __name__ == '__main__':
    db_conn = Db.connect('localhost', 'hockstats', 'hockstats', 'NHL_STATS', charset='utf8')
    try:
        main(db_conn)
    finally:
        db_conn.close()
