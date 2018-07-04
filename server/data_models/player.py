from collections import namedtuple

from logger import get_loader_logger
from data_models.entity_model import EntityModel
from data_models.team import Team
from data_models.query import Query
from data_models import convert_attr_if_none, convert_str_to_date

LOG = get_loader_logger()

# NHL position 'code' mapping to DB 'primary_pos' enum
PLAYER_POSITION = {
  'C': 'center',
  'R': 'right wing',
  'L': 'left wing',
  'D': 'defenseman',
  'G': 'goalie'
}

# NHL 'shootsCatches' mapping to DB 'shoots_catches' enum
PLAYER_SHOOTS = {
  'R': 'right',
  'L': 'left'
}


PlayerName = namedtuple('PlayerName', ['id', 'name'])
PlayerShortInfo = namedtuple('PlayerShortInfo', ['id', 'name', 'pos', 'tid'])


# convert height from string <6' 2"> to inches
def _convert_height(value):
    v = value.split(' ')
    feet = int(v[0][:-1])
    inches = int(v[1][:-1])
    return feet * 12 + inches


def _get_name_col(lang):
    if lang is None:
        return 'p.name'
    return 'tr.{}'.format(lang)


class Player(EntityModel):
    _table_name = 'players'
    _translate_join = 'JOIN translations tr ON p.id = tr.resource_id '
    _translate_where = ' AND tr.resource_type = "player_name"'

    CENTER = 'center'
    RIGHT_WING = 'right wing'
    LEFT_WING = 'left wing'
    DEFENSEMAN = 'defenseman'
    GOALIE = 'goalie'

    def __init__(self):
        self.id = None
        self.name = ''
        self.birth_date = None
        self.birth_city = ''
        self.birth_state = ''
        self.birth_country = ''
        self.nationality = ''
        self.height = 0
        self.weight = 0
        self.shoots_catches = ''
        self.primary_pos = ''
        self.current_team = None

    @classmethod
    def from_json(cls, obj):
        player = cls()
        player.id = obj['id']
        player.name = obj['fullName']
        player.birth_date = convert_str_to_date(obj.get('birthDate', '1900-01-01'))
        player.birth_city = obj.get('birthCity', player.birth_city)
        player.birth_country = obj.get('birthCountry', player.birth_country)
        player.birth_state = obj.get('birthStateProvince', player.birth_state)
        player.nationality = obj.get('nationality', player.nationality)
        height = obj.get('height')
        if height:
            player.height = _convert_height(obj.get('height'))
        player.weight = obj.get('weight', player.weight)
        shoots_catches = obj.get('shootsCatches')
        if shoots_catches is None:
            # This field is mandatory, but in rare cases it is missed in server response. Set it to 'L'.
            shoots_catches = 'L'
            LOG.warning('Player %s: shootsCatches is missed. Set to L.', player.id)
        player.shoots_catches = PLAYER_SHOOTS[shoots_catches]
        player.primary_pos = PLAYER_POSITION[obj['primaryPosition']['code']]
        team = obj.get('currentTeam')
        if team:
            player.current_team = Team()
            player.current_team.id = team['id']
        return player

    @classmethod
    def from_tuple(cls, fields):
        player = cls()
        player.id = fields[0]
        player.name = fields[1]
        player.birth_date = fields[2]
        player.birth_city = fields[3]
        player.birth_state = fields[4]
        player.birth_country = fields[5]
        player.nationality = fields[6]
        player.height = fields[7]
        player.weight = fields[8]
        player.shoots_catches = fields[9]
        player.primary_pos = fields[10]
        team_id = fields[11]
        if team_id:
            player.current_team = Team()
            player.current_team.id = team_id
        return player

    def to_tuple(self):
        return (self.id, self.name, self.birth_date, self.birth_city, self.birth_state, self.birth_country,
                self.nationality, self.height, self.weight, self.shoots_catches, self.primary_pos,
                self.current_team.id if self.current_team else None)

    def __str__(self):
        return '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
            self.id,
            self.name,
            self.birth_date,
            self.birth_city,
            self.birth_state,
            self.birth_country,
            self.nationality,
            self.height,
            self.weight,
            self.shoots_catches,
            self.primary_pos,
            convert_attr_if_none(self.current_team, 'id'))

    @classmethod
    def get_player(cls, db_conn, player_id, lang=None):
        if lang is None:
            return cls.from_db(db_conn, player_id)

        query = ('SELECT p.id, {}, p.birth_date, p.birth_city, p.birth_state, p.birth_country, p.nationality, '
                 'p.height, p.weight, p.shoots_catches, p.primary_pos, p.current_team_id '
                 'FROM players p ').format(_get_name_col(lang))
        query += cls._translate_join + 'WHERE p.id = %s' + cls._translate_where
        return cls._get_one_from_db(db_conn, query, (player_id,))

    @classmethod
    def get_players(cls, db_conn, player_ids, season_id, current, names_only, lang):
        named_tuple_cls = PlayerName if names_only else PlayerShortInfo
        if names_only or current:
            col_list = ('p.id, {}' if names_only else
                        'p.id, {}, p.primary_pos, p.current_team_id').format(_get_name_col(lang))
            query = 'SELECT {} FROM players p '.format(col_list)
            if lang is not None:
                query += cls._translate_join
            query += 'WHERE p.id IN ({})'.format(','.join(['%s'] * len(player_ids)))
            query_params = player_ids
        else:
            query = ('SELECT p.id, {}, p.primary_pos, pts.team_id FROM players p '
                     'JOIN player_team_season pts ON p.id = pts.player_id ').format(_get_name_col(lang))
            if lang is not None:
                query += cls._translate_join
            query += 'WHERE pts.season_id = %s AND p.id IN ({})'.format(','.join(['%s'] * len(player_ids)))
            query_params = [season_id] + player_ids
        if lang is not None:
            query += cls._translate_where
        return cls._get_columns_from_db(db_conn, query, query_params, named_tuple_cls=named_tuple_cls)

    @classmethod
    def get_skaters_for_season(cls, db_conn, season_id, regular, current, names_only, lang=None):
        return cls._get_players_for_season(db_conn, season_id, regular, current, names_only, 'skater_sum_stats', lang)

    @classmethod
    def get_goalies_for_season(cls, db_conn, season_id, regular, current, names_only, lang=None):
        return cls._get_players_for_season(db_conn, season_id, regular,  current, names_only, 'goalie_sum_stats', lang)

    @classmethod
    def _get_players_for_season(cls, db_conn, season_id, regular, current, names_only, sum_stat_table, lang):
        named_tuple_cls = PlayerName if names_only else PlayerShortInfo
        if names_only or current:
            col_list = ('p.id, {}' if names_only else
                        'p.id, {}, p.primary_pos, p.current_team_id').format(_get_name_col(lang))
            query = 'SELECT {} FROM players p JOIN {} s ON p.id = s.player_id '.format(col_list, sum_stat_table)
            if lang is not None:
                query += cls._translate_join
            query += 'WHERE s.season_id = %s AND s.is_regular = %s'
            query_params = (season_id, regular)
        else:
            query = ('SELECT p.id, {}, p.primary_pos, pts.team_id '
                     'FROM players p JOIN {} s ON p.id = s.player_id '
                     'JOIN player_team_season pts ON p.id = pts.player_id ').format(_get_name_col(lang), sum_stat_table)
            if lang is not None:
                query += cls._translate_join
            query += 'WHERE s.season_id = %s AND s.is_regular = %s AND pts.season_id = %s'
            query_params = (season_id, regular, season_id)
        if lang is not None:
            query += cls._translate_where
        return cls._get_columns_from_db(db_conn, query, query_params, named_tuple_cls=named_tuple_cls)

    @classmethod
    def get_player_for_season(cls, db_conn, player_id, season_id, current, lang=None):
        tid_col = 'p.current_team_id' if current else 'pts.team_id'
        query = ('SELECT p.id, {}, p.birth_date, p.birth_city, p.birth_state, p.birth_country, p.nationality, '
                 'p.height, p.weight, p.shoots_catches, p.primary_pos, {} '
                 'FROM players p ').format(_get_name_col(lang), tid_col)
        if not current:
            query += 'JOIN player_team_season pts ON p.id = pts.player_id '
        if lang is not None:
            query += cls._translate_join

        if current:
            query += 'WHERE p.id = %s'
            query_params = (player_id,)
        else:
            query += 'WHERE pts.season_id = %s AND p.id = %s'
            query_params = (season_id, player_id)
        if lang is not None:
            query += cls._translate_where
        return cls._get_one_from_db(db_conn, query, query_params)

    @classmethod
    def get_all_players_for_season(cls, db_conn, season_id, columns=None, named_tuple_cls=None):
        col_list = Query.get_col_list(columns, 'p')
        query = ('SELECT {} FROM players p JOIN skater_sum_stats s ON p.id = s.player_id '
                 'WHERE s.season_id = %s GROUP BY p.id UNION '
                 'SELECT {} FROM players p JOIN goalie_sum_stats g ON p.id = g.player_id '
                 'WHERE g.season_id = %s GROUP BY p.id').format(col_list, col_list)
        if columns is None:
            return cls._get_all_from_db(db_conn, query, (season_id, season_id))
        return cls._get_columns_from_db(db_conn, query, (season_id, season_id), named_tuple_cls=named_tuple_cls)

    @classmethod
    def get_team_players(cls, db_conn, team_id, season_id, current, columns, named_tuple_cls=None, lang=None):
        col_list = Query.get_col_list(columns, 'p')
        if lang is not None:
            col_list = col_list.replace('p.name', 'tr.{}'.format(lang))
        query = 'SELECT {} FROM players p '.format(col_list)
        if not current:
            query += 'JOIN player_team_season pts ON p.id = pts.player_id '
        if lang is not None:
            query += cls._translate_join

        if current:
            query += 'WHERE current_team_id = %s'
            query_params = (team_id,)
        else:
            query += 'WHERE pts.season_id = %s AND pts.team_id = %s'
            query_params = (season_id, team_id)
        if lang is not None:
            query += cls._translate_where
        return cls._get_columns_from_db(db_conn, query, query_params, named_tuple_cls=named_tuple_cls)

    @classmethod
    def get_player_season_team_map(cls, db_conn, player_id, all_seasons):
        # return dictionary (season_id : team_id) for player
        query = ('SELECT pts.season_id, pts.team_id, p.current_team_id FROM players p '
                 'JOIN player_team_season pts ON p.id = pts.player_id WHERE p.id = %s')
        season_team = cls._get_columns_from_db(db_conn, query, (player_id,))
        result = dict((sid, tid) for sid, tid, cur_tid in season_team)
        current_tid = 0
        if len(season_team) > 0:
            current_tid = season_team[0][2]

        for season in all_seasons:
            if season.id not in result:
                result[season.id] = current_tid
        return result
