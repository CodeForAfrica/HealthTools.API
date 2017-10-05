import logging

from healthtools.core import create_app
from healthtools.views import mount_app_blueprints


log = logging.getLogger('healthtools')

app = create_app()
mount_app_blueprints(app)


if __name__ == "__main__":
     app.run()