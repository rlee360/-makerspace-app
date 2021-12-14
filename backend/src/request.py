# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from flask import json, request, jsonify, send_file
from flask.blueprints import Blueprint
from markupsafe import escape
from werkzeug.utils import secure_filename, send_from_directory
from bson import json_util
from flask_cors import CORS
import datetime

from helper import *
from db_queries import *
from sendmail import *

import os

request_bp = Blueprint('request', __name__, url_prefix='/api/request')
CORS(request_bp, resources={r'/*': {'origins': '*'}})

@request_bp.route('/update', methods=['POST'])
def _update_request():
    post_data = request.get_json()

    update_id = post_data.get('id', None)

    job = query_job(update_id)
    if job == None:
        return jsonify({'status': 'failed', 'error': 'cannot find id'}), 400

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
        post_data['name'] = post_data['name']
    if 'notes' in post_data:
        post_data['notes'] = post_data['notes']
    if 'filename' in post_data:
        post_data['filename'] = post_data['filename']
    if 'class_id' in post_data:
        post_data['class_id'] = post_data['class_id']
    if 'material' in post_data:
        post_data['material'] = post_data['material']
    if 'status' in post_data:
        post_data['status'] = post_data['status']
    if 'operator' in post_data:
        post_data['operator'] = post_data['operator']
    if 'machine' in post_data:
        post_data['machine'] = post_data['machine']

    # cast values to integer
    if 'shells' in post_data:
        post_data['shells'] = int(post_data['shells'])
    if 'infill' in post_data:
        post_data['infill'] = int(post_data['infill'])
    if 'top_bottom' in post_data:
        post_data['top_bottom'] = int(post_data['top_bottom'])
    if 'material_used' in post_data:
        post_data['material_used'] = int(post_data['material_used'])
    if 'queue_position' in post_data:
        post_data['queue_position'] = int(post_data['queue_position'])

    print(post_data)
    res = update_request(update_id, post_data)
    print(res)

    fns = job['filename'][job['filename'].find('-')+1:]

    try:
        if post_data['status'] == 'completed':
            mes = create_message('sonbyj01@gmail.com', 
                                ', '.join(query_job(update_id)['email']), 
                                '[Makerspace] Completed Print!', 
                                f'Your print {fns} is completed and is available for pick up. http://localhost:8080/job?id={job["_id"]}')
            Gmail().send_message(mes)
    except Exception as e:
        print("Error sending email")
        pass # can write to a log

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

@request_bp.route('/download/<string:id>', methods=['GET'])
def _download_request(id):
    filename = query_job(id)['filename']
    pathing = os.path.join('./uploads', filename)
    return send_file(pathing, as_attachment=True)

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
    post_data['datetime'] = datetime.datetime.now()

    print(post_data)

    inserted_id = str(insert_job(post_data))

    new_filename = secure_filename(inserted_id + '-' + post_data['filename'])

    update_request(inserted_id, {'filename': new_filename})

    files.save(os.path.join('./uploads', new_filename))

    return jsonify({'status': 'success', 'id': str(inserted_id)})
