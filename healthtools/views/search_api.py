from builtins import str
import logging
from flask import Blueprint, request, jsonify

from healthtools.search.query import run_query

blueprint = Blueprint('search_api', __name__)
log = logging.getLogger(__name__)

@blueprint.route('/search', methods=['GET'], strict_slashes=False)
@blueprint.route('/search/<doc_type>', methods=['GET'], strict_slashes=False)
def index(doc_type=None):
    query = request.args.get('q')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    try:
        result, doc_type = run_query(query, doc_type, page, per_page)
        response = jsonify({
            'page': page,
            'per_page': per_page,
            'result': result,
            'doc_type': doc_type,
            'status': 'OK'
        })

    except Exception as err:
        response =  jsonify({
            'result': {'hits': [], 'total': 0},
            'doc_type': doc_type,
            'status': 'FAILED',
            'msg': str(err)
        })
        log.error('Search failed \n' + str(err))

    # TODO: Log event here (send to Google Analytics)
    return response
