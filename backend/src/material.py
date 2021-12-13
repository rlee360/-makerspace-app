# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from ctypes import resize
from flask import Flask, flash, json, request, redirect, url_for, jsonify, Blueprint
from markupsafe import escape
from werkzeug.utils import secure_filename

from bson import json_util

from helper import *
from db_queries import *
from mail import *

material_bp = Blueprint('material', __name__, url_prefix='/api/material')

@material_bp.route('/update', methods=['POST'])
def api_update_material():
    post_data = request.form.to_dict(flat=False)

    update_id = post_data.pop('id', None)[0]
    print(query_material(update_id))

    if query_material(update_id) == None:
        return jsonify({'status': 'failed', 'error': 'cannot find id'})
    
    # format to correct type
    if 'type' in post_data:
        post_data['type'] = post_data['type'][0]
    if 'material' in post_data:
        post_data['material'] = post_data['material'][0]
    if 'color' in post_data:
        post_data['color'] = post_data['color'][0]
    if 'brand' in post_data:
        post_data['brand'] = post_data['brand'][0]
    if 'link' in post_data:
        post_data['link'] = post_data['link'][0]

    if 'grams_remaining' in post_data:
        post_data['grams_remaining'] = float(post_data['grams_remaining'][0])
    if 'price' in post_data:
        post_data['price'] = float(post_data['price'][0])
    if 'valid_machines' in post_data:
        post_data['valid_machines'] = post_data['valid_machines'][0].split(', ')
    if 'operator_notes' in post_data:
        post_data['operator_notes'] = post_data['operator_notes'][0].split(', ')
    if 'notes' in post_data:
        post_data['notes'] = post_data['notes'][0].split(', ')

    print(post_data)
    res = update_material(update_id, post_data)
    print(res)
    return jsonify({'status': 'success', 'new_data': json.loads(json_util.dumps(res))})

# view all materials available
@material_bp.route('/', methods=['GET'])
def view_all_material():
    return jsonify(json.loads(json_util.dumps(query_all_materials())))

@material_bp.route('/add', methods=['POST'])
def add_material():
    post_data = request.form.to_dict(flat=False)

    post_data['type'] = post_data['type'][0]
    post_data['material'] = post_data['material'][0]
    post_data['color'] = post_data['color'][0]
    post_data['brand'] = post_data['brand'][0]
    post_data['link'] = post_data['link'][0]

    post_data['grams_remaining'] = float(post_data['grams_remaining'][0])
    post_data['price'] = float(post_data['price'][0])
    post_data['valid_machines'] = post_data['valid_machines'][0].split(', ')

    if 'operator_notes' not in post_data:
        post_data['operator_notes'] = []
    
    if 'notes' not in post_data:
        post_data['notes'] = []

    print(post_data)
    inserted_id = insert_material(post_data)
    return jsonify({'status': 'success', 'id': str(inserted_id)})
