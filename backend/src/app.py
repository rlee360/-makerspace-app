# https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/

from flask import Flask

from flask_cors import CORS

from material import material_bp
from machine import machine_bp
from request import request_bp
from sendmail import sendmail_bp

app = Flask(__name__)

app.register_blueprint(material_bp)
app.register_blueprint(machine_bp)
app.register_blueprint(request_bp)
app.register_blueprint(sendmail_bp)

CORS(app, resources={r'/*': {'origins': '*'}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
