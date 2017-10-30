from flask import jsonify, make_response

from .error_codes import API_ERRORS


def response(data):
    resp = make_response(data)
    resp.headers['Content-Type'] = 'application/json'
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
