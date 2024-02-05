

class CapabilitiesRequest:


    def json_response(self, query:dict)->None:

        query['outputFormat']='application/json'
        query['exceptions']='application/json'

    def get_capabilities(self, query:dict)->None:

        query['request']='GetCapabilities'

    def __call__(self):

        query = {}
        self.json_response(query)
        self.get_capabilities(query)

        return query