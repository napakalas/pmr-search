#===============================================================================

from .sparqlclient import PMRClient, ScicrunchClient
from .embeddingclient import EmbeddingClient

#===============================================================================

EMBEDDING = 1
SPARQL = 2

#===============================================================================

namespaces = { 
              'UBERON': 'http://purl.obolibrary.org/obo/UBERON_',
              'ILX': 'http://uri.interlex.org/base/ilx_',
             }

#===============================================================================

class ModelSearch:
    def __init__(self):
        self.__pmr_client = PMRClient()
        self.__sci_client = ScicrunchClient()
        self.__emb_client = EmbeddingClient()

    def search(self, term, context=[], topk=5, min_sim=0.8, c_weight=0.5, client_type=EMBEDDING):
        if client_type == EMBEDDING:
            return self.__emb_client.search(term, context=context, topk=topk, min_sim=min_sim, c_weight=c_weight)
        elif client_type == SPARQL:
            curies = self.__sci_client.get_existings(term)
            return self.__pmr_client.search(curies)

    def close(self):
        self.__sci_client.close()

    def get_curie(uri_or_uriref):
        uri = str(uri_or_uriref)
        for k, v in namespaces.items():
            if uri.startswith(v):
                return k + ':' + uri.split(v)[-1]
        return uri_or_uriref
        
#===============================================================================
