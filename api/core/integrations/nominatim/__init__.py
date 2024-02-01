from .nominatim import Nominatim
from api.config import CITY, STATE, COUNTRY_ISO, NOMINATIM_EMAIL


print(COUNTRY_ISO)
nominatim_address_search = Nominatim(CITY, STATE, COUNTRY_ISO, NOMINATIM_EMAIL)