from db_utils import get_all_from_query_result
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.team_sum_stat import TeamSumStat


def get_all_skaters_sum_stats(db, season_id, regular):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM skater_sum_stats WHERE season_id = %s AND is_regular = %s', [season_id, regular])
        return get_all_from_query_result(SkaterSumStat, cur)


def get_all_goalies_sum_stats(db, season_id, regular):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM goalie_sum_stats WHERE season_id = %s AND is_regular = %s', [season_id, regular])
        return get_all_from_query_result(GoalieSumStat, cur)


def get_all_teams_sum_stats(db, season_id, regular):
    with db.cursor() as cur:
        cur.execute('SELECT * FROM team_sum_stats WHERE season_id = %s AND is_regular = %s', [season_id, regular])
        return get_all_from_query_result(TeamSumStat, cur)
