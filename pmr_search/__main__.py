
import argparse
from pmr_search import ModelSearch, __version__

#===============================================================================

def arg_parser():
    parser = argparse.ArgumentParser(description='Identify PMR models of the provided terms in a json file')
    
    parser.add_argument('-v', '--version', action='version', version=__version__)

    required = parser.add_argument_group('Required arguments')
    required.add_argument('--filename', required=True,
                        help='A json file containing anatomical terms')

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
