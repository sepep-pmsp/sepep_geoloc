from typing import List


class ParseCamadas:

    def get_camadas(self, xml_resp:dict)->List[dict]:
        '''Xml resp must be the original wfs xml resp parsed to dict'''

        return xml_resp['WFS_Capabilities']['FeatureTypeList']['FeatureType']
    
    def parse_camada(self, feature_dict:dict)->dict:

        parsed = {
            'layer_name' : feature_dict['Name'],
            'title' : feature_dict['Title'],
            'abstract' : feature_dict['Abstract'],
            'crs' : feature_dict['SRS']
        }

        return parsed
    
    def parse_all_camadas(self, feature_list:list)->List[dict]:

        return [self.parse_camada(feat) for feat in feature_list]
    
    def __call__(self, xml_resp:dict)->List[dict]:

        features = self.get_camadas(xml_resp)

        return self.parse_all_camadas(features)
