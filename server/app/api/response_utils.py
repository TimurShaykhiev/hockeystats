from flask import jsonify, make_response

from .error_codes import API_ERRORS

CACHE_TYPE_CURRENT_SEASON_STATS = 0
CACHE_TYPE_OLD_SEASON_STATS = 1


def response(data, cache_type):
    resp = make_response(data)
    resp.headers['Content-Type'] = 'application/json'
    _add_cache_headers(resp, cache_type)
    return resp


class ApiError(Exception):
    def __init__(self, status_code, api_err_code):
        Exception.__init__(self)
        self.status_code = status_code
        self.api_err_code = api_err_code

    def get_response(self):
        return make_response(jsonify({'error': API_ERRORS[self.api_err_code]}), self.status_code)


class InvalidQueryParams(ApiError):
    def __init__(self):
        super().__init__(400, 'INVALID_QUERY_PARAMS')


def _add_cache_headers(resp, cache_type):
    if cache_type == CACHE_TYPE_OLD_SEASON_STATS:
        # This info won't be changed. Expiration time: 1 year.
        resp.headers['Cache-Control'] = 'public, max-age=31536000'
    elif cache_type == CACHE_TYPE_CURRENT_SEASON_STATS:
        # This info is changed every day. Expiration time: 1 hour.
        resp.headers['Cache-Control'] = 'public, max-age=3600'
