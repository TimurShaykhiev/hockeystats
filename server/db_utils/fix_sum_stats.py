def fix_skater_summary_stats(db_cur, skater_sum_stats):
    num = db_cur.executemany(
        'UPDATE skater_sum_stats '
        'SET assists = %s, goals = %s, shots = %s, pp_goals = %s, pp_assists = %s, penalty_minutes = %s, '
        'sh_goals = %s, sh_assists = %s, plus_minus = %s, games = %s '
        'WHERE player_id = %s AND season_id = %s AND is_regular = %s', skater_sum_stats)
    return num


def fix_goalie_summary_stats(db_cur, goalie_sum_stats):
    num = db_cur.executemany(
        'UPDATE goalie_sum_stats '
        'SET assists = %s, goals = %s, penalty_minutes = %s, shots = %s, saves = %s, games = %s, shutout = %s '
        'WHERE player_id = %s AND season_id = %s AND is_regular = %s', goalie_sum_stats)
    return num


def fix_team_summary_stats(db_cur, team_sum_stats):
    num = db_cur.executemany(
        'UPDATE team_sum_stats '
        'SET goals_for = %s, goals_against = %s, games = %s '
        'WHERE team_id = %s AND season_id = %s AND is_regular = %s', team_sum_stats)
    return num
