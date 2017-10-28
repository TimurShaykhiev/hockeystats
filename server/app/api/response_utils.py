from flask import jsonify, make_response


def response(data):
    resp = make_response(data)
    resp.headers['Content-Type'] = 'application/json'
    return resp


def error(http_err_code, api_err_code):
    return make_response(jsonify({'error': api_err_code}), http_err_code)
