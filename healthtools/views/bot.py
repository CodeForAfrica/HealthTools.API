from flask import Blueprint, redirect, request
from healthtools.bot import messenger_bot

blueprint = Blueprint('bot', __name__)

@blueprint.route('/bot/<adapter>', methods=['GET', 'POST'], strict_slashes=False)
def index(adapter='messenger'):
    if request.method == 'POST' :
        return messenger_bot.handle_messages
    else:
        return messenger_bot.handle_verification
          
