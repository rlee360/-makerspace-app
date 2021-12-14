import os

import bson
import pymongo
from bson.son import SON
from bson.decimal128 import Decimal128
import datetime

"""
TODO List:
Try adding mimetype checks to the upload_file func
Implement all remaining unpopulated tables
"""

# link is not required because it might not be applicable (i.e. bought in store, at event, etc.)
material_schema = {
    "title": "material",
    "required": [
        "type",
        "material",
        "color",
        "brand",
        "grams_remaining",
        "valid_machines"
    ],
    "properties": {
        "type": {"bsonType": "string"},
        "material": {"bsonType": "string"},
        "color": {"bsonType": "string"},
        "brand": {"bsonType": "string"},
        "grams_remaining": {"bsonType": "number"},
        "notes": {"bsonType": ["array"]},
        "link" : {"bsonType": "string"},
        "operator_notes": {"bsonType": ["array"]},
        "price": {"bsonType": "number"},
        "valid_machines": {"bsonType": ["array"]}
    }
}

job_schema = {
    "title": "job",
    "required": [
        "filename",
        "email",
        "name",
        "class_id",
        "material", # this will be an object id str?
        "shells",
        "infill",
        "top_bottom",
        "notes",
        "status",
        "datetime"
    ],
    "properties": {
        "filename": {"bsonType": "string"},
        "email": {"bsonType": ["string", "array"]},
        "name": {"bsonType": "string"},
        "class_id": {"bsonType": "string"},
        "material": {"bsonType": ["string", "objectId"]},
        "shells": {"bsonType": "int"},
        "infill" : {"bsonType": "int"},
        "top_bottom" : {"bsonType": "int"},
        "notes": {"bsonType": "string"},
        "status" : {"bsonType": "string"}, # inactive, queued, active, completed
        "operator" : {"bsonType": "string"},
        "machine" : {"bsonType": ["string", "objectId"]},
        "material_used" : {"bsonType": "int"},
        "queue_position" : {"bsonType": "int"},
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
    # "name" : "Black PLA+",
    "type" : "filament",
    "material" : "PLA",
    "color" : "black",
    "brand" : "Inland",
    "grams_remaining" : 300,
    "link" : "https://www.microcenter.com/product/632388/inland-175mm-black-pla-pro-3d-printer-filament-1kg-spool-(22-lbs)",
    "notes" : [],
    "valid_machines": ["FDM_1", "FDM_2", "FDM_3", "FDM_4", "FDM_5", "FDM_6"],
    "price": 18.99,
    "operator_notes" : []
}

material_docs = [
    {
        "type": "filament",
        "material": "PLA",
        "color": "black",
        "brand": "Inland",
        "grams_remaining": 300,
        "link": "https://www.microcenter.com/product/632388/inland-175mm-black-pla-pro-3d-printer-filament-1kg-spool-(22-lbs)",
        "notes": [],
        "valid_machines": ["FDM_1", "FDM_2", "FDM_3", "FDM_4", "FDM_5", "FDM_6"],
        "price": 18.99,
        "operator_notes": []
    },
    {
        "type": "filament",
        "material": "PLA",
        "color": "white",
        "brand": "Inland",
        "grams_remaining": 950,
        "link": "https://www.microcenter.com/product/632389/inland-175mm-white-pla-pro-3d-printer-filament-1kg-spool-(22-lbs)",
        "notes": [],
        "valid_machines": ["FDM_1", "FDM_2", "FDM_3", "FDM_4", "FDM_5", "FDM_6"],
        "price": 18.99,
        "operator_notes": ["Seem to have complaints about poor outer wall finish. Might be inaccurate filament"]
    },
    {
        "type": "filament",
        "material": "PETG",
        "color": "white",
        "brand": "Atomic",
        "grams_remaining": 1000,
        "link": "https://atomicfilament.com/products/bright-white-opaque-petg-pro?_pos=1&_sid=b3a57fe67&_ss=r&variant=11046098497",
        "notes": [],
        "valid_machines": ["FDM_4", "FDM_5", "FDM_6"],
        "price": 32.99,
        "operator_notes": ["Expensive, but prints really well"]
    },
    {
        "type": "filament",
        "material": "ABS",
        "color": "blue",
        "brand": "Hatchbox",
        "grams_remaining": 800,
        "link": "https://www.amazon.com/HATCHBOX-3D-Filament-Dimensional-Accuracy/dp/B00J0H3PG0/?th=1",
        "notes": ["Models with small bases prone to failing due to warping."],
        "valid_machines": ["FDM_6"],
        "price": 21.99,
        "operator_notes": ["Excessive warping, do not buy again."]
    },
    {
        "type": "filament",
        "material": "PETG",
        "color": "black",
        "brand": "eSun",
        "grams_remaining": 500,
        "link": "https://www.amazon.com/eSUN-1-75mm-Filament-Printer-Opaque/dp/B00ZAUQZTA/ref=sr_1_5?keywords=esun+filament&qid=1639520018&sr=8-5",
        "notes": [""],
        "valid_machines": ["FDM_5","FDM_6"],
        "price": 22.99,
        "operator_notes": ["Pretty inexpensive and prints quite well."]
    },
    {
        "type": "filament",
        "material": "PLA",
        "color": "clear",
        "brand": "eSun",
        "grams_remaining": 700,
        "link": "https://www.amazon.com/eSUN-1-75mm-Printer-Filament-2-2lbs/dp/B07QBM53H5/ref=sr_1_7?keywords=esun+filament&qid=1639520018&sr=8-7",
        "notes": [""],
        "valid_machines": ["FDM_2","FDM_3"],
        "price": 20.99,
        "operator_notes": ["Material is very brittle"]
    },
    {
        "type": "filament",
        "material": "PLA",
        "color": "purple",
        "brand": "TTYT3D",
        "grams_remaining": 200,
        "link": "https://www.amazon.com/Dark-Violet-Purple-Printer-Filament/dp/B07WC8R1PD/ref=sr_1_2_sspa?keywords=esun+filament&qid=1639520806&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExQjdaQkdJVkFCRkJHJmVuY3J5cHRlZElkPUEwMjU0NTg2MkVIV0szWUs0WVBaOCZlbmNyeXB0ZWRBZElkPUEwMTg2NDI3MktQUTdPMkowUUc1SCZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=",
        "notes": ["Very nice colors"],
        "valid_machines": ["FDM_1"],
        "price": 24.99,
        "operator_notes": ["Buy again."]
    },
    {
        "type": "filament",
        "material": "PLA",
        "color": "red",
        "brand": "eSun",
        "grams_remaining": 400,
        "link": "https://www.amazon.com/eSUN-Printer-Filament-Diameter-Pantone/dp/B07983PYHT/ref=sr_1_9?keywords=esun+filament&qid=1639520756&sr=8-9",
        "notes": [],
        "valid_machines": ["FDM_4"],
        "price": 25.88,
        "operator_notes": []
    },
    {
        "type": "filament",
        "material": "PLA",
        "color": "black",
        "brand": "eSun",
        "grams_remaining": 900,
        "link": "https://www.amazon.com/eSUN-Filament-Printer-Printing-Printers/dp/B08RS3FB37/ref=sr_1_14?keywords=esun%2Bfilament&qid=1639521086&sr=8-14&th=1",
        "notes": [],
        "valid_machines": [],
        "price": 59.99,
        "operator_notes": []
    },
    {
        "type": "filament",
        "material": "PLA",
        "color": "black",
        "brand": "Overture",
        "grams_remaining": 700,
        "link": "https://www.amazon.com/OVERTURE-Filament-Consumables-Dimensional-Accuracy/dp/B07PGYHYV8/ref=sr_1_1_sspa?keywords=pet+filament&qid=1639521317&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFBM1M5NFNLSTFNS0omZW5jcnlwdGVkSWQ9QTA3MDQzMTYzSk1SRjZCVFRXUlVNJmVuY3J5cHRlZEFkSWQ9QTA1MDg4MzQyWTJCUkVQOEFIMDVBJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==",
        "notes": ["Good quality"],
        "valid_machines": ["FDM_1", "FDM_4"],
        "price": 21.99,
        "operator_notes": []
    },
]

job_doc = {
    "filename": "benchy.stl",
    "email": "test@cooper.edu",
    "name": "test thing",
    "class_id": "ME412",
    "material": "",  # this relies on diff materials being available
    "shells": 2,
    "infill": 20,
    "top_bottom": 4,
    "notes": "",
    "status": "inactive",
    "machine": "",
    "queue_position": 1,
    "datetime": datetime.datetime.now()
}

# job_doc = {
#     "filename": "benchy.stl", # upload button
#     "email": "test@cooper.edu", # type in box
#     "material": "", # drop down menu
#     "shells": 2, # >= 0 increment/decrement button
#     "infill": 20, # >= 0, <= 100 increment/decrement button
#     "top_bottom": 4, # >= 0 increment/decrement button
#     "notes": "", # text box, resizeable
# }

operator_doc = {
        "name": "John Smith",
        "email": "test_operator@cooper.edu",
        "year": "junior",
        "wage": 15.75,
        "hours": 2.5
}

machine_doc = {
    "_id" : "FDM_1",
    "type" : "FDM",
    "brand" : "Prusa",
    "model" : "i3 MK3",
    "build_volume" : [210, 210, 250],
    "maintenance" : False,
    "notes" : [],
    "jobs" : []
}

machine_docs = [
    ["FDM_1", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM_2", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM_3", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM_4", "FDM", "Prusa", "i3 MK3", [210, 210, 250], True, ["x belt is too loose."], []],
    ["FDM_5", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM_6", "FDM", "Prusa", "i3 MK3", [210, 210, 250], False, [], []],
    ["FDM_7", "FDM", "Tinkerine", "Ditto Pro", [215, 165, 220], True, ["bed needs to be leveled", "nozzle is clogged"], []],

    ["SLA_1", "SLA", "Elegoo", "Mars", [120, 68, 155], False, [], []],

    ["Laser_1", "Laser", "Glowforge", "Pro", [304, 518, 0.6], False, [], []]
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
    db["materials"].insert_many(material_docs)
    #db["jobs"].insert_one(job_doc)
    db["operators"].insert_one(operator_doc)

    machine_docs_dicts = map(machines_list_to_dict, machine_docs)
    db["machines"].insert_many(machine_docs_dicts)


if __name__ == "__main__":
    main()
