import os
import requests
import json

class GraphQL:
    
    api: str
    
    def __init__(self, api):
        self.api = api
        
    def post(self, query, variables):
        request = requests.post(
            self.api, json={'query': query, "variables": variables}, 
            headers={'Authorization': 'bearer {}'.format(os.environ['TOKEN'])}
        )
        if request.status_code == 200:
            return json.loads(request.text)
        else:
            raise Exception("Query failed, with status code {}".format(request.status_code))


        