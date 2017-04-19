from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions
from healthtools_ke_api.nurses import nurses_api
from healthtools_ke_api.sms_handler import sms_handler


app = Flask(__name__)
app.register_blueprint(nurses_api, url_prefix='/nurses')
app.register_blueprint(sms_handler)


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
        print error
    return jsonify(response), status_code


# change error handler for all http exceptions to return json instead of html
for code in default_exceptions.keys():
    app.errorhandler(code)(handle_error)
