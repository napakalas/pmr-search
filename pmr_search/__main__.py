#===============================================================================

import argparse
from pmr_search import ModelSearch, __version__

#===============================================================================

def arg_parser():
    parser = argparse.ArgumentParser(description='Identify PMR models of the provided terms in a json file')
    
    parser.add_argument('-v', '--version', action='version', version=__version__)

    args = parser.add_argument_group('options')
    args.add_argument('-o', dest='term', help='search with ontology term or free text query.', default='')
    args.add_argument('-t', dest='min_sim', type=float, help='set threshold for similarity score (default: 0.8).', default=0.84)
    args.add_argument('-s', dest='topk', type=int, help='set maximum number of models to retrieve (default: 5).', default=5)
    args.add_argument('-f', dest='source_file', help='search with a json file containing anatomical terms.', default='')
    args.add_argument('-d', dest='dest_file', help='file destination to save the results..', default='')
    
    return parser

#===============================================================================
def single_search(term, topk, min_sim):
    ms = ModelSearch()
    results = ms.search(term, topk=topk, min_sim=min_sim)
    ms.close()
    return results

def multi_search(source_file, dest_file, topk, min_sim):
    import os
    import json
    from tqdm import tqdm
    source_file = os.path.expanduser(source_file)
    with open(source_file, 'r') as fp:
        annotations = json.load(fp)
    
    ms = ModelSearch()
    
    for values in annotations.values():
        for ann in tqdm(values):
            term_id = ann.get('Model', '') + ann.get('Models', '')
            context = ann.get('Organ', '') + ann.get('Organ/System', '')
            cand_model = ms.search(term_id, context=[context, 'Human'], topk=topk, min_sim=min_sim, c_weight=1)
            if len(cand_model) > 0:
                model = cand_model[0]
                pmr_model = (model['exposure'] + model['workspace'] + model['cellml'])[0]
                ann['pmr'] = {'score': model['score'], 'pmr_model': pmr_model}

    with open(dest_file, 'w') as fp:
        json.dump(annotations, fp)


def main():
    parser = arg_parser()
    options = vars(parser.parse_args())
    min_sim = options.get('min_sim')
    topk = options.get('topk')
    term = options.get('term')
    source_file = options.get('source_file')
    dest_file = options.get('dest_file')
    if options.get('term') != '':
        print(single_search(term, topk=topk, min_sim=min_sim))
        return

    if source_file != '' and dest_file != '':
        multi_search(source_file=source_file, dest_file=dest_file, topk=topk, min_sim=min_sim)
        return
	
#===============================================================================

if __name__ == '__main__':
    main()

#===============================================================================
