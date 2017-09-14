# from __future__ import absolute_import

import os
import sys

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions

from healthtools_ke_api.views.doctors import doctors_api
from healthtools_ke_api.views.nurses import nurses_api
from healthtools_ke_api.views.clinical_officers import clinical_officers_api
from healthtools_ke_api.views.nhif_inpatient import nhif_inpatient_api
from healthtools_ke_api.views.nhif_outpatient_cs import nhif_outpatient_cs_api
from healthtools_ke_api.views.nhif_outpatient import nhif_outpatient_api
  

from healthtools_ke_api.views.sms_handler import sms_handler
from healthtools_ke_api.views.telegram_bot import telegram_bot as tg


app = Flask(__name__)

app.register_blueprint(doctors_api, url_prefix='/doctors')
app.register_blueprint(nurses_api, url_prefix='/nurses')
app.register_blueprint(clinical_officers_api, url_prefix='/clinical-officers')
app.register_blueprint(nhif_inpatient_api, url_prefix='/nhif-inpatient')
app.register_blueprint(nhif_outpatient_cs_api, url_prefix='/nhif-outpatient-cs')
app.register_blueprint(nhif_outpatient_api, url_prefix='/nhif-outpatient')

app.register_blueprint(sms_handler)
app.register_blueprint(tg.telegram_bot)


@app.route("/")
def index():
    '''
    Landing endpoint

    '''
    msg = {
        "name": "HealthTools.KE-API",
        "authentication": [],
        "endpoints": {
            "/": {"methods": ["GET"]},
            "/nurses": {"methods": ["GET"]},
            "/doctors": {"methods": ["GET"]},
            "/clinical-officers": {"methods": ["GET"]},
            "/nhif-inpatient": {"methods": ["GET"]},
            "/nhif-outpatient-cs": {"methods": ["GET"]},
            "/nhif-outpatient": {"methods": ["GET"]}
        }
    }
    return jsonify(msg)


def handle_error(error):
    '''Generic error handlers for all http exceptions'''
    
    response = {}
    status_code = 500
    if isinstance(error, HTTPException):
        status_code = error.code
    response["status_code"] = status_code
    response["error"] = str(error)
    try:
        response['description'] = error.description
    except Exception as err:
        print err
    return jsonify(response), status_code


# change error handler for all http exceptions to return json instead of html
for code in default_exceptions.keys():
    app.errorhandler(code)(handle_error)
