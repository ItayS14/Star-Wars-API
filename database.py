
from pymongo import MongoClient

class DBWrapper:
    def __init__(self, connection_string, db_name):
        self._client = MongoClient(connection_string)
        self._db = self._client[db_name]

    def insert(self, collection_name, data, search_term):
        """
        The function will insert data to a given collection
        :param collection_name: The resource which is the collection to insert the data to (string)
        :param data: The data to insert (list of dict)
        :param search_term: The serche term used to get this data (str)
        """
        collection = self._db[collection_name]
        res = collection.insert_many(data)

        # Adding cache which is linked to the ids of the documents
        cache = {
            'resource': collection_name,
            'search_term': search_term,
            'data': res.inserted_ids
        }
        cache_collection = self._db['cache']
        cache_collection.insert(cache)

    def is_cached(self, resource, search_term):
        """
        The function checks if the query can be preformed with the existing data
        :param resource: the resource to check i.e: people (str)
        :param search_term: the search term to use (str)
        """
        return self._db['cache'].find({
            'resource': resource,
            'search_term': search_term 
        }).count() > 0


    def find(self, resource, search_term):
        """
        The function will find in the db documents acoording to the query 
        :param resource: the resource to check i.e: people (str)
        :param search_term: the search term to use (str)
        :return: iterator to the data (list)
        """
        ids = self._db['cache'].find_one({
            'resource': resource,
            'search_term': search_term
        })['data']
        return [self._db[resource].find_one({'_id': _id}) for _id in ids]