import json
import requests

from flask import Blueprint, request, jsonify

from telegram import Update

from healthtools_ke_api.views.telegram_bot import telegram_manager as manager


telegram_bot = Blueprint('telegram_bot', __name__)

# Initialize the Telegram Bot handler
manager.setup()


@telegram_bot.route('/' + manager.TOKEN, methods=['POST'])
def webhook():
    '''
    retrieve the message in JSON and then transform it to Telegram object

    Returns:
        json. The jsonified tranformation of the message passed
    '''

    if request.method == "POST":
        if not manager.DEBUG:
            # retrieve the message in JSON and then transform it to Telegram
            # object
            update = Update.de_json(request.get_json(force=True), manager.bot)

            # Start conversation
            manager.update_queue.put(update)

            return jsonify({
                "Success": "Telegram Bot is up and running on Webhooks",
                "status": 200})
        else:
            return jsonify({
                "Success": "Telegram Bot is up and running on polling",
                "status": 200})
    else:
        return jsonify({"Error": "Method not allowed", "status": 405})
