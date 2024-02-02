from. handlers import attr_not_found

from typing import List

class AddressParser:

    @attr_not_found('address')
    def get_address(self, feature:dict)->dict:

        return feature['properties']['address']

    @attr_not_found('cidade')
    def get_city(self, address:dict)->str:

        return address['city']
    

    @attr_not_found('state')
    def get_state(self, address:dict)->str:

        return address['state']
    
    @attr_not_found('country')
    def get_country(self, address:dict)->str:

        return address['country']
    
    @attr_not_found('country_code')
    def get_country_code(self, address:dict)->str:

        return address['country_code']
    
    @attr_not_found('road')
    def get_road(self, address:dict)->str:

        return address['road']
    
    @attr_not_found('house_number')
    def get_number(self, address:dict)->str:

        return address['house_number']
    
    @attr_not_found('geometry')
    def get_geom(self, feature:dict)->dict:

        return feature['geometry']
    
    @attr_not_found('bbox')
    def get_bbox(self, feature:dict)->dict:

        return feature['bbox']
    
    def build_address_string(self, parsed_adress:dict)->str:

        addres= (f"{parsed_adress['rua']}, nº {parsed_adress['numero']}, "
                f"{parsed_adress['cidade']}, {parsed_adress['cidade']}, {parsed_adress['pais']}")
        
        return addres
    
    def parse_address(self, feature:dict)->dict:

        resp_address = self.get_address(feature)
        parsed_addres = {
            'rua' : self.get_road(resp_address),
            'numero' : self.get_number(resp_address),
            'cidade' : self.get_city(resp_address),
            'estado' : self.get_state(resp_address),
            'pais' : self.get_country(resp_address),
            'codigo_pais' : self.get_country_code(resp_address),
        }

        parsed_addres['string_endereco'] = self.build_address_string(parsed_addres)

        return parsed_addres
    
    def build_feat_geojson(self, feature:dict)->dict:

        resp = {'type' : 'feature'}
        resp['properties'] = self.parse_address(feature)
        resp['geometry'] = self.get_geom(feature)
        resp['bbox'] = self.get_bbox(feature)

        return resp
    
    @attr_not_found('features')
    def get_features(self, resp:dict)->List[dict]:

        return resp['features']

    
    def parse_all_features(self, resp:dict)->List[dict]:

        features = self.get_features(resp)

        return [self.build_feat_geojson(feat) for feat in features]

    def add_crs_param(self, geojson:dict)->None:

        geojson['crs']  = {
            "type": "name",
            "properties": {
            "name": "EPSG:4326"
            }
        }
    
    def geojson_envelop(self, parsed_resp:List[dict])->dict:

        geojson = {
            'type': 'FeatureCollection',
            'features' : parsed_resp
        }

        self.add_crs_param(geojson)

        return geojson
    
    def __call__(self, resp:dict)->List[dict]:

        parsed_features = self.parse_all_features(resp)

        return self.geojson_envelop(parsed_features)


    
