import requests
from lambda_decorators import (load_json_body, json_http_resp, on_exception, cors_headers)

@on_exception
def handle_errors(e):
    resp = {}
    if e.response.status_code:
        # if we have a status code, use it
        resp = {'statusCode': e.response.status_code, 'body': str(e) }
    else:
        # otherwise just use 400
        resp = {'statusCode': 400, 'body': str(e) }
    print(resp)
    return resp
    

@cors_headers
@handle_errors
@json_http_resp
@load_json_body
def handler(event, context):
    r = requests.get('http://worldtimeapi.org/api/fails')

    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise err

    return r.json()