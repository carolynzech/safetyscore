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


def userExists(username):
    datastore_client = datastore.Client()

    query = datastore_client.query(kind="user")
    query.add_filter("username", "=", username)
    result = list(query.fetch(1))
    return len(result) > 0


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


def addPlace(placeName, masksRating, distancingRating, outdoorRating, capacityRating, contactRating, tempRating, lat, lng, dangerType):
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
        'contactRating': contactRating,
        'tempRating': tempRating
    }
    entity["numRatings"] = 1
    entity['lat'] = lat
    entity['lng'] = lng
    entity["dangerType"] = dangerType
    datastore_client.put(entity)
    print(f"Saved {entity.key.name}: {entity['ratings']}")

def getPlace(placeName):
    datastore_client = datastore.Client()

    query = datastore_client.query(kind="place")
    query.add_filter("placeName", "=", placeName)
    result = list(query.fetch(1))
    if len(result) > 0:
        result = result[0]
        # print(result.key.name)
        # print(result["ratings"]["masksRating"])
        return result
    else:
        return None

def updatePlace(placeName, masksRating, distancingRating, outdoorRating, capacityRating, contactRating, tempRating, lat, lng, dangerType):
    result = getPlace(placeName)
    currMasks = result["ratings"]["masksRating"]
    currDistancing = result["ratings"]["distancingRating"]
    currOutdoor = result["ratings"]["outdoorRating"]
    currCapacity = result["ratings"]["capacityRating"]
    currContact = result["ratings"]["contactRating"]
    currTemp = result["ratings"]["tempRating"]
    currRatings = result["numRatings"]

    newRatings = currRatings + 1
    newMasks = round((currMasks + masksRating)/newRatings, 2)
    newDistancing = round((currDistancing + distancingRating)/newRatings, 2)
    newOutdoor = round((currOutdoor + outdoorRating)/newRatings, 2)
    newCapacity = round((currCapacity + capacityRating)/newRatings, 2)
    newContact = round((currContact + contactRating)/newRatings, 2)
    newTemp = round((currTemp + tempRating)/newRatings, 2)


    datastore_client = datastore.Client()

    key = result.key

    entity = datastore.Entity(key=key)
    entity["placeName"] = placeName
    entity["ratings"] = {
        'masksRating': newMasks, 
        'distancingRating': newDistancing, 
        'outdoorRating': newOutdoor,
        'capacityRating': newCapacity,
        'contactRating': newContact,
        'tempRating': newTemp
    }
    entity["numRatings"] = newRatings
    entity['lat'] = lat
    entity['lng'] = lng
    entity["dangerType"] = dangerType

    datastore_client.put(entity)
    print(f"Updated {entity.key.name}: {entity['ratings']}")


def getAllPlaces():
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="place")
    results = list(query.fetch())
    print(results)
    return results

def getType(type):
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="place")
    if type != '':
        query.add_filter("dangerType", "=", type)

    results = list(query.fetch())
    print(results)
    return results