from .azure_maps import AzureMapsAdress
from config import CITY, STATE, COUNTRY_ISO, AZURE_KEY


azure_maps_address_search = AzureMapsAdress(CITY, STATE, COUNTRY_ISO, AZURE_KEY)