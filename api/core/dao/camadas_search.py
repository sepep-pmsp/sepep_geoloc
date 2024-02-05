from typing import List
from api.core.integrations import geosampa
from api.core.dao.parsers.geosampa_capabilities import ParseCamadas

class CamadasSearch:

    def __init__(self):

        self.geosampa = geosampa
        self.parser = ParseCamadas()

    def get_camadas(self)->List[dict]:

        capabilities = self.geosampa.list_capabilities()
        camadas = self.parser(capabilities)

        return camadas
    
    def __call__(self):

        return self.get_camadas()
    