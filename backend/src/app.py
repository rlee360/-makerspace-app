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

@app.route('/api/request/status/<string:id>')
def view_request(id):
    query_result = query_job(escape(id)) # needs to be escaped as well?
    return jsonify(json.loads(json_util.dumps(query_result)))

@app.route('/api/request/create', methods=['GET', 'POST'])
def create_request():
    if request.method == 'POST':
        files = request.files['files']

        filename = secure_filename(files.filename)
        files.save(os.path.join(app.config['UPLOAD_DIR'], filename))

        post_data = request.form.to_dict(flat=False)
        print(post_data)

        # parse and validate emails
        invalid_emails = []
        parsed_emails = parse_emails(post_data['email'][0])

        for email in parsed_emails:
            if not valid_email(email):
                invalid_emails.append(email)
        
        print(parsed_emails)
        
        if invalid_emails != []:
            return jsonify({'error': "Following emails are not cooper.edu: {}".format(invalid_emails)})
        else: 
            post_data['email'] = parsed_emails
        
        print(post_data, type(post_data))
        inserted_id = insert_job(post_data)

        return jsonify({'status': 'success', 'id': str(inserted_id)})
    return
