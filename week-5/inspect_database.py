import pymongo
from pprint import pprint

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["starwars"]

print("Collections:", db.list_collection_names()) # list of collections

print("\n--- CHARACTER EXAMPLE ---")
pprint(db["characters"].find_one())

print("\n--- STARSHIP EXAMPLE ---")
pprint(db["starships"].find_one())

print("\n--- DOCUMENT COUNTS ---")
print("Characters:", db["characters"].count_documents({}))
print("Starships:", db["starships"].count_documents({}))

client.close()