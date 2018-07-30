from collections import namedtuple

import requests

REST_API_FILE = 'test_rest_api.http'

ApiRequest = namedtuple('ApiRequest', ['name', 'url', 'response_code'])


def _get_requests():
    def _req_default_params():
        return '', None, 200

    req = []
    with open(REST_API_FILE, 'r') as f:
        name, url, response_code = _req_default_params()
        for line in f:
            if line.startswith('###'):
                # New request
                if url is not None:
                    req.append(ApiRequest(name, url, response_code))
                name, url, response_code = _req_default_params()
                name = line[4:-1]
            elif line.startswith('GET'):
                url = line[4:-1]
            elif line.startswith('# Response code:'):
                response_code = int(line[17:])
    return req


def main():
    passed = 0
    failed = 0
    req = _get_requests()
    for r in req:
        response = requests.get(r.url)
        ok = response.status_code == r.response_code
        if ok:
            passed += 1
            print('Test: {}. Passed.\n'.format(r.name))
        else:
            failed += 1
            print('Test: {}. Failed.'.format(r.name))
            print('URL: {}. Expected: {}.  Actual: {}.\n'.format(r.url, r.response_code, response.status_code))
    print('===========================')
    print('Test run complete. Passed: {}. Failed: {}.'.format(passed, failed))


if __name__ == '__main__':
    main()
