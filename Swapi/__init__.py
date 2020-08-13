from Swapi.swapi import Swapi
from Swapi.database import DBWrapper
import json

with open('config.json') as f:
    config = json.load(f)
swapi = Swapi(config['BASE_URL'])
db = DBWrapper(config['CONNECTION_STRING'], config['DB_NAME'])