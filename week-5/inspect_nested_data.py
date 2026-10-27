
import pymongo
from pprint import pprint

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["starwars"]

print("=== CHARACTER HOMEWORLD ===")
pprint(db["characters"].find_one({}, {"homeworld": 1, "_id": 0}))

print("\n=== CHARACTER SPECIES ===")
pprint(db["characters"].find_one({}, {"species": 1, "_id": 0}))

print("\n=== CHARACTER FILMS ===")
pprint(db["characters"].find_one({}, {"films": 1, "_id": 0}))

print("\n=== STARSHIP PILOTS ===")
pprint(db["starships"].find_one({}, {"pilots": 1, "_id": 0}))

print("\n=== STARSHIP FILMS ===")
pprint(db["starships"].find_one({}, {"films": 1, "_id": 0}))

print("\n=== ALL COLLECTIONS ===")
print(db.list_collection_names())

client.close()
