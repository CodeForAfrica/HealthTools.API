from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException, default_exceptions
from api_healthtools_ke.nurses import nurses_api

app = Flask(__name__)
app.register_blueprint(nurses_api, url_prefix='/nurses')


def handle_error(error):
    '''Generic error handlers for all http exceptions'''
    response = {}
    status_code = 500
    if isinstance(error, HTTPException):
        status_code = error.code
    response["status_code"] = status_code
    response["error"] = str(error)
    response['description'] = error.description
    return jsonify(response), status_code


# change error handler for all http exceptions to return json instead of html
for code in default_exceptions.keys():
    app.errorhandler(code)(handle_error)
