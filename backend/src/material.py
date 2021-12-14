# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from flask import json, request, jsonify
from flask.blueprints import Blueprint
from markupsafe import escape
from bson import json_util
from flask_cors import CORS

from db_queries import *

material_bp = Blueprint('material', __name__, url_prefix='/api/material')
CORS(material_bp, resources={r'/*': {'origins': '*'}})

@material_bp.route('/', methods=['GET'])
def _get_material():
    if not request.args:
        res = query_material_types()
        res = [mat_type['_id'] for mat_type in res]
        return jsonify(res)
    else:
        res = query_material_types(request.args.get('type'))
        res = {str(mat['_id']): f"{mat['color'].title()} ({mat['brand']})" for mat in res}
        return jsonify(res)


@material_bp.route('/update', methods=['POST'])
def _update_material():
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

@material_bp.route('/view/<string:id>', methods=['GET'])
def _view_material(id):
    query_result = query_material(escape(id)) # needs to be escaped as well?
    print(query_result)
    return jsonify(json.loads(json_util.dumps(query_result)))

@material_bp.route('/filter', methods=['POST'])
def _filter_material():
    post_data = request.form.to_dict(flat=False)
    
    for query in post_data:
        post_data[query] = post_data[query][0]
        
        if query in ['grams_remaining', 'price']:
            if '=<' in post_data[query]:
                post_data[query] = {'$lte': int(post_data[query].split('=<')[1])}
            elif '=>' in post_data[query]:
                post_data[query] = {'$gte': int(post_data[query].split('=>')[1])}
            else:
                return jsonify({'status': 'failed', 'error': 'invalid comparison for {}'.format(query)})

    res = filter_material(post_data)
    return jsonify({'status': 'success', 'filtered': json.loads(json_util.dumps(res))})

@material_bp.route('/add', methods=['POST'])
def _add_material():
    post_data = request.get_json()

    post_data['type'] = post_data['type']
    post_data['material'] = post_data['material']
    post_data['color'] = post_data['color']
    post_data['brand'] = post_data['brand']
    post_data['link'] = post_data['link']

    post_data['grams_remaining'] = float(post_data['grams_remaining'])
    post_data['price'] = float(post_data['price'])
    post_data['valid_machines'] = post_data['valid_machines'].split(', ')

    if 'operator_notes' not in post_data:
        post_data['operator_notes'] = []
    
    if 'notes' not in post_data:
        post_data['notes'] = []

    print(post_data)
    inserted_id = insert_material(post_data)
    return jsonify({'status': 'success', 'id': str(inserted_id)})
