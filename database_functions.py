from google.cloud import datastore



#an example of how to add an entity to the database
def addEntity():
    datastore_client = datastore.Client()
    kind = "kind"

    name = "name"

    key = datastore_client.key(kind, name)

    entity = datastore.Entity(key=key)

    entity["key"] = "value"

    datastore_client.put(entity)

    print(f"Saved {entity.key.name}: {entity['description']}")


def addUser(username):
    datastore_client = datastore.Client()
    kind = "user"
    name = username
    key = datastore_client.key(kind, name)
    entity = datastore.Entity(key=key)
    datastore_client.put(entity)
    print(f"Saved {entity.key.name}: {entity['description']}")

def addPlace(placeName, masksRating, distancingRating, outdoorRating, capacityRating, contactRating):
    datastore_client = datastore.Client()
    kind = "place"
    name = placeName

    key = datastore_client.key(kind, name)
    entity = datastore.Entity(key=key)
    entity["ratings"] = {
        'masksRating': masksRating, 
        'distancingRating': distancingRating, 
        'outdoorRating': outdoorRating,
        'capacityRating': capacityRating,
        'contactRating': contactRating
    }
    datastore_client.put(entity)
    print(f"Saved {entity.key.name}: {entity['description']}")

def getPlace(placeName):
    datastore_client = datastore.Client()

    query = datastore_client.query(kind="Place")
    result = query.fetch(1)
    print(result.key.name)
    return result

