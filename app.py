# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from flask import Flask, flash, json, request, redirect, url_for, jsonify
from markupsafe import escape
from werkzeug.utils import secure_filename
import os

from bson.objectid import ObjectId
from bson import json_util

from pymongo import MongoClient

from flask_cors import CORS

from helper import *
from config import *

UPLOAD_DIR = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR

client = MongoClient('localhost', 27017)
db = client[MONGO_DB]
collection = db['requests']

CORS(app, resources={r'/*': {'origins': '*'}})

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_status(id):
    # todo - database
    pass

@app.route('/status/<string:id>')
def show_status(id):
    status = get_status(escape(id))

@app.route('/request/view/<string:id>')
def view_request(id):
    print(type(collection.find_one({'_id': ObjectId(id)})))
    return jsonify(json.loads(json_util.dumps(collection.find_one({'_id': ObjectId(id)}))))

@app.route('/request/create', methods=['GET', 'POST'])
def create_request():
    if request.method == 'POST':
        post_data = request.get_json()

        # parse and validate emails
        invalid_emails = []
        parsed_emails = parse_emails(post_data['email'])

        for email in parsed_emails:
            if not valid_email(email):
                invalid_emails.append(email)
        
        print(parsed_emails)
        
        if invalid_emails != []:
            return jsonify({'error': "Following emails are not cooper.edu: {}".format(invalid_emails)})
        else: 
            post_data['email'] = parsed_emails
        
        print(post_data)
        document = collection.insert_one(post_data)

        return jsonify({'status': 'success', 'id': str(document.inserted_id)})
    return

# https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if post request has file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select a file, browser submits empty file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_DIR'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''
