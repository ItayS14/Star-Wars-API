from Swapi import swapi, db
import json

def pprint(data):
    """
    The function will print the data nicely in json format
    :param data: data to print (iterable of dicts)
    """
    for doc in data:
        del doc['_id'] # Id is not JSON serializable, and not related to the data. Threfore, deleting it
        print(json.dumps(doc, indent=3))
        print('*' * 100)


def search(args):
    """
    The function will get the search results and save them in db
    :param args: The arguments from the cli (Namespace)
    :return: The results to print (list)
    """
    if db.is_cached(args.resource, args.term):
        return db.find(args.resource, args.term)
    else:
        search_results = swapi.search(args.resource, args.term)
        db.insert(
            args.resource,
            search_results,
            args.term        
        )
        return search_results
    

def get_planets(args):
    """
    The function will get all the planets and save them in db
    :param args: The arguments from the cli (Namespace)
    :return: The results to print (list)
    """
    if db.is_cached('planets', ''):
        planets = db.find('planets', '')
    else:
        planets = swapi.get_planets()
        db.insert('planets', planets, '')
    return sorted(
        planets, 
        key=lambda document: document[args.field], 
        reverse=args.direction == 'dec'
    )