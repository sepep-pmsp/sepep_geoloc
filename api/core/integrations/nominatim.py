from requests import Session
from copy import copy

class QueryBuilder:

    def __init__(self, city:str, state:str, country_iso:str, 
                contact_email:str, bbox_bound:dict=None)->None:

        self.check_country_iso(country_iso)
        self.country = country_iso
        self.state = state
        self.city = city
        if bbox_bound is not None:
            self.bbox = self.build_bbox(bbox_bound)
        else:
            self.bbox = None

        self.email = contact_email

    def check_country_iso(self, country_iso:str)->None:

        num_chars = len(country_iso)
        if num_chars!=2:
            raise ValueError('Contry ISO must be ISO_3166 compliant. Must be only two characters!')

    def build_bbox(self, *, x_min:str, x_max:str, y_min:str, y_max:str)->str:

        return f'{x_min},{y_min},{x_max},{y_max}'

    def set_format_param(self, query:dict)->None:

        query['format'] = 'geojson'

    def set_accept_language_param(self, query:dict)->None:

        #soh para garantir vou colocar nos parametros tambem
        query['accept-language'] = 'en-US'

    def set_bbox_param(self, query:dict)->None:

        if self.bbox:
            query['bounded'] = 1
            query['viewbox'] = self.bbox
        else:
            query['bounded'] = 0

    def set_email_param(self, query:dict)->None:

        query['email'] = self.email

    def set_address_layer_param(self, query:dict)->None:

        #esse parametro diz que estamos buscando endereços e não pontos de interesse
        query['layer'] = 'address'

    def set_address_details_param(self, query:dict)->None:

        #esse parametro faz retornar os detalhes do endereco encontrado - importante para checagem
        query['addressdetails'] = 1

    def set_city(self, query:dict)->None:

        query['city'] = self.city

    def set_state(self, query:dict)->None:

        query['state'] = self.state

    def set_country(self, query:dict)->None:

        query['country'] = self.country

    def set_config_params(self, query:dict)->None:

        self.set_address_layer_param(query)
        self.set_format_param(query)
        self.set_accept_language_param(query)
        self.set_email_param(query)
        self.set_address_details_param(query)
    
    def set_search_boundaries(self, query:dict)->None:

        self.set_city(query)
        self.set_state(query)
        self.set_country(query)
        self.set_bbox_param(query)

    def search_address(self, query:dict, address:str)->None:

        #rua e numero apenas o resto vai ser pre definido
        query['street'] = address

    def build_query_str(self, query:dict)->str:

        search_pairs = [f'{key}={val}' for key, val in query.items()]

        return '&'.join(search_pairs)

    def build_full_query(self, address:str)->dict:

        query = dict()
        self.search_address(query, address)
        self.set_search_boundaries(query)
        self.set_config_params(query)

        return self.build_query_str(query)

    def __call__(self, address:str)->str:
        '''Addess as street name and street number. Rest is pre-defined'''

        return self.build_full_query(address)


class Nominatim:
    '''Classe que implementa busca por endereços usando a API do nominatim.
    city: str -> parametro que define a cidade limite da pesquisa;
    state: str -> parametro que define o Estado limite da pesquisa;
    country_iso: str -> parametro que define o país limite da pesquisa
    tem que estar no formato ISO https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2;
    bbox_bound: dict{x_min, x_max, y_min, y_max} -> parametro que define o bound box limite da pesquisa;
    '''

    host = 'nominatim.openstreetmap.org'
    endpoint = 'search'

    def __init__(self, city:str, state:str, country_iso:str, contact_email:str, bbox_bound:dict=None)->None:

        
        self.build_query = QueryBuilder(city, state, country_iso, 
                                        contact_email, bbox_bound)

        self.session = Session()
        self.add_language_headers()

        self.base_url = self.build_base_url()    
        
    def build_base_url(self)->str:

        return f'https://{self.host}/{self.endpoint}'
        
    
    def add_language_headers(self):
        
        #tem que colocar esse header se nao ele muda a language da
        #resposta da API com base no reverse location search do IP
        #o que faria o codigo quebrar

        self.session.headers.update({'Accept-Language' : 'en-US'})

    def address_request(self, address:str)->dict:

        query = self.build_query(address)
        url = self.base_url+'?'+query
        print('Searching nominatim: ', url)
        with self.session.get(url) as r:
            return r.json()

    def __call__(self, address:str)->dict:

        return self.address_request(address)