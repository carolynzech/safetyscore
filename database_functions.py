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

    print(f"Saved {entity.key.name}: {entity['key']}")

def addUser(username, password):
    datastore_client = datastore.Client()
    kind = "user"
    name = username
    key = datastore_client.key(kind, name)
    entity = datastore.Entity(key=key)
    entity["username"] = username
    entity["password"] = password

    datastore_client.put(entity)
    print(f"Saved {entity.key.name}: {entity}")

def checkUser(username, password):
    datastore_client = datastore.Client()
    key = datastore_client.key("user", username)
    entity = datastore_client.get(key=key)
    return (entity["username"]==username and entity["password"]==password)


def addPlace(placeName, masksRating, distancingRating, outdoorRating, capacityRating, contactRating, lat, lng):
    datastore_client = datastore.Client()
    kind = "place"
    name = placeName

    key = datastore_client.key(kind, name)
    entity = datastore.Entity(key=key)
    entity["placeName"] = placeName
    entity["ratings"] = {
        'masksRating': masksRating, 
        'distancingRating': distancingRating, 
        'outdoorRating': outdoorRating,
        'capacityRating': capacityRating,
        'contactRating': contactRating
    }
    entity["numRatings"] = 1
    entity['lat'] = lat
    entity['lng'] = lng
    datastore_client.put(entity)
    print(f"Saved {entity.key.name}: {entity['ratings']}")

def getPlace(placeName):
    datastore_client = datastore.Client()

    query = datastore_client.query(kind="place")
    query.add_filter("placeName", "=", placeName)
    result = list(query.fetch(1))
    if len(result) > 0:
        result = result[0]
        print(result.key.name)
        print(result["ratings"]["masksRating"])
        return result
    else:
        return None

def updatePlace(placeName, masksRating, distancingRating, outdoorRating, capacityRating, contactRating, lat, lng):
    result = getPlace(placeName)
    currMasks = result["ratings"]["masksRating"]
    currDistancing = result["ratings"]["distancingRating"]
    currOutdoor = result["ratings"]["outdoorRating"]
    currCapacity = result["ratings"]["capacityRating"]
    currContact = result["ratings"]["contactRating"]
    currRatings = result["numRatings"]

    newRatings = currRatings + 1
    newMasks = (currMasks + masksRating)/newRatings
    newDistancing = (currDistancing + distancingRating)/newRatings
    newOutdoor = (currOutdoor + outdoorRating)/newRatings
    newCapacity = (currCapacity + capacityRating)/newRatings
    newContact = (currContact + contactRating)/newRatings


    datastore_client = datastore.Client()

    key = result.key

    entity = datastore.Entity(key=key)
    entity["placeName"] = placeName
    entity["ratings"] = {
        'masksRating': newMasks, 
        'distancingRating': newDistancing, 
        'outdoorRating': newOutdoor,
        'capacityRating': newCapacity,
        'contactRating': newContact
    }
    entity["numRatings"] = newRatings
    entity['lat'] = lat
    entity['lng'] = lng

    datastore_client.put(entity)
    print(f"Updated {entity.key.name}: {entity['ratings']}")


def getAllPlaces():
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="place")
    results = list(query.fetch())
    print(results)
    return results