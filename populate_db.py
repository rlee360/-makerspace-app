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
    # used to skip repeat items and save some time if restart is needed because of bad scrape
    for doc in docs_list:
        col.update_one(filter={update_field : doc[update_field]}, update={"$set" : doc}, upsert=True)

material_doc = {
    "name" : "Black PLA+",
    "type" : "filament",
    "material" : "PLA",
    "color" : "black",
    "brand" : "Inland",
    "valid_printers" : []
}

printer_doc = {
    "name" : ""
}

def main():
    with open(os.getcwd() + '/mongo_uri.txt') as f:
        mongo_uri = f.readline().strip()


if __name__ == "__main__":
    main()