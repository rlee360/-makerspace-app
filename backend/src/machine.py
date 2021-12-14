# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from flask import json, request, jsonify
from flask.blueprints import Blueprint
from markupsafe import escape
from bson import json_util
from flask_cors import CORS

from db_queries import *

machine_bp = Blueprint('machine', __name__, url_prefix='/api/machine')
CORS(machine_bp, resources={r'/*': {'origins': '*'}})

@machine_bp.route('/', methods=['GET'])
def _get_machine():
    if not request.args:
        res = query_machines()
        res = [mac['_id'] for mac in res]
        return jsonify(res)
    else:
        res = query_machines(request.args.get('machine'), False if request.args.get('maintenance') else True)
        res = [i for i in res] #{str(mat['_id']): f"{mat['color'].title()} ({mat['brand']})" for mat in res}
        return jsonify(res)
