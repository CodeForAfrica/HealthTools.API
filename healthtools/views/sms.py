from flask import Blueprint, request, jsonify

from healthtools.search import run_query
from healthtools.sms import process_sms


blueprint = Blueprint('sms_api', __name__)


@blueprint.route('/sms', methods=['GET'])
@blueprint.route('/sms/<adapter>', methods=['GET'])
def index(adapter='mtech'):
    result = process_sms(request.args, adapter)

    # Error with process_sms (process_sms returns false result)
    if(not result):
        return jsonify({
            'result': {'msg': '', 'phone_no': ''},
            'status': 'FAILED',
            'msg': ''  # TODO: Pass process_sms message here.
        })

    # TODO: Log event here (send to Google Analytics)

    return jsonify({'result': result, 'status': 'OK'})
