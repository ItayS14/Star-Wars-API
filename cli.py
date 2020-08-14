import argparse
from utils import *
from Swapi import config

def main():
    parser = argparse.ArgumentParser(prog='swapi')
    sub_parsers = parser.add_subparsers()

    search_parser = sub_parsers.add_parser('search', help='Search data in the StarWars API')
    search_parser.add_argument('resource', type=validate_resource, help='The resource to serch in')
    search_parser.add_argument('term', help='The term to search. For example: "R2-D2"')
    search_parser.set_defaults(func=search)

    get_planets_parser = sub_parsers.add_parser('get-planets', help='Get data about all the planets from the API')
    get_planets_parser.add_argument('field', help='The field to order by')
    get_planets_parser.add_argument('direction', help='The direction to sort the data', choices=['dec', 'asc'])
    get_planets_parser.set_defaults(func=get_planets)
    
    args = parser.parse_args()
    try:
        results = args.func(args)
    except (KeyError, TypeError): 
        print('swapi get-planets: error: argument field: Invalid field to sort by at the moment' )
    else:
        pprint(results)

def validate_resource(value):
    """
    The validator checks that the value is a valid resource
    :param value: the entered resource by the user
    :return: the same value (str)
    :raise: argparse execption if the param was invalid
    """
    if value not in config['RESOURCES']:
        raise argparse.ArgumentTypeError('Invalid resource\nValid resources are:\n' + '\n'.join(config['RESOURCES']))
    return value

if __name__ == '__main__':
    main()