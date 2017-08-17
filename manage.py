from healthtools_ke_api import app
from telegramHandler.manager import Manager, CONTEXT, TOKEN, PORT

from healthtools_ke_api.settings import TGBOT

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=int(PORT),
            ssl_context=CONTEXT,
            debug=True)
