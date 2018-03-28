import functools
from collections import namedtuple

from marshmallow import fields

from app.database import get_db
from data_models.division import Division
from data_models.team import Team as TeamDm
from data_models.game import Game
from data_models.team_sum_stat import TeamSumStat
from statistics.team_season import get_standings_stats
from statistics.games import get_tie_breaking_info
from .season import SeasonSchema
from . import ModelSchema, StatValue

_DivStandings = namedtuple('_DivStandings', ['did', 'teams'])
_ConfStandings = namedtuple('_ConfStandings', ['cid', 'teams'])
_WcStandings = namedtuple('_WcStandings', ['cid', 'div1', 'div2', 'wc'])

'''
From NHL official site: Tie-Breaking Procedure.

If two or more clubs are tied in points during the regular season, the standing of the clubs is determined in the
following order:
1. The fewer number of games played (i.e., superior points percentage).
2. The greater number of games won, excluding games won in the Shootout.
3. The greater number of points earned in games between the tied clubs. If two clubs are tied, and have not played an
   equal number of home games against each other, points earned in the first game played in the city that had the extra
   game shall not be included. If more than two clubs are tied, the higher percentage of available points earned in
   games among those clubs, and not including any "odd" games, shall be used to determine the standing.
4. The greater differential between goals for and against for the entire regular season.

NOTE: In standings a victory in a shootout counts as one goal for, while a shootout loss counts as one goal against.
'''


def _filter_conf(stats, cid):
    return [x for x in stats if x.cid == cid]


def _filter_div(stats, did):
    return [x for x in stats if x.did == did]


def _get_ids(stats):
    return [x.tid for x in stats]


class Standings:
    def __init__(self, season):
        self.season = season
        self.league = []
        self.conferences = []
        self.divisions = []
        self.wild_cards = []
        self._stats = None
        self._divisions = set()
        self._conferences = set()
        self._conf_div = set()
        self._ties = dict()
        self._tie_breaking_info = None
        self._team_key_fn = functools.cmp_to_key(self._team_cmp)

    def _prepare_data(self, db):
        div_map = dict((el.id, el) for el in Division.get_all(db))
        teams = TeamDm.get_for_season(db, self.season.id, columns=['id', 'division_id'])
        team_info = dict((tid, [div_map[did].conference.id, did]) for tid, did in teams)
        stats_from_db = TeamSumStat.get_stat_tuples(db, self.season.id, True)
        self._stats = get_standings_stats(stats_from_db, team_info)
        for s in self._stats:
            self._divisions.add(s.did)
            self._conferences.add(s.cid)
            self._conf_div.add((s.cid, s.did))

        # check if we need additional data to resolve ties
        self._stats.sort(key=self._team_key_fn)
        if len(self._ties) > 0:
            team_ids = [list(v) for v in self._ties.values()]
            games = Game.get_head_to_head_games(db, team_ids, self.season.start, self.season.end)
            self._tie_breaking_info = get_tie_breaking_info(games, team_ids)

    def get_wild_cards(self, db):
        if self._stats is None:
            self._prepare_data(db)
        res = []
        for cid in self._conferences:
            div = [(d, _filter_div(self._stats, d)) for c, d in self._conf_div if c == cid]
            # get division top 3
            div1_st = sorted(div[0][1], key=self._team_key_fn)
            div1 = _DivStandings(div[0][0], _get_ids(div1_st[:3]))
            # get division top 3
            div2_st = sorted(div[1][1], key=self._team_key_fn)
            div2 = _DivStandings(div[1][0], _get_ids(div2_st[:3]))
            # get rest conference teams
            wc = sorted(div1_st[3:] + div2_st[3:], key=self._team_key_fn)
            res.append(_WcStandings(cid, div1, div2, _get_ids(wc)))
        return res

    def get_data(self):
        db = get_db()
        self._prepare_data(db)

        self._stats.sort(key=self._team_key_fn)
        self.league = _get_ids(self._stats)

        for cid in self._conferences:
            st = _filter_conf(self._stats, cid)
            st.sort(key=self._team_key_fn)
            self.conferences.append(_ConfStandings(cid, _get_ids(st)))

        for did in self._divisions:
            st = _filter_div(self._stats, did)
            st.sort(key=self._team_key_fn)
            self.divisions.append(_DivStandings(did, _get_ids(st)))

        self.wild_cards = self.get_wild_cards(db)

        schema = _StandingsSchema()
        return schema.dumps(self)

    def _team_cmp(self, a, b):
        # 0
        res = b.points - a.points
        if res != 0:
            return res
        # 1
        res = a.games - b.games
        if res != 0:
            return res
        # 2
        res = b.wins - a.wins
        if res != 0:
            return res
        # 3. To check this condition we need games info
        if self._tie_breaking_info is not None:
            res = self._tie_breaking_info[b.tid] - self._tie_breaking_info[a.tid]
            if res != 0:
                return res
        elif a.games > 20:
            # it makes no sense to do these check when too few games are played
            key = (a.points, a.games, a.wins)
            if key not in self._ties:
                self._ties[key] = set()
            self._ties[key].add(a.tid)
            self._ties[key].add(b.tid)
        # 4
        return b.diff - a.diff


class _DivStandingsSchema(ModelSchema):
    did = fields.Integer()
    teams = fields.List(StatValue())


class _ConfStandingsSchema(ModelSchema):
    cid = fields.Integer()
    teams = fields.List(StatValue())


class _WildCardStandingsSchema(ModelSchema):
    cid = fields.Integer()
    div1 = fields.Nested(_DivStandingsSchema)
    div2 = fields.Nested(_DivStandingsSchema)
    wc = fields.List(StatValue())


class _StandingsSchema(ModelSchema):
    season = fields.Nested(SeasonSchema)
    league = fields.List(StatValue())
    conferences = fields.Nested(_ConfStandingsSchema, many=True)
    divisions = fields.Nested(_DivStandingsSchema, many=True)
    wildCards = fields.Nested(_WildCardStandingsSchema, many=True, attribute='wild_cards')
