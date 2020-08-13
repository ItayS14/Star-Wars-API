
from pymongo import MongoClient

class DBWrapper:
    def __init__(self, connection_string, db_name):
        self._client = MongoClient(connection_string)
        self._db = self._client[db_name]

    def insert(self, collection_name, data, term=None):
        """
        The function will insert data to a given collection
        :param collection_name: The collection to insert the data to (string)
        :param data: The data to insert (list of dict)
        :param tern: If given, cache will be composed from the data and stored in the db (str)
        """
        collection = self._db[collection_name]
        res = collection.insert_many(data)

        if term:
            # Adding cache which is linked to the ids of the documents
            cache = {
                'resource': collection_name,
                'term': term,
                'data': res.inserted_ids
            }
            cache_collection = self._db['cache']
            cache_collection.insert(cache)


