import json
import requests

from flask import Blueprint, request, jsonify
from telegram import Update

from healthtools_ke_api.views.telegram_bot import telegram_manager as manager


telegram_bot = Blueprint('telegram_bot', __name__)

# Initialize the Telegram Bot handler
manager.setup()


@telegram_bot.route('/' + manager.TOKEN, methods=['GET', 'POST'])
def webhook():
    if request.method == "POST":
        if not manager.DEBUG:

            print ("\n-----WE ARE HERE: request.get_json-----")
            print ("\nBase URL:", request.base_url)
            print ("\nurl_root:", request.url_root)
            print ("\nrequest.json:", request.get_json(force=True))
            print ("\n")

            # retrieve the message in JSON and then transform it to Telegram
            # object
            update = Update.de_json(request.get_json(force=True), manager.bot)

            # Start conversation
            manager.update_queue.put(update)

            return jsonify({"Success": "Telegram Bot is up and running",
                            "status": 200})
        else:
            return jsonify({"Success": "Telegram Bot is up and running",
                            "status": 200})
    else:
        return jsonify({"Error": "Method not allowed", "status": 405})


@telegram_bot.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({"Success": "This takes you to the telegram Bot",
                    "status": 200})
