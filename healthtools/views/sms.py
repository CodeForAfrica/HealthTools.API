from flask import Blueprint, request, jsonify

from healthtools.search import run_query
from healthtools.sms import process_sms


blueprint = Blueprint('sms_api', __name__)


@blueprint.route('/sms', methods=['GET'])
@blueprint.route('/sms/<adapter>', methods=['GET'])
def index(adapter=None):
    msg = request.args.get('msg')
    phone_no = request.args.get('phone_no')
    results = process_sms(msg, phone_no, adapter)
    return jsonify({'results': results, 'status': 'OK'})
