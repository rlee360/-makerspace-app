# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from ctypes import resize
from flask import Flask, flash, json, request, redirect, url_for, jsonify, Blueprint
from flask.blueprints import Blueprint
from markupsafe import escape
from werkzeug.utils import secure_filename
import os

from bson import json_util

from flask_cors import CORS

from helper import *
from db_queries import *
from mail import *

request_bp = Blueprint('request', __name__, url_prefix='/api/request')

@request_bp.route('/status/<string:id>', methods=['GET'])
def view_request(id):
    query_result = query_job(escape(id)) # needs to be escaped as well?
    print(query_result)
    return jsonify(json.loads(json_util.dumps(query_result)))

@request_bp.route('/create', methods=['POST'])
def create_request():
    if request.method == 'POST':
        # file handling
        files = request.files['files']

        filename = secure_filename(files.filename)
        files.save(os.path.join('./uploads', filename))

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

        inserted_id = insert_job(post_data)

        return jsonify({'status': 'success', 'id': str(inserted_id)})
    return
