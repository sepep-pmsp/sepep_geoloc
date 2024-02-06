from api.core.integrations import geosampa
from api.core.utils.geo import convert_points_to_sirgas

class GeoSampaQuery:

    def __init__(self):

        self.geosampa = geosampa
    
    def geosampa_layer_query(self, point_geojson:dict, layer_name:str)->dict:

        x, y = convert_points_to_sirgas(point_geojson)

        return self.geosampa.point_within_pol(layer_name, x, y)
    
    def distrito(self, point_geojson:dict)->dict:

        return self.geosampa_layer_query(point_geojson, 'geoportal:distrito_municipal')

    def subprefeitura(self, point_geojson:dict)->dict:

        return self.geosampa_layer_query(point_geojson, 'geoportal:subprefeitura')

    def query_camadas(self, endereco_feature:dict, **camadas)->dict:
        '''endereco_feature must be a point geojson'''

        camadas_geosampa = dict()
        if camadas:
            for camada_alias, camada_nome in camadas.items():
                camadas_geosampa[camada_alias] = self.geosampa_layer_query(endereco_feature, camada_nome)

            return camadas_geosampa
        return {}
    
    def __call__(self, endereco_feature:dict, **camadas)->dict:

        return self.query_camadas(endereco_feature, **camadas)