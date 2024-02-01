from api.core.integrations.nominatim import nominatim
from api.core.integrations.geosampa import geosampa
from typing import Tuple

from api.core.utils.geo import point_from_wgs_to_sirgas

class AddresSearch:

    def __init__(self):

        self.nominatim = nominatim
        self.geosampa = geosampa

    def points_from_nominatim(address_str: str)->Tuple[float, float]:

        #transform projection using utils
        pass

