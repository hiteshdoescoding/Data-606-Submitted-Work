import requests
import pymongo

client = pymongo.MongoClient()
db = client["starwars"]

# Get starships function
def get_starships():
    url = "https://swapi.dev/api/starships/"   # taken from the documentation
    response = requests.get(url)   # getting the response from the address
    data = response.json()   # putting the response into a json format which is a python dictionary to sort through

    return data["results"]   # a key is needed, as if it was just return data, then
# you would be returning the whole dictionary, which if trying to loop through would only
# loop through the keys (count, next, previous, results) and not the starships

print(get_starships()[0]["name"])   # this is just to check if it worked, to print the first ship


# get pilot ids function
def get_pilot_ids(pilot_urls):   # defining the function, which receives the input we are calling pilot_urls
    pilot_object_ids = []   # creating the list to put all the pilots in from the database

    for pilot_url in pilot_urls():   # goes through the starship's pilots list
        pilot_response = requests.get(pilot_url)   # gets the data from the pilot's url
        pilot_data = pilot_response.json()   # takes the data and converts to a json dictionary format

        characters_collection = db["characters"]   # character data from database
        character_name = pilot_data["name"]   # essentially matching the character name to the pilot name
        character_doc = characters_collection.find_one({"name": character_name})   #

        if character_doc:
            pilot_object_ids.append(character_doc["_id"])   # if the character exists, take the database ID to the pilot objects id list

    return pilot_object_ids   # return the completed list of IDs from MongoDB




# replace pilot links with ids function
#def replace_pilots_and_insert():