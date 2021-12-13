# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from flask import json, request, jsonify
from flask.blueprints import Blueprint
from markupsafe import escape
from werkzeug.utils import secure_filename
from bson import json_util

from helper import *
from db_queries import *

import os

request_bp = Blueprint('request', __name__, url_prefix='/api/request')

@request_bp.route('/update', methods=['POST'])
def _update_request():
    post_data = request.form.to_dict(flat=False)

    update_id = post_data.pop('id', None)[0]
    print(query_job(update_id))

    if query_job(update_id) == None:
        return jsonify({'status': 'failed', 'error': 'cannot find id'})

    # format to correct type
    if 'email' in post_data:
        # parse and validate emails
        invalid_emails = []
        parsed_emails = parse_emails(post_data['email'][0])

        for email in parsed_emails:
            if not valid_email(email):
                invalid_emails.append(email)

        if invalid_emails != []:
            return jsonify({'error': "Following emails are not cooper.edu: {}".format(invalid_emails)})
        else: 
            post_data['email'] = parsed_emails

    # one element to array
    if 'name' in post_data:
        post_data['name'] = post_data['name'][0]
    if 'notes' in post_data:
        post_data['notes'] = post_data['notes'][0]
    if 'filename' in post_data:
        post_data['filename'] = post_data['filename'][0]
    if 'class_id' in post_data:
        post_data['class_id'] = post_data['class_id'][0]
    if 'material' in post_data:
        post_data['material'] = post_data['material'][0]
    if 'status' in post_data:
        post_data['status'] = post_data['status'][0]
    if 'operator' in post_data:
        post_data['operator'] = post_data['operator'][0]
    if 'machine' in post_data:
        post_data['machine'] = post_data['machine'][0]

    # cast values to integer
    if 'shells' in post_data:
        post_data['shells'] = int(post_data['shells'][0])
    if 'infill' in post_data:
        post_data['infill'] = int(post_data['infill'][0])
    if 'top_bottom' in post_data:
        post_data['top_bottom'] = int(post_data['top_bottom'][0])
    if 'material_used' in post_data:
        post_data['material_used'] = int(post_data['material_used'][0])
    if 'queue_position' in post_data:
        post_data['queue_position'] = int(post_data['queue_position'][0])

    print(post_data)
    res = update_request(update_id, post_data)
    print(res)
    return jsonify({'status': 'success', 'new_data': json.loads(json_util.dumps(res))})

@request_bp.route('/status/<string:id>', methods=['GET'])
def _view_request(id):
    query_result = query_job(escape(id)) # needs to be escaped as well?
    print(query_result)
    return jsonify(json.loads(json_util.dumps(query_result)))

@request_bp.route('/filter', methods=['POST'])
def _filter_requests():
    post_data = request.form.to_dict(flat=False)
    
    for query in post_data:
        post_data[query] = post_data[query][0]

    res = filter_requests(post_data)
    return jsonify({'status': 'success', 'filtered': json.loads(json_util.dumps(res))})

@request_bp.route('/create', methods=['POST'])
def _create_request():
    # file handling
    files = request.files['files']

    # convert request form to mutable dict
    post_data = request.form.to_dict(flat=False)

    # parse and validate emails
    invalid_emails = []
    parsed_emails = parse_emails(post_data['email'][0])

    for email in parsed_emails:
        if not valid_email(email):
            invalid_emails.append(email)

    if invalid_emails != []:
        return jsonify({'error': "Following emails are not cooper.edu: {}".format(invalid_emails)})
    else: 
        post_data['email'] = parsed_emails

    # one element to array
    post_data['name'] = post_data['name'][0]
    post_data['notes'] = post_data['notes'][0]
    post_data['filename'] = post_data['filename'][0]
    post_data['class_id'] = post_data['class_id'][0]
    post_data['material'] = post_data['material'][0]

    # cast values to integer
    post_data['shells'] = int(post_data['shells'][0])
    post_data['infill'] = int(post_data['infill'][0])
    post_data['top_bottom'] = int(post_data['top_bottom'][0])

    # add default values
    post_data['status'] = 'inactive'
    post_data['operator'] = ''
    post_data['machine'] = ''
    post_data['material_used'] = 0
    post_data['queue_position'] = 0

    print(post_data)

    inserted_id = str(insert_job(post_data))

    new_filename = secure_filename(inserted_id + '-' + post_data['filename'])

    update_request(inserted_id, {'filename': new_filename})

    files.save(os.path.join('./uploads', new_filename))

    return jsonify({'status': 'success', 'id': str(inserted_id)})
