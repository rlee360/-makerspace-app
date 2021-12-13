# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from ctypes import resize
from flask import Flask, flash, json, request, redirect, url_for, jsonify
from markupsafe import escape
from werkzeug.utils import secure_filename
import os

from bson import json_util

from flask_cors import CORS

from helper import *
from db_queries import *
from mail import *

sendmail_bp = Blueprint('sendmail', __name__, url_prefix='/api/sendmail')

@sendmail_bp.route('/', methods=['POST'])
def send_mail():
    post_data = request.form

    job = query_job(post_data['id'])

    try: 
        mes = create_message('sonbyj01@gmail.com', ', '.join(job['email']), post_data['subject'], post_data['message'])
        Gmail().send_message(mes)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'failed'})
