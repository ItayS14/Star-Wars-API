from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.swapi_db
collection = db.cache
print(collection.find({}))
# for res in collection.find({}):
    # print(res)

collection.delete_many({})