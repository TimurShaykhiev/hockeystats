from requests.exceptions import ConnectionError

from logger import get_loader_logger
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.team_sum_stat import TeamSumStat
from data_models.player_trade import PlayerTrade
from data_loaders.game_loader import get_games_list, get_game_info
from data_loaders.player_loader import get_players, create_player_link
from db_utils import get_columns_from_table
from db_utils.players import add_players, update_player_teams
from db_utils.seasons import get_season_by_date
from db_utils.player_trades import add_player_trades
import db_utils.add_stats as add_stats


LOG = get_loader_logger()
players = {}
all_games = []
all_skater_stats = []
all_goalie_stats = []
all_tga = []
all_penalty = []
all_goals = []
skater_sum_stats = {}
goalie_sum_stats = {}
team_sum_stats = {}
load_date = None

LOAD_RESULT_SUCCESS = 0
LOAD_RESULT_FAIL = 1
LOAD_RESULT_TRY_AGAIN = 2


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
    player_trades = []
    pt_dict = {}
    player_team_info = get_columns_from_table(db_conn, 'players', ['id', 'current_team_id'])
    # convert list to dict to improve search
    for info in player_team_info:
        pt_dict[info[0]] = info[1]

    for p in players.keys():
        if p in pt_dict:
            if players[p] != pt_dict[p]:
                # player in DB but contains another team id
                player_info_to_update.append((players[p], p))
                player_trades.append(PlayerTrade(p, load_date, pt_dict[p], players[p]))
        else:
            # no such player in DB
            player_ids_to_add.append(p)

    links = [create_player_link(pid) for pid in player_ids_to_add]
    new_players = get_players(links)

    num = add_players(db_conn, new_players)
    LOG.info('%s new players added', num if num else 0)
    num = update_player_teams(db_conn, player_info_to_update)
    LOG.info('%s players updated', num if num else 0)
    num = add_player_trades(db_conn, player_trades)
    LOG.info('%s player trades added', num if num else 0)


def _update_db(db_conn):
    _update_players(db_conn)
    with db_conn as cur:
        num = add_stats.add_games(cur, all_games)
        LOG.info('%s rows loaded into games', num if num else 0)
        num = add_stats.add_skater_stats(cur, all_skater_stats)
        LOG.info('%s rows loaded into skater_stats', num if num else 0)
        num = add_stats.add_goalie_stats(cur, all_goalie_stats)
        LOG.info('%s rows loaded into goalie_stats', num if num else 0)
        num = add_stats.add_goals(cur, all_goals)
        LOG.info('%s rows loaded into goals', num if num else 0)
        num = add_stats.add_penalty(cur, all_penalty)
        LOG.info('%s rows loaded into penalty', num if num else 0)
        num = add_stats.add_tga(cur, all_tga)
        LOG.info('%s rows loaded into take_give_away', num if num else 0)

        num = add_stats.update_skater_summary_stats(cur, skater_sum_stats)
        LOG.info('%s rows loaded into skater_sum_stats', num if num else 0)
        num = add_stats.update_goalie_summary_stats(cur, goalie_sum_stats)
        LOG.info('%s rows loaded into goalie_sum_stats', num if num else 0)
        num = add_stats.update_team_summary_stats(cur, team_sum_stats)
        LOG.info('%s rows loaded into team_sum_stats', num if num else 0)
    LOG.info('DB updates commit')
    cur.close()


def load(date, db_conn):
    global players, LOG, all_games, all_skater_stats, all_goalie_stats, all_goals, all_penalty, all_tga, load_date

    LOG.info('Load for %s', date)
    result = LOAD_RESULT_SUCCESS
    try:
        season = get_season_by_date(db_conn, date)
        if season is None:
            LOG.error('Date must belong to the season')
            return LOAD_RESULT_FAIL

        load_date = date
        game_links = get_games_list(date, date)
        for link in game_links:
            LOG.info('Process %s', link)
            game, skater_stats, goalie_stats, tga, penalty, goals = get_game_info(link)
            if len(skater_stats) == 0 or len(goalie_stats) == 0:
                LOG.warning('No stats in game info')
                raise UserWarning
            all_games.append(game)
            all_skater_stats += skater_stats
            all_goalie_stats += goalie_stats
            all_goals += goals
            all_penalty += penalty
            all_tga += tga

            for pl in skater_stats:
                players[pl.player.id] = pl.team.id
            for pl in goalie_stats:
                players[pl.player.id] = pl.team.id
            _update_skater_sum_stats(skater_stats, season, game.is_regular)
            _update_goalie_sum_stats(goalie_stats, season, game.is_regular)
            _update_team_sum_stats(game, season)

        if len(game_links) > 0:
            _update_db(db_conn)
    except ConnectionError:
        LOG.error('Connection error')
        result = LOAD_RESULT_TRY_AGAIN
    except:
        LOG.exception('Exception during data load')
        result = LOAD_RESULT_FAIL
    LOG.info('Script end with %s', 'success' if result == LOAD_RESULT_SUCCESS else 'fail')
    return result
