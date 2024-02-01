import json
from requests import Response

def json_resp_decode_error(resp:Response)->dict:

    try:
        return resp.json()
    except json.JSONDecodeError:
        return {'erro' : resp.txt}