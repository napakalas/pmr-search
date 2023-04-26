import json

from pmr_search import ModelSearch, SPARQL

ms = ModelSearch()

print('. testing free text')
results = ms.search('basolateral plasma membrane')
assert len(results) == 0, f"... number of results greater than 0 expected, got: {len(results)}"

print('. testing UBERON')
results = ms.search('UBERON:0001629', ['Carotid body'], topk = 5, min_sim= 0.8, c_weight=0.6)
assert len(results) == 0, f"... EMBEDDING: number of results greater than 0 expected, got: {len(results)}"
results = ms.search('UBERON:0001629', ['Carotid body'], topk = 5, min_sim= 0.8, c_weight=0.6, client_type=SPARQL)
assert len(results) != 0, f"... SPARQL: number of results equal to 0 expected, got: {len(results)}"

print('Done')
