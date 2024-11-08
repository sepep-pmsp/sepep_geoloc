from .azure_maps import AzureMapsAdress
from .azure_maps_cep import AzureMapsCep
from config import CITY, STATE, COUNTRY_ISO, AZURE_KEY


azure_maps_address_search = AzureMapsAdress(CITY, STATE, COUNTRY_ISO, AZURE_KEY)
azure_maps_cep_search = AzureMapsCep(CITY, STATE, COUNTRY_ISO, AZURE_KEY)