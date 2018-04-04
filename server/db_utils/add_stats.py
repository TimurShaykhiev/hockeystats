from db_utils import get_all_from_query_result
from data_models.skater_sum_stat import SkaterSumStat
from data_models.goalie_sum_stat import GoalieSumStat
from data_models.team_sum_stat import TeamSumStat


def add_games(db_cur, games):
    num = db_cur.executemany('INSERT INTO games (id, date, is_regular, win_type, home_team_id, away_team_id, '
                             'home_goals, home_goals_period1, home_goals_period2, home_goals_period3, home_shots, '
                             'home_pp_goals, home_pp_opportunities, home_face_off_wins, home_blocked, home_hits, '
                             'home_penalty_minutes, away_goals, away_goals_period1, away_goals_period2, '
                             'away_goals_period3, away_shots, away_pp_goals, away_pp_opportunities, '
                             'away_face_off_wins, away_blocked, away_hits, away_penalty_minutes, face_off_taken) '
                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
                             '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                             [g.to_tuple() for g in games])
    return num


def add_skater_stats(db_cur, skater_stats):
    num = db_cur.executemany('INSERT INTO skater_stats (player_id, team_id, game_id, date, assists, goals, shots, '
                             'hits, pp_goals, pp_assists, penalty_minutes, face_off_wins, face_off_taken, takeaways, '
                             'giveaways, sh_goals, sh_assists, blocked, plus_minus, toi, even_toi, pp_toi, sh_toi) '
                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
                             '%s, %s, %s, %s, %s, %s, %s, %s, %s)', [sk.to_tuple() for sk in skater_stats])
    return num


def add_goalie_stats(db_cur, goalie_stats):
    num = db_cur.executemany('INSERT INTO goalie_stats (player_id, team_id, game_id, date, toi, assists, goals, '
                             'penalty_minutes, shots, saves, pp_saves, sh_saves, even_saves, sh_shots_against, '
                             'even_shots_against, pp_shots_against, decision) '
                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '
                             '%s, %s, %s)', [gl.to_tuple() for gl in goalie_stats])
    return num


def add_goals(db_cur, goals):
    num = db_cur.executemany('INSERT INTO goals (team_id, game_id, date, scorer_id, assist1_id, assist2_id, '
                             'secondary_type, empty_net, strength, period_num, period_time, coord_x, coord_y) '
                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                             [gl.to_tuple() for gl in goals])
    return num


def add_penalty(db_cur, penalty):
    num = db_cur.executemany('INSERT INTO penalty (team_id, game_id, date, penalty_on_id, drew_by_id, penalty_minutes, '
                             'secondary_type, period_num, period_time, coord_x, coord_y) '
                             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                             [p.to_tuple() for p in penalty])
    return num


def update_skater_summary_stats(db_cur, skater_sum_stats):
    num = 0
    for pl_id, season_id, regular in skater_sum_stats.keys():
        db_cur.execute('SELECT * FROM skater_sum_stats WHERE player_id = %s AND season_id = %s AND is_regular = %s',
                       [pl_id, season_id, regular])
        res = get_all_from_query_result(SkaterSumStat, db_cur)
        if len(res) > 0:
            stat = res[0]
            stat.add_sum_stat(skater_sum_stats[(pl_id, season_id, regular)])
            fields = list(stat.to_tuple())
            fields = fields[3:] + fields[:3]
            num += db_cur.execute(
                'UPDATE skater_sum_stats '
                'SET assists = %s, goals = %s, shots = %s, hits = %s, pp_goals = %s, pp_assists = %s, '
                'penalty_minutes = %s, face_off_wins = %s, face_off_taken = %s, takeaways = %s, '
                'giveaways = %s, sh_goals = %s, sh_assists = %s, blocked = %s, plus_minus = %s, '
                'toi = %s, even_toi = %s, pp_toi = %s, sh_toi = %s, games = %s '
                'WHERE player_id = %s AND season_id = %s AND is_regular = %s', fields)
        else:
            num += db_cur.execute(
                'INSERT INTO skater_sum_stats (player_id, season_id, is_regular, assists, goals, shots, hits, '
                'pp_goals, pp_assists, penalty_minutes, face_off_wins, face_off_taken, takeaways, giveaways, '
                'sh_goals, sh_assists, blocked, plus_minus, toi, even_toi, pp_toi, sh_toi, games) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                skater_sum_stats[(pl_id, season_id, regular)].to_tuple())
    return num


def update_goalie_summary_stats(db_cur, goalie_sum_stats):
    num = 0
    for pl_id, season_id, regular in goalie_sum_stats.keys():
        db_cur.execute('SELECT * FROM goalie_sum_stats WHERE player_id = %s AND season_id = %s AND is_regular = %s',
                       [pl_id, season_id, regular])
        res = get_all_from_query_result(GoalieSumStat, db_cur)
        if len(res) > 0:
            stat = res[0]
            stat.add_sum_stat(goalie_sum_stats[(pl_id, season_id, regular)])
            fields = list(stat.to_tuple())
            fields = fields[3:] + fields[:3]
            num += db_cur.execute(
                'UPDATE goalie_sum_stats '
                'SET toi = %s, assists = %s, goals = %s, penalty_minutes = %s, shots = %s, saves = %s, '
                'pp_saves = %s, sh_saves = %s, even_saves = %s, sh_shots_against = %s, '
                'even_shots_against = %s, pp_shots_against = %s, games = %s, wins = %s, shutout = %s '
                'WHERE player_id = %s AND season_id = %s AND is_regular = %s', fields)
        else:
            num += db_cur.execute(
                'INSERT INTO goalie_sum_stats (player_id, season_id, is_regular, toi, assists, goals, penalty_minutes, '
                'shots, saves, pp_saves, sh_saves, even_saves, sh_shots_against, even_shots_against, pp_shots_against, '
                'games, wins, shutout) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                goalie_sum_stats[(pl_id, season_id, regular)].to_tuple())
    return num


def update_team_summary_stats(db_cur, team_sum_stats):
    num = 0
    for team_id, season_id, regular in team_sum_stats.keys():
        db_cur.execute('SELECT * FROM team_sum_stats WHERE team_id = %s AND season_id = %s AND is_regular = %s',
                       [team_id, season_id, regular])
        res = get_all_from_query_result(TeamSumStat, db_cur)
        if len(res) > 0:
            stat = res[0]
            stat.add_sum_stat(team_sum_stats[(team_id, season_id, regular)])
            fields = list(stat.to_tuple())
            fields = fields[3:] + fields[:3]
            num += db_cur.execute(
                'UPDATE team_sum_stats '
                'SET goals_for = %s, goals_against = %s, shots = %s, pp_goals = %s, '
                'pp_opportunities = %s, sh_goals_against = %s, sh_opportunities = %s, '
                'face_off_wins = %s, face_off_taken = %s, blocked = %s, '
                'hits = %s, penalty_minutes = %s, games = %s, win_regular = %s, win_overtime = %s, '
                'win_shootout = %s, lose_regular = %s, lose_overtime = %s, lose_shootout = %s '
                'WHERE team_id = %s AND season_id = %s AND is_regular = %s', fields)
        else:
            num += db_cur.execute(
                'INSERT INTO team_sum_stats (team_id, season_id, is_regular, goals_for, goals_against, shots, '
                'pp_goals, pp_opportunities, sh_goals_against, sh_opportunities, face_off_wins, face_off_taken, '
                'blocked, hits, penalty_minutes, games, win_regular, win_overtime, win_shootout, lose_regular, '
                'lose_overtime, lose_shootout) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                team_sum_stats[(team_id, season_id, regular)].to_tuple())
    return num
