import os
import pymongo
from bson.son import SON
import textwrap
from tabulate import tabulate

"""
TODO List:
Try adding mimetype checks to the upload_file func
Implement all remaining unpopulated tables
"""

def insert_db(db_host, db_name, col_name, docs_list, update_field=None):
    client = pymongo.MongoClient(db_host)
    db = client[db_name]
    col = db[col_name]
    col.insert_many(docs_list)
    # used to skip repeat items and save some time if there is a unique id to search with
    # for doc in docs_list:
        # col.update_one(filter={update_field : doc[update_field]}, update={"$set" : doc}, upsert=True)

printer_doc = {
    "_id" : "FDM 1",
    "brand" : "Prusa",
    "model" : "i3 MK3",
    "build_volume" : [210, 210, 250],
    "maintenance" : False,
    "jobs" : []
}
# link is not required because it might not be applicable (i.e. bought in store, at event, etc.)
material_schema = {
    "title": "material",
    "required": [
        "name",
        "type",
        "material",
        "color",
        "brand",
        "grams_remaining",
        "valid_printers"
    ],
    "properties": {
        "name": {"bsonType": "string"},
        "type": {"bsonType": "string"},
        "material": {"bsonType": "string"},
        "color": {"bsonType": "string"},
        "brand": {"bsonType": "string"},
        "link" : {"bsonType": "string"},
        "grams_remaining" : {"bsonType": "number"},
        "valid_printers": {"bsonType": "array"}
    }
}

material_doc = {
    "name" : "Black PLA+",
    "type" : "filament",
    "material" : "PLA",
    "color" : "black",
    "brand" : "Inland",
    "link" : "https://www.microcenter.com/product/632388/inland-175mm-black-pla-pro-3d-printer-filament-1kg-spool-(22-lbs)",
    "grams_remaining" : 400,
    "valid_printers" : []
}

job_schema = {
    "title": "job",
    "required": [
        "name",
        "email",
        "material", # this will be an object id str?
        "shells",
        "infill",
        "top_bottom",
        "notes"
    ],
    "properties": {
        "name": {"bsonType": "string"},
        "email": {"bsonType": "string"},
        "material": {"bsonType": "string"},
        "shells": {"bsonType": "int"},
        "infill" : {"bsonType": "int"},
        "top_bottom" : {"bsonType": "int"},
        "notes": {"bsonType": "string"}
    }
}

job_doc = {
    "name": "benchy.stl",
    "email": "test@cooper.edu",
    "material": "",  # this relies on diff materials being available
    "shells": 2,
    "infill": 20,
    "top_bottom": 4,
    "notes": ""
}

def create_col_schema(db, col_name, schema):
    res = db.create_collection(col_name, validator={"$jsonSchema": schema})
    print(res)

def main():
    with open(os.getcwd() + '/mongo_uri.txt') as f:
        mongo_uri = f.readline().strip()
    client = pymongo.MongoClient(mongo_uri)
    db = client["makerspace"]
    create_col_schema(db, "materials", material_schema)
    create_col_schema(db, "jobs", job_schema)



if __name__ == "__main__":
    main()