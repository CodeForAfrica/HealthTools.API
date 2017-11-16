from healthtools.views.base_api import blueprint as base_api
from healthtools.views.search_api import blueprint as search_api
from healthtools.views.sms import blueprint as sms

def mount_app_blueprints(app):
    app.register_blueprint(base_api)
    app.register_blueprint(search_api)
    app.register_blueprint(sms)
