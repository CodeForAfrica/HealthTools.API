from flask import Blueprint, request, jsonify


blueprint = Blueprint('base_api', __name__)


@blueprint.route('/')
def index():
    return jsonify({'results': [], 'status': 'OK'})
