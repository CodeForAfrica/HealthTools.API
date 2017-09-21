from flask import Blueprint, redirect


blueprint = Blueprint('base_api', __name__)


@blueprint.route('/')
def index():
    # TODO: Redirect to HealthTools docs instead
    return redirect('https://github.com/CodeForAfricaLabs/HealthTools.API')
