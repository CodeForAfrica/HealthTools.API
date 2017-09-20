from flask import Blueprint, request, jsonify

from healthtools.search import run_query


blueprint = Blueprint('search_api', __name__)


@blueprint.route('/search', methods=['GET'])
@blueprint.route('/search/<doc_type>', methods=['GET'])
def index(doc_type=None):
    query = request.args.get('q')
    results = run_query(query, doc_type)

    # Error with run_query (run_query returns false)
    if(not results):
        return jsonify({
            'results': [],
            'status': 'FAILED',
            'msg': ''  # TODO: Pass run_query msg here.
        })

    return jsonify({'results': results, 'status': 'OK'})
