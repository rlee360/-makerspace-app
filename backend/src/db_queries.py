import pymongo
import os
from bson.objectid import ObjectId
from bson import json_util

# with open('../db/mongo_uri.txt') as f:
#     mongo_uri = f.readline().strip()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["makerspace"]

def query_material(query_id):
    res = db['materials'].find_one({'_id': ObjectId(query_id)})
    return res

def filter_material(query):
    res = db['materials'].find(query)
    return res

def filter_requests(query):
    res = db['jobs'].find(query)
    return res

def query_job(query_id):
    if query_id == 'all':
        res = db["jobs"].find()
    else:
        res = db["jobs"].find_one({'_id': ObjectId(query_id)})
    print(res)
    return res

def insert_job(data):
    document = db["jobs"].insert_one(data)
    return document.inserted_id

def insert_material(data):
    document = db["materials"].insert_one(data)
    return document.inserted_id

def update_request(query_id, data):
    db['jobs'].update_one(
        { '_id': ObjectId(query_id) }, 
        { '$set': data }
    )
    return db['jobs'].find_one({'_id': ObjectId(query_id)})

def update_material(query_id, data):
    db['materials'].update_one(
        { '_id': ObjectId(query_id) }, 
        { '$set': data }
    )
    return db['materials'].find_one({'_id': ObjectId(query_id)})
