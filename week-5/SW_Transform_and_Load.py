
import os

import pandas as pd
from pymongo import MongoClient


# --------------------------------------------------
# 1. CONNECT TO MONGODB
# --------------------------------------------------

mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
database_name = os.getenv("MONGODB_DATABASE", "starwars")

client = MongoClient(mongo_uri)
db = client[database_name]

starships_raw = list(db["starships"].find())
characters_raw = list(db["characters"].find())

print("Starships retrieved:", len(starships_raw))
print("Character records retrieved for pilot lookup:", len(characters_raw))


# --------------------------------------------------
# 2. CREATE LOOKUP FOR PILOT REFERENCES
# --------------------------------------------------

# Convert MongoDB IDs to strings so ObjectIds and string
# references can be compared consistently.

characters_by_mongo_id = {
    str(character["_id"]): character
    for character in characters_raw
}


# --------------------------------------------------
# 3. TRANSFORM STARSHIPS
# --------------------------------------------------

starship_rows = []
starship_id_by_mongo_id = {}

for starship_id, ship in enumerate(starships_raw, start=1):

    mongo_id = str(ship["_id"])
    starship_id_by_mongo_id[mongo_id] = starship_id

    starship_rows.append({
        "starship_id": starship_id,
        "mongo_id": mongo_id,
        "name": ship.get("name"),
        "model": ship.get("model"),
        "manufacturer": ship.get("manufacturer"),
        "cost_in_credits": ship.get("cost_in_credits"),
        "length": ship.get("length"),
        "max_atmosphering_speed": ship.get(
            "max_atmosphering_speed"
        ),
        "crew": ship.get("crew"),
        "passengers": ship.get("passengers"),
        "cargo_capacity": ship.get("cargo_capacity"),
        "consumables": ship.get("consumables"),
        "hyperdrive_rating": ship.get("hyperdrive_rating"),
        "MGLT": ship.get("MGLT"),
        "starship_class": ship.get("starship_class"),
        "created": ship.get("created"),
        "edited": ship.get("edited"),
        "url": ship.get("url")
    })

starships_df = pd.DataFrame(starship_rows)


# --------------------------------------------------
# 4. TRANSFORM STARSHIP PILOT RELATIONSHIPS
# --------------------------------------------------

pilot_rows = []
unresolved_pilots = []

for ship in starships_raw:

    ship_mongo_id = str(ship["_id"])
    starship_id = starship_id_by_mongo_id[ship_mongo_id]

    for pilot_reference in ship.get("pilots") or []:

        # References may be ObjectIds, strings or dictionaries.
        if isinstance(pilot_reference, dict):
            pilot_mongo_id = (
                pilot_reference.get("_id")
                or pilot_reference.get("id")
                or pilot_reference.get("mongo_id")
            )
        else:
            pilot_mongo_id = pilot_reference

        if pilot_mongo_id is None:
            unresolved_pilots.append({
                "starship": ship.get("name"),
                "pilot_reference": str(pilot_reference)
            })
            continue

        pilot_mongo_id = str(pilot_mongo_id)

        pilot = characters_by_mongo_id.get(pilot_mongo_id)

        if pilot is None:
            unresolved_pilots.append({
                "starship": ship.get("name"),
                "pilot_reference": pilot_mongo_id
            })
            continue

        pilot_rows.append({
            "starship_id": starship_id,
            "pilot_mongo_id": pilot_mongo_id,
            "pilot_name": pilot.get("name")
        })

starship_pilots_df = pd.DataFrame(
    pilot_rows,
    columns=[
        "starship_id",
        "pilot_mongo_id",
        "pilot_name"
    ]
).drop_duplicates(
    subset=["starship_id", "pilot_mongo_id"]
).reset_index(drop=True)


# --------------------------------------------------
# 5. REPORT TRANSFORMATION RESULTS
# --------------------------------------------------

print("\n--- TRANSFORMED DATAFRAMES ---")

print("\nstarships_df:", len(starships_df), "rows")
print(starships_df.head(3).to_string(index=False))

print("\nstarship_pilots_df:", len(starship_pilots_df), "rows")
print(starship_pilots_df.head(10).to_string(index=False))

print("\nUnresolved pilot references:", len(unresolved_pilots))
print(unresolved_pilots)



import pandas as pd
from sqlalchemy import text
from connect_sql import engine   # runs connect_sql.py, so the DB and tables exist

# --------------------------------------------------
# 1. SPLIT INTO 3NF TABLES
# --------------------------------------------------
# pilot_name depends on the pilot, not on the ship/pilot pair,
# so it belongs in its own Pilots table.

pilots_df = (
    starship_pilots_df[["pilot_mongo_id", "pilot_name"]]
    .drop_duplicates(subset="pilot_mongo_id")
)
links_df = starship_pilots_df[["starship_id", "pilot_mongo_id"]]

# --------------------------------------------------
# 2. RENAME COLUMNS TO MATCH THE SQL TABLES
# --------------------------------------------------

starships_load = starships_df.rename(columns={
    "starship_id": "StarshipID",
    "mongo_id": "MongoID",
    "name": "Name",
    "model": "Model",
    "manufacturer": "Manufacturer",
    "cost_in_credits": "CostInCredits",
    "length": "Length",
    "max_atmosphering_speed": "MaxAtmospheringSpeed",
    "crew": "Crew",
    "passengers": "Passengers",
    "cargo_capacity": "CargoCapacity",
    "consumables": "Consumables",
    "hyperdrive_rating": "HyperdriveRating",
    "MGLT": "MGLT",
    "starship_class": "StarshipClass",
    "created": "Created",
    "edited": "Edited",
    "url": "URL",
})

pilots_load = pilots_df.rename(columns={
    "pilot_mongo_id": "PilotMongoID",
    "pilot_name": "PilotName",
})

links_load = links_df.rename(columns={
    "starship_id": "StarshipID",
    "pilot_mongo_id": "PilotMongoID",
})

# --------------------------------------------------
# 3. LOAD INTO SQL SERVER
# --------------------------------------------------
# engine.begin() = one transaction: if anything fails, nothing is saved.
# Parents (Starships, Pilots) go in before the child (StarshipPilots),
# because of the foreign keys. Deletes run in reverse order.

with engine.begin() as conn:
    conn.execute(text("DELETE FROM StarshipPilots"))
    conn.execute(text("DELETE FROM Pilots"))
    conn.execute(text("DELETE FROM Starships"))

    starships_load.to_sql("Starships", conn, if_exists="append", index=False)
    pilots_load.to_sql("Pilots", conn, if_exists="append", index=False)
    links_load.to_sql("StarshipPilots", conn, if_exists="append", index=False)

print("Load complete.")

# --------------------------------------------------
# 4. VERIFY
# --------------------------------------------------

with engine.connect() as conn:
    for table in ["Starships", "Pilots", "StarshipPilots"]:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(table, ":", count, "rows")

    print(pd.read_sql(text("""
        SELECT s.Name AS Starship, p.PilotName
        FROM Starships s
        JOIN StarshipPilots sp ON s.StarshipID = sp.StarshipID
        JOIN Pilots p ON p.PilotMongoID = sp.PilotMongoID
        ORDER BY s.Name
    """), conn))



# Close the MongoDB connection after extraction.
client.close()
