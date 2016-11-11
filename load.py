import sys
import os
import logging
from logging.handlers import RotatingFileHandler
import MySQLdb as Db

from config import CONFIG
from data_models.game import Game
from data_models.skater_stat import SkaterStat
from data_models.goalie_stat import GoalieStat
from data_models.goal import Goal
from data_models.penalty import Penalty
from data_models.take_give_away import load_data_to_db as tga_load_data_to_db
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.team_sum_stat import TeamSumStat
from data_loaders import create_load_file
from data_loaders.game_loader import get_games_list, get_game_info
from data_loaders.player_loader import get_players, create_player_link
from db_utils.players import get_player_team_info, add_players, update_player_teams
from db_utils.seasons import get_season_by_date
from db_utils.summary_stats import update_skater_summary_stats, update_goalie_summary_stats, update_team_summary_stats


LOG_SIZE_LIMIT = 50*1024*1024
DB_GAME_TABLE = 'games'
DB_SKATER_STATS_TABLE = 'skater_stats'
DB_GOALIE_STATS_TABLE = 'goalie_stats'
DB_GOAL_TABLE = 'goals'
DB_PENALTY_TABLE = 'penalty'
DB_TGA_TABLE = 'take_give_away'


def _create_logger():
    logger = logging.getLogger('loader')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(filename)s] [%(levelname)s] %(message)s')

    rfh = RotatingFileHandler(CONFIG['loader_log_file'], maxBytes=LOG_SIZE_LIMIT, backupCount=5)
    rfh.setLevel(logging.DEBUG)
    rfh.setFormatter(formatter)
    logger.addHandler(rfh)
    return logger


def _create_data_files_dict(file_prefix):
    loader_dir = CONFIG['loader_data_dir']
    return {
        DB_GAME_TABLE: os.path.join(loader_dir, file_prefix + DB_GAME_TABLE),
        DB_SKATER_STATS_TABLE: os.path.join(loader_dir, file_prefix + DB_SKATER_STATS_TABLE),
        DB_GOALIE_STATS_TABLE: os.path.join(loader_dir, file_prefix + DB_GOALIE_STATS_TABLE),
        DB_GOAL_TABLE: os.path.join(loader_dir, file_prefix + DB_GOAL_TABLE),
        DB_PENALTY_TABLE: os.path.join(loader_dir, file_prefix + DB_PENALTY_TABLE),
        DB_TGA_TABLE: os.path.join(loader_dir, file_prefix + DB_TGA_TABLE)
    }


LOG = _create_logger()
DATA_FILES = {}
players = {}
skater_sum_stats = {}
goalie_sum_stats = {}
team_sum_stats = {}


# check that start and end date belong to the same season and return the season
def _get_season(db_conn, start, end):
    start_season = get_season_by_date(db_conn, start)
    if start_season:
        end_season = get_season_by_date(db_conn, end)
        if end_season and start_season.id == end_season.id:
            return start_season
    return None


def _update_skater_sum_stats(stats, season, regular):
    for st in stats:
        sum_st = skater_sum_stats.get((st.player.id, season.id, regular))
        if sum_st is None:
            sum_st = SkaterSumStat(st.player, season, regular)
        sum_st.add_stat(st, season.id, regular)
        skater_sum_stats[(st.player.id, season.id, regular)] = sum_st


def _update_goalie_sum_stats(stats, season, regular):
    for st in stats:
        sum_st = goalie_sum_stats.get((st.player.id, season.id, regular))
        if sum_st is None:
            sum_st = GoalieSumStat(st.player, season, regular)
        sum_st.add_stat(st, season.id, regular)
        goalie_sum_stats[(st.player.id, season.id, regular)] = sum_st


def _update_team_sum_stats(game, season):
    for team in [game.home.team, game.away.team]:
        sum_st = team_sum_stats.get((team.id, season.id, game.is_regular))
        if sum_st is None:
            sum_st = TeamSumStat(team, season, game.is_regular)
        sum_st.add_stat(game, team.id, season.id)
        team_sum_stats[(team.id, season.id, game.is_regular)] = sum_st


def _update_players(db_conn):
    player_ids_to_add = []
    player_info_to_update = []
    pt_dict = {}
    player_team_info = get_player_team_info(db_conn)
    # convert list to dict to improve search
    for info in player_team_info:
        pt_dict[info[0]] = info[1]

    for p in players.keys():
        if p in pt_dict:
            if players[p] != pt_dict[p]:
                # player in DB but contains another team id
                player_info_to_update.append((players[p], p))
        else:
            # no such player in DB
            player_ids_to_add.append(p)

    links = [create_player_link(pid) for pid in player_ids_to_add]
    new_players = get_players(links)

    num = add_players(db_conn, new_players)
    LOG.info('%s new players added', num if num else 0)
    num = update_player_teams(db_conn, player_info_to_update)
    LOG.info('%s players updated', num if num else 0)


def _update_db(db_conn):
    _update_players(db_conn)
    with db_conn as cur:
        num = Game.load_data_to_db(cur, DATA_FILES[DB_GAME_TABLE])
        LOG.info('%s rows loaded into games', num if num else 0)
        num = SkaterStat.load_data_to_db(cur, DATA_FILES[DB_SKATER_STATS_TABLE])
        LOG.info('%s rows loaded into skater_stats', num if num else 0)
        num = GoalieStat.load_data_to_db(cur, DATA_FILES[DB_GOALIE_STATS_TABLE])
        LOG.info('%s rows loaded into goalie_stats', num if num else 0)
        num = Goal.load_data_to_db(cur, DATA_FILES[DB_GOAL_TABLE])
        LOG.info('%s rows loaded into goals', num if num else 0)
        num = Penalty.load_data_to_db(cur, DATA_FILES[DB_PENALTY_TABLE])
        LOG.info('%s rows loaded into penalty', num if num else 0)
        num = tga_load_data_to_db(cur, DATA_FILES[DB_TGA_TABLE])
        LOG.info('%s rows loaded into take_give_away', num if num else 0)

        num = update_skater_summary_stats(cur, skater_sum_stats)
        LOG.info('%s rows loaded into skater_sum_stats', num if num else 0)
        num = update_goalie_summary_stats(cur, goalie_sum_stats)
        LOG.info('%s rows loaded into goalie_sum_stats', num if num else 0)
        num = update_team_summary_stats(cur, team_sum_stats)
        LOG.info('%s rows loaded into team_sum_stats', num if num else 0)
    LOG.info('DB updates commit')
    cur.close()


def load(start, end, db_conn):
    global DATA_FILES, players

    LOG.info('Load from %s to %s', start, end)
    result = True
    try:
        season = _get_season(db_conn, start, end)
        if season is None:
            LOG.error('Start and end dates must belong to the same season')
            sys.exit(-1)

        DATA_FILES = _create_data_files_dict('{}_{}_'.format(start, end))

        game_links = get_games_list(start, end)
        for link in game_links:
            LOG.info('Process %s', link)
            game, skater_stats, goalie_stats, tga, penalty, goals = get_game_info(link)
            create_load_file(DATA_FILES[DB_GAME_TABLE], [game])
            create_load_file(DATA_FILES[DB_SKATER_STATS_TABLE], skater_stats)
            create_load_file(DATA_FILES[DB_GOALIE_STATS_TABLE], goalie_stats)
            create_load_file(DATA_FILES[DB_GOAL_TABLE], goals)
            create_load_file(DATA_FILES[DB_PENALTY_TABLE], penalty)
            create_load_file(DATA_FILES[DB_TGA_TABLE], tga)

            for pl in skater_stats:
                players[pl.player.id] = pl.team.id
            for pl in goalie_stats:
                players[pl.player.id] = pl.team.id
            _update_skater_sum_stats(skater_stats, season, game.is_regular)
            _update_goalie_sum_stats(goalie_stats, season, game.is_regular)
            _update_team_sum_stats(game, season)

        _update_db(db_conn)
    except:
        LOG.exception('Exception during data load')
        result = False
    LOG.info('Script end with %s', 'success' if result else 'fail')
    return result


def main():
    LOG.info('Started with params %s', ', '.join(sys.argv))
    if len(sys.argv) < 3:
        print('You must pass start and end dates.')
        LOG.error('Invalid params')
        sys.exit(-1)

    start, end = sys.argv[1], sys.argv[2]

    db_conn = Db.connect('localhost', CONFIG['db_user'], CONFIG['db_password'], CONFIG['db_name'])
    try:
        load(start, end, db_conn)
    finally:
        db_conn.close()

if __name__ == '__main__':
    main()
