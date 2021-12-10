import os

import bson
import pymongo
from bson.son import SON
import textwrap
from tabulate import tabulate
from bson.decimal128 import Decimal128

"""
TODO List:
Try adding mimetype checks to the upload_file func
Implement all remaining unpopulated tables
"""

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
        "valid_machines"
    ],
    "properties": {
        "name": {"bsonType": "string"},
        "type": {"bsonType": "string"},
        "material": {"bsonType": "string"},
        "color": {"bsonType": "string"},
        "brand": {"bsonType": "string"},
        "grams_remaining": {"bsonType": "number"},
        "link" : {"bsonType": "string"},
        "valid_machines": {"bsonType": ["array"]}
    }
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
        "notes",
        "status"
    ],
    "properties": {
        "name": {"bsonType": "string"},
        "email": {"bsonType": "string"},
        "material": {"bsonType": ["string", "objectId"]},
        "shells": {"bsonType": "int"},
        "infill" : {"bsonType": "int"},
        "top_bottom" : {"bsonType": "int"},
        "notes": {"bsonType": "string"},
        "status" : {"bsonType": "string"}, # inactive, queued, active, completed
        "operator" : {"bsonType": ["string", "array"]},
        "machine" : {"bsonType": ["string", "objectId"]},
        "material_used" : {"bsonType": "int"},
    }
}

operator_schema = {
    "title": "operator",
    "required": [
        "name",
        "email",
        "year",
        "wage",
        "hours"
    ],
    "properties": {
        "name": {"bsonType": "string"},
        "email": {"bsonType": "string"},
        "year": {"bsonType": "string"},
        "wage": {"bsonType": "number"},
        "hours": {"bsonType": "number"}
    }
}

machine_schema = {
    "title": "machine",
    "required": [
        "_id",
        "type",
        "brand",
        "model",
        "build_volume",
        "maintenance"
    ],
    "properties": {
        "_id": {"bsonType": "string"},
        "type": {"bsonType": "string"},
        "brand": {"bsonType": "string"},
        "build_volume": {"bsonType": "array"},
        "maintenance": {"bsonType": "bool"},
        "notes": {"bsonType": "array"},
        "jobs": {"bsonType": "array"},
    }
}

material_doc = {
    "name" : "Black PLA+",
    "type" : "filament",
    "material" : "PLA",
    "color" : "black",
    "brand" : "Inland",
    "grams_remaining" : 300,
    "link" : "https://www.microcenter.com/product/632388/inland-175mm-black-pla-pro-3d-printer-filament-1kg-spool-(22-lbs)",
    "valid_machines" : ["FDM 1", "FDM 2", "FDM 3", "FDM 4", "FDM 5", "FDM 6"]
}

job_doc = {
    "name": "benchy.stl",
    "email": "test@cooper.edu",
    "material": "",  # this relies on diff materials being available
    "shells": 2,
    "infill": 20,
    "top_bottom": 4,
    "notes": "",
    "status": "inactive",
    "machine": "FDM 1"
}

operator_doc = {
        "name": "John Smith",
        "email": "test_operator@cooper.edu",
        "year": "junior",
        "wage": 15.75,
        "hours": 2.5
}

machine_doc = {
    "_id" : "FDM 1",
    "type" : "FDM",
    "brand" : "Prusa",
    "model" : "i3 MK3",
    "build_volume" : [210, 210, 250],
    "maintenance" : False,
    "notes" : [],
    "jobs" : []
}

machine_docs = [
    ["FDM 1", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 2", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 3", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 4", "FDM", "Prusa", "i3 MK3", [210, 210, 250], True, ["x belt is too loose."], []],
    ["FDM 5", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 6", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM 7", "FDM", "Tinkerine", "Ditto Pro", [215, 165, 220], True, ["bed needs to be leveled", "nozzle is clogged"], []],

    ["SLA 1", "SLA", "Elegoo", "Mars", [120, 68, 155], False, [], []],

    ["Laser 1", "Laser", "Glowforge", "Pro", [304, 518, 0.6], False, [], []]
]

def machines_list_to_dict(doc):
    return {
        "_id": doc[0],
        "type": doc[1],
        "brand": doc[2],
        "model": doc[3],
        "build_volume": doc[4],
        "maintenance": doc[5],
        "notes": doc[6],
        "jobs": doc[7]
    }

def create_col_schema(db, col_name, schema):
    res = db.create_collection(col_name, validator={"$jsonSchema": schema})
    print(res)

def main():
    with open(os.getcwd() + '/mongo_uri.txt') as f:
        mongo_uri = f.readline().strip()
    client = pymongo.MongoClient(mongo_uri)
    db = client["makerspace"]
    for col in db.list_collection_names():
        db[col].drop()
    create_col_schema(db, "materials", material_schema)
    create_col_schema(db, "jobs", job_schema)
    create_col_schema(db, "operators", operator_schema)
    create_col_schema(db, "machines", machine_schema)
    db["materials"].insert_one(material_doc)
    db["jobs"].insert_one(job_doc)
    db["operators"].insert_one(operator_doc)

    machine_docs_dicts = map(machines_list_to_dict, machine_docs)

    db["machines"].insert_many(machine_docs_dicts)


if __name__ == "__main__":
    main()