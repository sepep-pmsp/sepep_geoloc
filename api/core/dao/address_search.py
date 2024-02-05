from api.core.integrations import nominatim_address_search
from api.core.integrations import geosampa
from .parsers.nominatim import AddressParser
from typing import List

from api.core.utils.geo import convert_points_to_sirgas, geojson_envelop

class AddresSearch:

    def __init__(self):

        self.nominatim = nominatim_address_search
        self.nominatim_parser = AddressParser()
        self.geosampa = geosampa

    def nominatim_address_search(self, address:str)->List[dict]:

        resp = self.nominatim(address)
        geojson_data = self.nominatim_parser(resp)

        return geojson_data
    
    def geosampa_layer_query(self, point_geojson:dict, layer_name:str)->dict:

        x, y = convert_points_to_sirgas(point_geojson)

        return self.geosampa.point_within_pol(layer_name, x, y)
    
    def distrito(self, point_geojson:dict)->dict:

        return self.geosampa_layer_query(point_geojson, 'geoportal:distrito_municipal')

    def subprefeitura(self, point_geojson:dict)->dict:

        return self.geosampa_layer_query(point_geojson, 'geoportal:subprefeitura')
    
    def is_sp(self, address:dict)->bool:

        test_city = address['properties']['cidade']=='São Paulo'
        test_state = address['properties']['estado']=='São Paulo'
        test_country = address['properties']['codigo_pais']=='br'

        return test_city * test_state & test_country

    def filter_address_sp(self, address_geojson:list)->List:

        in_city = [add for add in address_geojson['features']
                if self.is_sp(add)]
        address_geojson['features'] = in_city


    def add_camadas_query(self, add_layer_data:dict, **camadas)->dict:

        if camadas:
            for camada_alias, camada_nome in camadas.items():
                endereco_feature = add_layer_data['endereco']['features'][0]
                add_layer_data[camada_alias] = self.geosampa_layer_query(endereco_feature, camada_nome)


    def address_feature_to_geojson(self, address_feat:dict, crs:dict)->dict:
        '''takes and anddress features and format it to a whole geojson'''
        
        #crs must be of t he whole geojson not of just one feature
        crs_num = int(crs['properties']['name'].split(':')[-1])
        
        return geojson_envelop([address_feat], crs_num)
    
    def __call__(self, address:str, **camadas)->[]:


        geoloc_resp = self.nominatim_address_search(address)
        self.filter_address_sp(geoloc_resp)
        nominatim_crs = geoloc_resp['crs']
        data = []
        #arrumar o endereco para ficar geojson
        for add in geoloc_resp['features']:
            
            add_layer_data = {
                'endereco' : self.address_feature_to_geojson(add, nominatim_crs),
                'distrito' : self.distrito(add),
                'subprefeitura' : self.subprefeitura(add),
            }

            self.add_camadas_query(add_layer_data, **camadas)

            data.append(add_layer_data)

        return data
            


    
    
    



