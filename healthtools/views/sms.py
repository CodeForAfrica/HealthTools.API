from flask import Blueprint, request, jsonify, Response

from healthtools.search import run_query
from healthtools.sms import process_sms


blueprint = Blueprint('sms_api', __name__)


@blueprint.route('/sms', methods=['GET', 'POST'])
@blueprint.route('/sms/<adapter>', methods=['GET', 'POST'])
def index(adapter='mtech'):
    arguments = request.args
    if adapter == "africastalking":
        arguments = {
            'phoneNumber': request.values.get('from'),
            'message': request.values.get('text')
        }

    result = process_sms(arguments, adapter)

    # Error with process_sms (process_sms returns false result)
    if(not result):
        return jsonify({
            'result': {'msg': '', 'phone_no': ''},
            'status': 'FAILED',
            'msg': ''  # TODO: Pass process_sms message here.
        })

    # TODO: Log event here (send to Google Analytics)

    if(adapter == 'twilio'):
        return Response(result, mimetype='text/xml')

    return jsonify({'result': result, 'status': 'OK'})
