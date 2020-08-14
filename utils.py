from Swapi import swapi, db
import json

def pprint(data):
    """
    The function will print the data nicely in json format
    :param data: data to print (iterable of dicts)
    """
    for doc in data:
        doc.pop('_id', None) # Id is not JSON serializable, and not related to the data. Threfore, deleting it if exists.
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

    # Special sorting key function to handle both regular and mixed list
    def sorting_key(item):
        try:
            return (False, int(item[args.field]))
        except ValueError:
            return (True, item[args.field])

    return sorted(
        planets, 
        key=sorting_key, 
        reverse=args.direction == 'dec'
    )