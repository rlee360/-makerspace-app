import pymongo
import os
from bson.objectid import ObjectId
from bson import json_util

__all__ = ["query_job", "insert_job"]

with open('../db/mongo_uri.txt') as f:
    mongo_uri = f.readline().strip()

client = pymongo.MongoClient(mongo_uri)
db = client["makerspace"]


def query_job(query_id):
    res = db["jobs"].find_one({'_id': query_id})
    print(res)
    return res

def insert_job(data):
    inserted_id = db["jobs"].insert_one(data)
    return inserted_id



