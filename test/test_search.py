import json

from pmr_search import ModelSearch

model_search = ModelSearch()
# results = model_search.search({'filename':'~/Documents/MapCore/flatmap-source/functional-connectivity/annotation.json', 'method':SPARQL})
# with open('/Users/ymun794/Documents/MapCore/temporary/annotation.json', 'w') as fp:
#     json.dump(results, fp)

# def search_model(self, args):
#     filename = os.path.expanduser(args.get('filename'))
#     method = args.get('method', EMBEDDING)
    
#     with open(filename, 'r') as fp:
#         annotations = json.load(fp)
#     terms = list(set([ann['Model'] for values in annotations.values() 
#                         for ann in values if 'Model' in ann]))
    
#     if method != SPARQL:
#         models = self.get_models_embedding(terms)
#     else:
#         models = self.get_models_sparql(terms)
#         for values in annotations.values():
#             for ann in tqdm(values):
#                 if 'Model' in ann:
#                     ann['PMR'] = models[ann['Model']]
#     return annotations

print(model_search.search('basolateral plasma membrane'))



print('Done')
