import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import logging

from healthtools.core import create_app
from healthtools.views import mount_app_blueprints


log = logging.getLogger('healthtools')

app = create_app()
mount_app_blueprints(app)


if __name__ == "__main__":
    app.run()
