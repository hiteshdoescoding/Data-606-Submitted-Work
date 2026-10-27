import requests
import pymongo

client = pymongo.MongoClient() # opening a connection line to the local server
db = client["starwars"] # selecting my database
characters_collection = db["characters"] # where my character data is
starships_collection = db["starships"] # where I will put my starships in locally


# Get starships function
def get_starships():
    url = "https://swapi.dev/api/starships/"   # taken from the documentation
    ship_list = []
    next_page = True

    while next_page:
        response = requests.get(url)  # getting the response from the address
        data = response.json()  # putting the response into a json format which is a python dictionary to sort through

        if data and "results" in data: # this is all pagination
            for starship in data["results"]:
                ship_list.append(starship)
            if data["next"] is not None:
                url = data["next"]
            else:
                next_page = False
        else:
             next_page = False

    return ship_list

    # return data["results"]   # a key is needed, as if it was just return data, then
# you would be returning the whole dictionary, which if trying to loop through would only
# loop through the keys (count, next, previous, results) and not the starships

print(get_starships()[0]["name"])   # this is just to check if it worked, to print the first ship


# get pilot ids function
def get_pilot_ids(pilot_urls):   # defining the function, which receives the input we are calling pilot_urls
    pilot_object_ids = []   # creating the list to put all the pilot IDs in from the database

    for pilot_url in pilot_urls:   # goes through the starship's pilots list
        pilot_response = requests.get(pilot_url)   # gets the data from the pilot's url
        pilot_data = pilot_response.json()   # takes the data and converts to a json dictionary format

        character_name = pilot_data["name"]   # extracting the pilots name
        character_doc = characters_collection.find_one({"name": character_name}) # searches MongoDB characters for a matching name

        if character_doc:
            pilot_object_ids.append(character_doc["_id"])   # if the character exists, take the database ID to the pilot objects id list

    return pilot_object_ids   # return the completed list of IDs from MongoDB


# replace pilot links with ids function
def replace_pilots_and_insert():

    starships = get_starships() # a function to get list of starships online from previously

    for starship in starships: # looping through every starship
        pilot_urls = starship["pilots"] # values/urls from each pilot key
        pilot_ids = get_pilot_ids(pilot_urls) # this is where the urls get translated to MongoDB IDs
        starship["pilots"] = pilot_ids # finally overwrites the old urls to the new IDs

    starships_collection.delete_many({}) # wipes old collection data to avoid duplicates if ran again
    starships_collection.insert_many(starships)

replace_pilots_and_insert()