
import argparse
from pmr_search import ModelSearch, __version__

#===============================================================================

def arg_parser():
    parser = argparse.ArgumentParser(description='Identify PMR models of the provided terms in a json file')
    
    parser.add_argument('-v', '--version', action='version', version=__version__)

    args = parser.add_argument_group('options')
    args.add_argument('-o', dest='term', help='search with ontology term(s)')
    args.add_argument('-t', dest='min_sim', help='set threshold for similarity score (default: 0.8).')
    args.add_argument('-s', dest='topk', help='set maximum number of models to retrieve (default: 5).')
    args.add_argument('-q', dest='query', help='search with free text query.')
    args.add_argument('-f', dest='source_file', help='search with a json file containing anatomical terms.')
    args.add_argument('-d', dest='dest_file', help='file destination to save the results..')
    
    return parser

#===============================================================================

def main():
    parser = arg_parser()
    args = parser.parse_args()
    model_search = ModelSearch()
    print(model_search(vars(args)))
	
#===============================================================================

if __name__ == '__main__':
    main()

#===============================================================================
