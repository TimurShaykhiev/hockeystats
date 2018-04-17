import MySQLdb as Db
import numpy as np

from statistics import percentage
import statistics.skater_season as skater_col
import statistics.goalie_season as goalie_col
import statistics.team_season as team_col

SKATER_QUERY = 'SELECT * FROM skater_sum_stats WHERE is_regular=1'
GOALIE_QUERY = 'SELECT * FROM goalie_sum_stats WHERE is_regular=1'
TEAM_QUERY = 'SELECT * FROM team_sum_stats WHERE is_regular=1'

TABLE_TEMPLATE = '{:<20}{:>15}{:>15}{:>15}{:>15}{:>15}{:>15}{:>15}{:>15}'


def _get_all(db, query):
    with db.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def _print_range(col_data, col_name):
    col_min = round(np.min(col_data))
    col_2p = round(np.percentile(col_data, 2))
    col_5p = round(np.percentile(col_data, 5))
    col_10p = round(np.percentile(col_data, 10))
    col_90p = round(np.percentile(col_data, 90))
    col_95p = round(np.percentile(col_data, 95))
    col_98p = round(np.percentile(col_data, 98))
    col_max = round(np.max(col_data))
    print(TABLE_TEMPLATE.format(col_name, col_min, col_2p, col_5p, col_10p, col_90p, col_95p, col_98p, col_max))


def _get_skater_stats_ranges(db):
    db_data = _get_all(db, SKATER_QUERY)
    arr = np.array(db_data)
    _print_range(arr[:, skater_col.COL_GOALS], 'goals')
    _print_range(arr[:, skater_col.COL_ASSISTS], 'assists')
    _print_range(arr[:, skater_col.COL_PLUS_MINUS], 'plus-minus')
    _print_range(arr[:, skater_col.COL_TAKEAWAYS] - arr[:, skater_col.COL_GIVEAWAYS], 'turnover')
    _print_range(arr[:, skater_col.COL_PENALTY_MINUTES], 'penalty minutes')
    _print_range(percentage(arr[:, skater_col.COL_FACE_OFF_WINS], arr[:, skater_col.COL_FACE_OFF_TAKEN]), 'FOW%')
    _print_range(arr[:, skater_col.COL_SHOTS], 'shots')
    _print_range(arr[:, skater_col.COL_HITS], 'hits')
    _print_range(arr[:, skater_col.COL_PP_GOALS], 'PP goals')
    _print_range(arr[:, skater_col.COL_PP_ASSISTS], 'PP assists')
    _print_range(arr[:, skater_col.COL_SH_GOALS], 'SH goals')
    _print_range(arr[:, skater_col.COL_SH_ASSISTS], 'SH assists')
    _print_range(arr[:, skater_col.COL_BLOCKED], 'blocks')
    _print_range(arr[:, skater_col.COL_TOI], 'TOI')
    _print_range(arr[:, skater_col.COL_EVEN_TOI], 'even TOI')
    _print_range(arr[:, skater_col.COL_PP_TOI], 'PP TOI')
    _print_range(arr[:, skater_col.COL_SH_TOI], 'SH TOI')
    _print_range(arr[:, skater_col.COL_GAMES], 'games')


def _get_goalie_stats_ranges(db):
    db_data = _get_all(db, GOALIE_QUERY)
    arr = np.array(db_data)
    _print_range(arr[:, goalie_col.COL_TOI], 'TOI')
    _print_range(arr[:, goalie_col.COL_ASSISTS], 'assists')
    _print_range(arr[:, goalie_col.COL_GOALS], 'goals')
    _print_range(arr[:, goalie_col.COL_PENALTY_MINUTES], 'penalty minutes')
    _print_range(arr[:, goalie_col.COL_SHOTS], 'shots')
    _print_range(arr[:, goalie_col.COL_SAVES], 'saves')
    _print_range(arr[:, goalie_col.COL_PP_SAVES], 'PP saves')
    _print_range(arr[:, goalie_col.COL_SH_SAVES], 'SH saves')
    _print_range(arr[:, goalie_col.COL_EVEN_SAVES], 'even saves')
    _print_range(arr[:, goalie_col.COL_SH_SHOTS_AGAINST], 'SH SA')
    _print_range(arr[:, goalie_col.COL_EVEN_SHOTS_AGAINST], 'even SA')
    _print_range(arr[:, goalie_col.COL_PP_SHOTS_AGAINST], 'PP SA')
    _print_range(arr[:, goalie_col.COL_GAMES], 'games')
    _print_range(arr[:, goalie_col.COL_WINS], 'wins')
    _print_range(arr[:, goalie_col.COL_SHUTOUT], 'shutout')


def _get_team_stats_ranges(db):
    db_data = _get_all(db, TEAM_QUERY)
    arr = np.array(db_data)
    _print_range(arr[:, team_col.COL_GOALS_FOR], 'goals for')
    _print_range(arr[:, team_col.COL_GOALS_AGAINST], 'goals against')
    _print_range(arr[:, team_col.COL_SHOTS], 'shots')
    _print_range(arr[:, team_col.COL_PP_GOALS], 'PP goals')
    _print_range(arr[:, team_col.COL_PP_OPPORTUNITIES], 'PP opp')
    _print_range(arr[:, team_col.COL_SH_GOALS_AGAINST], 'SH GA')
    _print_range(arr[:, team_col.COL_SH_OPPORTUNITIES], 'SH opp')
    _print_range(percentage(arr[:, team_col.COL_PP_GOALS], arr[:, team_col.COL_PP_OPPORTUNITIES]), 'PP%')
    _print_range(100 - percentage(arr[:, team_col.COL_SH_GOALS_AGAINST], arr[:, team_col.COL_SH_OPPORTUNITIES]), 'PK%')
    _print_range(percentage(arr[:, team_col.COL_FACE_OFF_WINS], arr[:, team_col.COL_FACE_OFF_TAKEN]), 'FOW%')
    _print_range(arr[:, team_col.COL_BLOCKED], 'blocks')
    _print_range(arr[:, team_col.COL_HITS], 'hits')
    _print_range(arr[:, team_col.COL_PENALTY_MINUTES], 'penalty minutes')
    _print_range(arr[:, team_col.COL_WIN_REGULAR], 'win R')
    _print_range(arr[:, team_col.COL_WIN_OVERTIME], 'win OT')
    _print_range(arr[:, team_col.COL_WIN_SHOOTOUT], 'win SO')
    _print_range(arr[:, team_col.COL_LOSE_REGULAR], 'lose R')
    _print_range(arr[:, team_col.COL_LOSE_OVERTIME], 'lose OT')
    _print_range(arr[:, team_col.COL_LOSE_SHOOTOUT], 'lose SO')


def main(db):
    """
    This script gets skaters, goalies and teams statistic values ranges.
    """
    header = TABLE_TEMPLATE.format('Name', 'Min', '2p', '5p', '10p', '90p', '95p', '98p', 'Max')
    print('Skater stats ranges')
    print(header)
    _get_skater_stats_ranges(db)
    print('\nGoalie stats ranges')
    print(header)
    _get_goalie_stats_ranges(db)
    print('\nTeam stats ranges')
    print(header)
    _get_team_stats_ranges(db)


if __name__ == '__main__':
    db_conn = Db.connect(host='localhost', user='hockstats', password='hockstats', database='NHL_STATS', charset='utf8')
    try:
        main(db_conn)
    finally:
        db_conn.close()
