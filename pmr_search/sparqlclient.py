import os
import requests
import json
import logging as log
from SPARQLWrapper import SPARQLWrapper, JSON

#===============================================================================

SCICRUNCH_API_KEY = os.environ.get('SCICRUNCH_API_KEY')
SCICRUNCH_EP = "https://scicrunch.org/api/1"
PMR_EP = "https://models.physiomeproject.org/pmr2_virtuoso_search"

#===============================================================================

SPARQL_TEMPLATE = """
    SELECT DISTINCT ?graph ?model
        WHERE 
        {{
          GRAPH ?graph 
          {{
              {{
                ?model ?p ?o.
                {}.
              }}
          }}
        }}
        ORDER BY ?graph
        LIMIT 10
    """

#===============================================================================

class PMRClient:
    def __init__(self):
        self.__sparql_ep = SPARQLWrapper(PMR_EP)
        self.__sparql_ep.setReturnFormat(JSON)
    
    def __create_term_filter(self, terms):
        filters = []
        for term in terms:
            filters += [f'STRENDS(STR(?o), "{term}") || REGEX(STR(?o), "{term.replace(":", "_")}")']
        return f"FILTER ({' || '.join(filters)})"
    
    def search(self, terms:list):
        if len(terms) == 0: 
            return []
        res, models = [], []
        f_terms = self.__create_term_filter(terms)
        query_term = SPARQL_TEMPLATE.format(f_terms)
        self.__sparql_ep.setQuery(query_term)
        ret = self.__sparql_ep.queryAndConvert()
        for r in ret["results"]["bindings"]:
            workspace = r['graph']['value']
            if workspace.endswith('.cellml'):
                workspace = model = os.path.join(workspace, 'view')
            else:
                model = os.path.join(workspace, 'file/HEAD', r['model']['value'].split('#')[0])
            if model not in models:
                res += [{'Workspace': workspace, 'Model': model}]
                models += [model]
        return res
        
#===============================================================================

class ScicrunchClient:
    def __init__(self):
        self.__session = requests.Session()
        self.__session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',})
        
    def __check_result(self, resp, curie:str):
        if resp.status_code == 401:
            raise Exception('incorrect SCICRUNCH_API_KEY')
        elif resp.status_code >= 400 and resp.status_code < 500:
            log.warning(f'{curie} is not found')
        elif resp.status_code > 500:
            log.warning('api server error')
        
    def get_data(self, api_path:str, curie:str):
        url = os.path.join(SCICRUNCH_EP, api_path, curie)
        params = {'key': SCICRUNCH_API_KEY}
        params = json.dumps(params)
        resp = self.__session.get(url, data=params)
        self.__check_result(resp, curie)
        if 'data' not in resp.json():
            return {}
        return resp.json()['data']
    
    def get_existings(self, curie:str):
        if len(curie.strip()) == 0:
            return []
        data = self.get_data('term/curie', curie)
        existings = []
        if 'existing_ids' in data:
            for term in data['existing_ids']:
                if term['curie'].startswith('FMA'):
                    existings += [term['curie']]
        return list(set(existings))
    
    def close(self):
        self.__session.close()

#===============================================================================
