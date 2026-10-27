import pymongo
from pprint import pprint
import pandas as pd

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["starwars"] # opens the client then selects this SW database

print("Collections:", db.list_collection_names()) # list of collections

print("\n--- CHARACTER EXAMPLE ---")
pprint(db["characters"].find_one())

print("\n--- STARSHIP EXAMPLE ---")
pprint(db["starships"].find_one())

print("\n--- DOCUMENT COUNTS ---")
print("Characters:", db["characters"].count_documents({}))
print("Starships:", db["starships"].count_documents({}))

# this was me exploring the data, listing the characters and starships collections and printing an example document
# from each, and also counting the documents, to verify what I am working with

client.close() # closes the connection as good practice


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["starwars"]
characters = list(db["characters"].find()) # loading documents into Python lists
starships = list(db["starships"].find())

print("Characters loaded:", len(characters))
print("Starships loaded:", len(starships))

print("loaded into Python:", len(characters))
print("loaded into Python:", len(starships))

# this is me using .find() to get every document, putting it in a list of Python dictionaries (into Python memory)
# printing the counts at the end and matching them to the previous section to verify if anything is lost

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

# so here each document is a row and each field is a column
# using .head() to select the first few rows and .columns.tolist() to show the field names for the structure


from sqlalchemy import create_engine, text

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# SQL Server connection settings (same as connect_sql.py)
SERVER = r"localhost\SQLSERVER2019"
DATABASE = "master"   # master always exists, so the check works before StarWarsDB is created
DRIVER = "ODBC Driver 18 for SQL Server"

odbc_connection = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

engine = create_engine(
    URL.create("mssql+pyodbc", query={"odbc_connect": odbc_connection})
)

# Test the connection
with engine.connect() as connection:
    result = connection.execute(text("SELECT @@VERSION"))
    print("SQL Server connection successful!")
    print("Server version:", result.scalar())

# a quick test to connect to my SQL database
