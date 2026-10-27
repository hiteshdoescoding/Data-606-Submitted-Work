import pandas as pd
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["starwars"]
characters = list(db["characters"].find()) # loading documents into Python lists
starships = list(db["starships"].find())

print("Characters loaded:", len(characters))
print("Starships loaded:", len(starships))

# Convert the documents into DataFrames
characters_df = pd.DataFrame(characters)
starships_df = pd.DataFrame(starships)

# Inspect the structure
print("\nCHARACTERS")
print(characters_df.head())
print("\nCharacter columns:")
print(characters_df.columns.tolist())

print("\nSTARSHIPS")
print(starships_df.head())
print("\nStarship columns:")
print(starships_df.columns.tolist())

client.close()