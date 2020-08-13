from swapi import Swapi
import argparse
from pymongo import MongoClient
import json
from database import DBWrapper


def pprint(data):
    """
    The function will print the data nicely in json format
    :param data: data to print (iterable)
    """
    for doc in data:
        del doc['_id'] # Id is not JSON serializable, and not related to the data. Threfore, deleting it
        print(json.dumps(doc, indent=3))
        print('*' * 100)


def search(swapi, db, args):
    """
    The function will get the search results and save them in db
    :param swapi: The class that interacts with the API (Swapi class)
    :param db: The database (MongoDB database)
    :param args: The arguments from the cli (Namespace)
    """
    if db.is_cached(args.resource, args.term):
        pprint(db.find(args.resource, args.term))
    else:
        search_results = swapi.search(args.resource, args.term)
        db.insert(
            args.resource,
            search_results,
            args.term        
        )
        pprint(search_results)
    

def get_planets(swapi, db, args):
    """
    The function will get all the planets and save them in db
    :param swapi: The class that interacts with the API (Swapi class)
    :param db: The database (MongoDB database)
    :param args: The arguments from the cli (Namespace)
    """
    if db.is_cached('planets', ''):
        pprint(db.find('planets', ''))
    else:
        planets = swapi.get_planets(args.field, args.direction == 'dec')
        db.insert('planets', planets, '')
        pprint(planets)


def main():
    with open('config.json') as f:
        config = json.load(f)

    swapi = Swapi(config['BASE_URL'])
    db = DBWrapper(config['CONNECTION_STRING'], config['DB_NAME'])

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
    args.func(swapi, db, args)


if __name__ == '__main__':
    main()