
import warnings
import re

class QueryBuilder:

    version = '1.0'

    def __init__(self, city:str, state:str, country_iso:str, 
                token:str, **kwargs)->None:
        

        self.check_country_iso(country_iso)
        self.country = country_iso
        self.state = state
        self.city = city
        self.token = token

        if kwargs.get('bbox_bound') or kwargs.get('bbox'):
            warnings.warn('Azure Maps não suporta bounding box na resposta')

    def check_country_iso(self, country_iso:str)->None:

        num_chars = len(country_iso)
        if num_chars!=2:
            raise ValueError('Contry ISO must be ISO_3166 compliant. Must be only two characters!')
        

    def set_accept_language_param(self, query:dict)->None:

        #soh para garantir vou colocar nos parametros tambem
        query['language'] = 'en-US'


    def set_token(self, query:dict)->None:

        query['subscription-key'] = self.token

    def set_version(self, query:dict)->None:

        query['api-version'] = self.version

    def set_city(self, query:dict)->None:

        query['municipality'] = self.city

    def set_state(self, query:dict)->None:

        query['countrySecondarySubdivision'] = self.state

    def set_country(self, query:dict)->None:

        query['countryCode'] = self.country

    def set_config_params(self, query:dict)->None:

        self.set_version(query)
        self.set_accept_language_param(query)
        self.set_token(query)
    
    def set_search_boundaries(self, query:dict)->None:

        self.set_city(query)
        self.set_state(query)
        self.set_country(query)


    def search_street(self, query:dict, street:str)->None:

        #rua e numero apenas o resto vai ser pre definido
        query['streetName'] = street

    def search_street_number(self, query:dict, number:str)->None:

        #rua e numero apenas o resto vai ser pre definido
        query['streetNumber'] = number

    def build_query_str(self, query:dict)->str:

        search_pairs = [f'{key}={val}' for key, val in query.items()]

        return '&'.join(search_pairs)

    def build_full_query(self, street:str, number:str)->dict:

        query = dict()
        self.search_street(query, street)
        self.search_street_number(query, number)
        self.set_search_boundaries(query)
        self.set_config_params(query)

        return self.build_query_str(query)
    
    def get_street_number(address:str)->str:

        apos_virgula = address.split(',')[1]
        search_sp = re.search('(s.o paulo)|(sp)', flags=re.IGNORECASE)
        if search_sp:
            indice_sp = search_sp.start()
            apos_virgula = apos_virgula[:indice_sp]

        return ''.join([item for item in  apos_virgula if item.is_digit()])
    
    def get_street_name(address:str)->str:

        return address.split(',')[0]

    def __call__(self, address:str)->str:
        '''Address is considered just street number and name. Rest is pre-defined. 
        Street number and name are extracted from string'''

        number = self.get_street_number(address)
        street = self.get_street_name(address)

        return self.build_full_query(street, number)