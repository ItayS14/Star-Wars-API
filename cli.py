import argparse
from utils import *

def main():
    parser = argparse.ArgumentParser(prog='swapi')
    sub_parsers = parser.add_subparsers()

    search_parser = sub_parsers.add_parser('search', help='Search data in the StarWars API')
    search_parser.add_argument('resource', help='The resource to serch in')
    search_parser.add_argument('term', help='The term to search. For example: "R2-D2"')
    search_parser.set_defaults(func=search)

    get_planets_parser = sub_parsers.add_parser('get-planets', help='Get data about all the planets from the API')
    get_planets_parser.add_argument('field', help='The field to order by')
    get_planets_parser.add_argument('direction', help='The direction to sort the data', choices=['dec', 'asc'])
    get_planets_parser.set_defaults(func=get_planets)

    args = parser.parse_args()
    results = args.func(args)
    pprint(results)

if __name__ == '__main__':
    main()