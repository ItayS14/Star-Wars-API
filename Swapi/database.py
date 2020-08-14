
from pymongo import MongoClient
from itertools import combinations


# The class is a wrapper to the mongodb client, adding caching functionality
class DBWrapper:
    def __init__(self, connection_string, db_name, search_fields):
        self._client = MongoClient(connection_string)
        self._db = self._client[db_name]
        self._search_fields = search_fields # The keys to find match in for each resource

    def insert(self, resource, data, search_term):
        """
        The function will insert data to a given collection
        :param resource: The resource which is the collection to insert the data to (string)
        :param data: The data to insert (list of dict)
        :param search_term: The serche term used to get this data (str)
        """
        collection = self._db[resource]
        #To avoid duplicates
        for doc in data:
            if collection.count_documents({'url': doc['url']}) == 0: # The url must be unique for each item
                collection.insert_one(doc)
    
        # Caching the insert command
        cache = {
            'resource': resource,
            'search_term': search_term,
        }
        self._db['cache'].insert_one(cache)

    def is_cached(self, resource, search_term):
        """
        The function checks if the query can be preformed with the existing data
        :param resource: the resource to check i.e: people (str)
        :param search_term: the search term to use (str)
        """
        substrings = [''] # Empty string is when somone searched for everything
        for x,y in combinations(range(len(search_term) + 1), r=2):
            substrings.append(search_term[x:y])

        # Iterate over the substring because for example if somone searched for "r"
        # The results for "r2" must already by in the database
        cache = self._db['cache']
        for substring in substrings:
            if cache.count_documents({'resource': resource,'search_term': substring}):
                return True
        return False

    def find(self, resource, search_term):
        """
        The function will find in the db documents acoording to the query 
        :param resource: the resource to check i.e: people (str)
        :param search_term: the search term to use (str)
        :return: iterator to the data (list)
        """
        fields = self._search_fields[resource] # Getting the field to search in
        collection = self._db[resource]
        final_results = []
        for field in fields:
            find_result = collection.find({
                field: {
                    # case insensetive regex to find the search term (simillar to the website search)
                    '$regex': '.*' + search_term + '.*',
                    '$options': 'i'
                }
            })
            final_results += list(find_result)
        return final_results