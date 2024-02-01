import json
from requests import Response

def json_resp_decode_error(resp:Response)->dict:

    try:
        return resp.json()
    except json.JSONDecodeError:
        try:
            return {'erro' : resp.txt,
                    'tipo_erro' : 'JsonDecodeError'}
        except AttributeError:
            return {'erro' : str(resp.content),
                    'tipo_erro' : 'JsonDecodeError'}