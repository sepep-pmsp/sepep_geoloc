from .nominatim import Nominatim
from .nominatim_reverse_geocode import ReverseGeocoding
from config import CITY, STATE, COUNTRY_ISO, NOMINATIM_EMAIL


nominatim_address_search = Nominatim(CITY, STATE, COUNTRY_ISO, NOMINATIM_EMAIL)
nominatim_reverse_search = ReverseGeocoding(NOMINATIM_EMAIL)