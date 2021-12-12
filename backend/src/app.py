# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from flask import Flask, flash, json, request, redirect, url_for, jsonify
from markupsafe import escape
from werkzeug.utils import secure_filename
import os

from bson import json_util

from flask_cors import CORS

from helper import *
from db_queries import *
from mail import *

UPLOAD_DIR = './uploads'

app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/api/sendmail', methods=['POST'])
def send_mail():
    post_data = request.form

    job = query_job(post_data['id'])

    try: 
        mes = create_message('sonbyj01@gmail.com', ', '.join(job['email']), post_data['subject'], post_data['message'])
        Gmail().send_message(mes)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'failed'})

@app.route('/api/material')
def view_all_material():
    return jsonify(json.loads(json_util.dumps(query_all_materials())))

@app.route('/api/material/add', methods=['POST'])
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

@app.route('/api/request/status/<string:id>')
def view_request(id):
    query_result = query_job(escape(id)) # needs to be escaped as well?
    return jsonify(json.loads(json_util.dumps(query_result)))

@app.route('/api/request/create', methods=['POST'])
def create_request():
    if request.method == 'POST':
        # file handling
        files = request.files['files']

        filename = secure_filename(files.filename)
        files.save(os.path.join(app.config['UPLOAD_DIR'], filename))

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

        inserted_id = insert_job(post_data)

        print(post_data)

        return jsonify({'status': 'success', 'id': str(inserted_id)})
    return
