from requests import Session, Response

from .query_builder import WithinQueryBuilder
from api.core.decorators.response_parsing import json_decode_error_handling

class GeoSampa:

    def __init__(self, host:str, version:str, default_precision:int)->None:

        self.host = host
        self.version = version
        self.base_url = self.build_base_url()

        self.session = Session()
        self.within_query = WithinQueryBuilder(self.version)

        self.precision = default_precision


    @json_decode_error_handling
    def wfs_geojson_request(self, request_url)->dict:

        with self.session.get(request_url) as r:
            return r

    def build_base_url(self)->str:
        
        base_params = f'?service=WFS&version={self.version}'

        return self.host + '/' + base_params
        
    def point_within_pol(self, camada:str, x:float, y:float, precision:float=None, geom_type='poligono')->dict:

        if precision is None:
            precision = self.precision

        query_args = self.within_query(camada, x, y, precision, geom_type)

        url = self.base_url + '&' + query_args

        print(f'Requesting geosampa: {url}')

        return self.wfs_geojson_request(url)