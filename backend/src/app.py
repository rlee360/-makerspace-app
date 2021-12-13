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
from material import material_bp
from request import request_bp

UPLOAD_DIR = './uploads'

app = Flask(__name__)
app.register_blueprint(material_bp)
app.register_blueprint(request_bp)
app.config['UPLOAD_DIR'] = UPLOAD_DIR

CORS(app, resources={r'/*': {'origins': '*'}})
