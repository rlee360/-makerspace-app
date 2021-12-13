import pymongo
import os
from bson.objectid import ObjectId
from bson import json_util

with open('../db/mongo_uri.txt') as f:
    mongo_uri = f.readline().strip()

client = pymongo.MongoClient(mongo_uri)
db = client["makerspace"]

def query_all_materials():
    return db['materials'].find({})

def query_material(query_id):
    res = db['materials'].find_one({'_id': ObjectId(query_id)})
    return res

def query_job(query_id):
    res = db["jobs"].find_one({'_id': ObjectId(query_id)})
    print(res)
    return res

def insert_job(data):
    document = db["jobs"].insert_one(data)
    return document.inserted_id

def insert_material(data):
    document = db["materials"].insert_one(data)
    return document.inserted_id

def update_material(query_id, data):
    db['materials'].update_one(
        { '_id': ObjectId(query_id) }, 
        { '$set': data }
    )
    return db['materials'].find_one({'_id': ObjectId(query_id)})