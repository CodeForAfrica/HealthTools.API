from flask import Blueprint, request, jsonify

from healthtools.search import run_query
from healthtools.core import print_error

blueprint = Blueprint('search_api', __name__)

@blueprint.route('/search', methods=['GET'], strict_slashes=False)
@blueprint.route('/search/<doc_type>', methods=['GET'], strict_slashes=False)
def index(doc_type=None):
    query = request.args.get('q')

    try:
        result, doc_type = run_query(query, doc_type)
        response = jsonify({
            'result': result,
            'doc_type': doc_type,
            'status': 'OK'
        })

    except Exception as err:
        response =  jsonify({
            'result': {'hits': [], 'total': 0},
            'doc_type': doc_type,
            'status': 'FAILED',
            'msg': ''  # TODO: Pass run_query message here.
        })
        error = {
            "ERROR": "index()",
            "MESSAGE": str(err)
        }
        print_error(error)

    # TODO: Log event here (send to Google Analytics)
    return response
