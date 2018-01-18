from data_models.player import Player
from data_models.player_trade import PlayerTrade


def get_team_players(db, team_id, season):
    """
    Returns a list of player ids.
    """
    if season.current:
        # There is no need to check trades for current season
        players = Player.get_filtered(db, ['current_team_id'], [team_id], columns=['id'])
        return [p[0] for p in players]

    pl_trades = PlayerTrade.get_for_team(db, team_id)
    trades = {}
    for t in pl_trades:
        if t.player_id not in trades:
            trades[t.player_id] = []
        trades[t.player_id].append(t)
    players = Player.get_ever_played_in_team(db, team_id, list(trades.keys()), columns=['id', 'current_team_id'])
    result = []
    for pid, tid in players:
        actual_tid = tid
        if pid in trades:
            actual_tid = get_player_team_for_season(tid, season, trades[pid])
        if actual_tid == team_id:
            result.append(pid)
    return result


def get_player_team_for_season(current_tid, season, trades):
    if season is None or len(trades) == 0:
        return current_tid
    new_tid = None
    for tr in trades:
        if tr.date < season.end:
            new_tid = tr.to_team
        if tr.date >= season.end:
            new_tid = tr.from_team
            break
    return new_tid


def get_player_season_team_map(current_tid, player_trades_it, all_seasons_it):
    """
    :param current_tid: Player current team id.
    :param player_trades_it: Player trades iterator(sorted by date).
    :param all_seasons_it: Seasons iterator(sorted by date).
    :return: dictionary (season_id : team_id) for player.
    """
    result = {}
    tid = current_tid
    trade = next(player_trades_it, None)
    if trade is not None:
        tid = trade.from_team
    for season in all_seasons_it:
        while trade is not None and trade.date < season.end:
            to_team = trade.to_team
            trade = next(player_trades_it, None)
            tid = trade.from_team if trade is not None else to_team
        result[season.id] = tid
    return result
