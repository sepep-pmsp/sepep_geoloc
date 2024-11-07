from core.integrations import nominatim_address_search
from core.integrations import azure_maps_address_search
from .parsers.nominatim import AddressParser as NominatimAdressParser
from .parsers.azure import AddressParser as AzureAdressParser
from .geosampa import geosampa_address_query
from core.utils.geo import geojson_envelop

from typing import List

from config import USE_AZURE

class AddresSearch:

    def __init__(self, use_azure=USE_AZURE):

        self.nominatim = nominatim_address_search
        self.nominatim_parser = NominatimAdressParser()
        self.geosampa_query = geosampa_address_query

        self.use_azure = use_azure
        if self.use_azure:
            #só vou definir aqui no if mesmo porque quero que dê erro
            #caso use a azure e não estiver especificado para usar
            self.azure = azure_maps_address_search
            self.azure_parser = AzureAdressParser()

    def nominatim_address_search(self, address:str)->List[dict]:

        resp = self.nominatim(address)
        geojson_data = self.nominatim_parser(resp)

        return geojson_data
    
    def azure_address_search(self, address:str)->List[dict]:

        resp = self.azure(address)
        geojson_data = self.azure_parser(resp)

        return geojson_data
    
    def is_sp(self, address:dict)->bool:

        test_city = address['properties']['cidade']=='São Paulo'
        test_state = address['properties']['estado']=='São Paulo'
        test_country = address['properties']['codigo_pais'].lower()=='br'

        return test_city * test_state & test_country

    def filter_address_sp(self, address_geojson:list)->List:

        in_city = [add for add in address_geojson['features']
                if self.is_sp(add)]
        address_geojson['features'] = in_city

    def address_feature_to_geojson(self, address_feat:dict, crs:dict)->dict:
        '''takes and anddress features and format it to a whole geojson'''
        
        #crs must be of t he whole geojson not of just one feature
        crs_num = int(crs['properties']['name'].split(':')[-1])
        
        return geojson_envelop([address_feat], crs_num)
    
    def format_address_data(self, address:dict, nominatim_crs:str, convert_to_wgs_84:bool, **camadas)->dict:

        address_data = {
                'endereco' : self.address_feature_to_geojson(address, nominatim_crs),
            }

        camadas_data = self.geosampa_query(address, convert_to_wgs_84, **camadas)
        address_data['camadas_geosampa'] = camadas_data

        return address_data
    
    def geoloc(self, address:str)->List[dict]:

        if not self.use_azure:
            print('Querying nominatim')
            geoloc_resp = self.nominatim_address_search(address)
        else:
            print('Querying azure')
            geoloc_resp = self.azure_address_search(address)

        self.filter_address_sp(geoloc_resp)

        return geoloc_resp
    
    def __call__(self, address:str, convert_to_wgs_84:bool=True, **camadas)->List[dict]:

        geoloc_resp = self.geoloc(address)
        resp_crs = geoloc_resp['crs']
        data = []
        #arrumar o endereco para ficar geojson
        for add in geoloc_resp['features']:
            data.append(self.format_address_data(add, resp_crs, convert_to_wgs_84, **camadas))

        return data
            


    
    
    



