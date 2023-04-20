#===============================================================================

import torch
from sentence_transformers import SentenceTransformer, util
import os

#===============================================================================

SEARCH_DATA = 'search_data.pt'
BERTModel = 'gsarti/biobert-nli'
ALPHA = 0.5
BETA = 0.8
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#===============================================================================

class EmbeddingClient:
    def __init__(self):
        data = torch.load(os.path.join(BASE_DIR, SEARCH_DATA))
        self.__term_embs = data['embedding']
        self.__terms = data['term']
        self.__pmr_term = data['pmrTerm']
        self.__sckan_term = data['sckanTerm']
        self.__cellmls = data['cellml']        
        self.__cluster = data['cluster']
        self.__term_cellmls = data['termCellml']
        self.__cellml_ids = data['cellmlId']
        self.__cellml_embs = data['cellmlEmbs']
        self.__model = SentenceTransformer(BERTModel)

    def __get_query_embedding(self, query, context=[], c_weight=0.5):
        if query in self.__sckan_term:
            query_emb = self.to_embedding(self.__sckan_term[query])
        else:
            query_emb = self.__model.encode(query, convert_to_tensor=True)
        if len(context) > 0:
            context_emb = torch.mean(self.__model.encode(context, convert_to_tensor=True)) * c_weight
            query_emb = (query_emb + context_emb) / (1 + c_weight)
        return query_emb
    
    def __get_wks_exp(self, term):
        
        cellmls = self.__term_cellmls[term]
        workspaces, exposures = [], []
        for cellml_id in cellmls:
            cellml = self.__cellmls['data'][cellml_id]
            if cellml['workspace'] not in workspaces:
                workspaces += [cellml['workspace']]
            if 'exposure' in cellml:
                if cellml['exposure'] not in exposures:
                    exposures += [cellml['exposure']]

        if len(exposures) > 0:
            return {'exposure':exposures, 'workspace':workspaces, 'cellml':cellmls}
        
        # check other model if exposure is not available
        available_cellml = []
        for cellml_id in self.__term_cellmls[term]:
            cluster_id = self.__cluster['url2Cluster'][cellml_id]
            if cluster_id == '-1':
                if cellml_id not in available_cellml:
                    available_cellml += [cellml_id]
            else:
                similar_cellmls = self.__cluster['cluster'][cluster_id]
                available_cellml += [idx for idx in similar_cellmls if idx not in available_cellml]

        # get exposure and workspace
        exposures, workspaces = [], []
        for cellml_id in available_cellml:
            cellml = self.__cellmls['data'][cellml_id]
            if 'workspace' in cellml:
                workspaces += [cellml['workspace']] if cellml['workspace'] not in workspaces else []
            if 'exposure' in self.__cellmls['data'][cellml_id]:
                exposures += [cellml['exposure']] if cellml['exposure'] not in exposures else []
        return {'exposure':exposures, 'workspace':workspaces, 'cellml':available_cellml}
    
    def search(self, query, context, topk, min_sim, c_weight):
        query_emb = self.__get_query_embedding(query, context, c_weight)
        cos_scores = util.pytorch_cos_sim(query_emb, self.__term_embs)[0]
        top_results = torch.topk(cos_scores, k=topk)
        cellml_res = []
        for rank, (score, idx) in enumerate(zip(top_results[0], top_results[1])):
            if score < min_sim:
                break
            rst = {'score': (score.item(), self.__terms[idx], self.__pmr_term[self.__terms[idx]]['label'])}
            rst.update(self.__get_wks_exp(self.__terms[idx]))
            cellml_res += [rst]
        return cellml_res
    
    def __get_exposure(self, cellml_id):
        if 'exposure' in self.__cellmls['data'][cellml_id]:
            return self.__cellmls['data'][cellml_id]['exposure']
        else:
            cluster_id = self.__cluster['url2Cluster'][cellml_id]
            if cluster_id != '-1':
                similar_cellmls = self.__cluster['cluster'][cluster_id]
                for sim_cellml_id in similar_cellmls:
                    if 'exposure' in self.__cellmls['data'][sim_cellml_id]:
                        return self.__cellmls['data'][sim_cellml_id]['exposure']
        return ''
                
    def search_by_cellml(self, query, context=[], topk=5, min_sim=0.5, c_weight=0.5, verbose=True):
        query_emb = self.__get_query_embedding(query, context, c_weight)
        cos_scores = util.pytorch_cos_sim(query_emb, self.__cellml_embs)[0]
        top_results = torch.topk(cos_scores, k=topk)
        cellml_res = []
        for rank, (score, idx) in enumerate(zip(top_results[0], top_results[1])):
            if score < min_sim:
                break
            cellml_id = self.__cellml_ids[idx]
            cellml = self.__cellmls['data'][cellml_id]
            cellml_res += [{'score':score.item(), 'exposure':[self.__get_exposure(cellml_id)], 'workspace':[cellml['workspace']], 'cellml':[cellml_id]}]
        return cellml_res
    
    def to_embedding(self, term_data):
        embs = self.__model.encode(term_data['label'], convert_to_tensor=True)
        if len(term_data['synonym']) > 0:
            syn_embs = torch.mean(self.__model.encode(term_data['synonym'], convert_to_tensor=True), 0) * ALPHA
            embs = (embs + syn_embs) / (1 + ALPHA)
        
        added_term = term_data['def'] if isinstance(term_data['def'], list) else [term_data['def']] + term_data['is_a_text']
        
        if len(added_term) > 0:
            added_embs = torch.mean(self.__model.encode(added_term, convert_to_tensor=True), 0) * BETA
            embs = (embs + added_embs) / (1 + BETA)
        
        return embs
    
#===============================================================================