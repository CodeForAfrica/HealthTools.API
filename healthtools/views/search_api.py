from flask import Blueprint, request, jsonify

from healthtools.search import run_query
from healthtools.search.wit_ai import wit_run_query


blueprint = Blueprint('search_api', __name__)


@blueprint.route('/wit_search', methods=['GET'], strict_slashes=False)
def wit_search_index():
    doc_type = None
    query = request.args.get('q')
    result, doc_type = wit_run_query(query, doc_type)

    # Error with wit_run_query (run_query returns false)
    if(not result):
        return jsonify({
            'result': {'hits': [], 'total': 0},
            'doc_type': doc_type,
            'status': 'FAILED',
            'msg': ''  # TODO: Pass run_query message here.
        })

    # TODO: Log event here (send to Google Analytics)

    return jsonify({'result': result, 'doc_type': doc_type, 'status': 'OK'})

@blueprint.route('/search', methods=['GET'], strict_slashes=False)
@blueprint.route('/search/<doc_type>', methods=['GET'], strict_slashes=False)
def index(doc_type=None):
    query = request.args.get('q')
    result, doc_type = run_query(query, doc_type)

    # Error with run_query (run_query returns false)
    if(not result):
        return jsonify({
            'result': {'hits': [], 'total': 0},
            'doc_type': doc_type,
            'status': 'FAILED',
            'msg': ''  # TODO: Pass run_query message here.
        })

    # TODO: Log event here (send to Google Analytics)

    return jsonify({'result': result, 'doc_type': doc_type, 'status': 'OK'})
