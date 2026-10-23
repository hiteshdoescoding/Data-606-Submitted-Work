```
import pymongo

client = pymongo.MongoClient()
db = client["starwars"]

luke = db.characters.find_one(
    {"name": "Luke Skywalker"}, {"name": 1, "eye_color": 1}
)
print(luke)
```
```
droids = db.characters.find({"species.name": "Droid"})
for droid in droids:
    print(droid["name"])
```

Height of Darth Vader
```
print(db.characters.find_one(
    {"name": "Darth Vader"},
    {"name": 1, "height": 1, "_id": 0}
))
```

Characters with yellow eyes
```
for doc in db.characters.find({"eye_color": "yellow"}):
    print(doc["name"])
```

Find the first 3 male characters in the collection
```
for man in db.characters.find({"gender": "male"}).limit(3):
    print(man)
```

All humans with the homeworld of Alderaan
```
for human in db.characters.find({"species.name": "Human", "homeworld.name": "Alderaan"}):
    print(human["name"])
```