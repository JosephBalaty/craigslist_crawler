
import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Designate functions which do the CRUD operations (add a listing
# to the database, retrieve current listings, and remove a listing from the database.

def getListings():
    uri = "mongodb+srv://jbalaty:qU4vUqpJWiC4AFM8@cluster0.4jtkek7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.CraigslistSearches
    # Send a ping to confirm a successful connection
    listings = []

    try:
        client.admin.command('ping')
        collection = db.QuerySearches

        result = collection.find()
        for list in result:
            listings.append(list)
        print("Pinged your deployment. You successfully connected to MongoDB!")

    except Exception as e:
        print(e)

    finally:
        client.close()
        return listings

def addListing(listing):
    uri = "mongodb+srv://jbalaty:qU4vUqpJWiC4AFM8@cluster0.4jtkek7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.CraigslistSearches
    # Send a ping to confirm a successful connection

    try:
        client.admin.command('ping')
        collection = db.QuerySearches

        result = collection.insert_one(listing)
        print("Pinged your deployment. You successfully connected to MongoDB!")

    except Exception as e:
        print(e)

    finally:
        client.close()

def updateListing(id, list):
    uri = "mongodb+srv://jbalaty:qU4vUqpJWiC4AFM8@cluster0.4jtkek7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.CraigslistSearches
    # Send a ping to confirm a successful connection

    query = {"_id" : id}
    new_values = {"$set": list}

    try:
        client.admin.command('ping')
        collection = db.QuerySearches

        result = collection.update_one(query, new_values)
        print("Pinged your deployment. You successfully connected to MongoDB!")

    except Exception as e:
        print(e)

    finally:
        client.close()


def deleteListing(id):
    uri = "mongodb+srv://jbalaty:qU4vUqpJWiC4AFM8@cluster0.4jtkek7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client.CraigslistSearches
    # Send a ping to confirm a successful connection

    try:
        client.admin.command('ping')
        collection = db.QuerySearches
        document_to_delete = {"_id": id}

        result = collection.delete_one(document_to_delete)
        print("Pinged your deployment. You successfully connected to MongoDB!")

    except Exception as e:
        print(e)

    finally:
        client.close()


