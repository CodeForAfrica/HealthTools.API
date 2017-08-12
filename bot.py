import logging
import os
import re
import requests

from flask import Blueprint, request, current_app

from telegram import ReplyKeyboardMarkup, ParseMode
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)


from healthtools_ke_api.views.sms_handler import build_query_response


telegram_bot = Blueprint("telegram_bot", __name__)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

logger = logging.getLogger(__name__)


CHOOSING, TYPING_REPLY, QUERY = range(3)

# Custom keyboard with reply options
reply_keyboard = [["Clinical Officer", "Doctor", "Nurse"],
                  ["Health Facility", "NHIF Hospital"]]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


# import json
# import logging
# import os
# import telepot
# import requests

# from flask import Blueprint, request, jsonify, current_app

# from elastic_search import Elastic

# telegram_bot = Blueprint('telegrambot', __name__)
# logger = logging.getLogger('telegram.bot')


# @telegram_bot.route('/telegram', methods=['GET'])
# def index():
#     token = os.getenv("BOT_TOKEN")
#     TelegramBot = telepot.Bot(token)

#     '''
#     Landing endpoint
#     '''
#     msg = {
#         "name": "Telegram Bot",
#         "Bot Details": {

#             # TelegramBot.getMe() Output contains first_name, id, username
#             "details": TelegramBot.getMe(),
#             "getUpdate": TelegramBot.getUpdates()
#         },

#     }
#     return jsonify(msg)



def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append("%s - %s" % (key, value))

    return "\n".join(facts).join(["\n", "\n"])


def start(bot, update):
    # id = update.message.from_user.id
    chat_id = update.message.chat_id
    user = update.message.from_user.first_name

    welcome_msg = (
        "*Hello* %s.\n"
        "My name is `Healthtools Bot`.\n"
        "???????"  # Description of the app
        "\n"
        "Send /cancel to stop talking to me.\n\n'"
        "You can interact with me by sending these commands:\n" % user
    )

    bot.send_message(
        chat_id=chat_id,
        text=welcome_msg,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup,
    )

    # Call the next function
    return CHOOSING


def regular_choice(bot, update, user_data):
    """
    Show summary of user choice and input
    """
    chat_id = update.message.chat_id

    text = update.message.text
    user_data['choice'] = text

    msg = "Please enter the name of a `%s` you want to find" % text.capitalize()

    bot.send_message(
        chat_id=chat_id,
        text=msg,
        parse_mode=ParseMode.MARKDOWN,
    )

    return TYPING_REPLY


# TO DO: Queueing messages?????


def received_information(bot, update, user_data):
    """
    Show summary of user choice and input
    """
    chat_id = update.message.chat_id

    text = update.message.text
    choice = user_data['choice']
    user_data[choice] = text
    del user_data['choice']

    update.message.reply_text("Here's what you have asked me to search"
                              "%s"
                              % facts_to_str(user_data),
                              reply_markup=markup)

    bot.sendChatAction(chat_id=chat_id, action="typing")

    # Now we fetch the data
    results = fetch_data(user_data)
    update.message.reply_text("WE ARE HERE\n\t\t\t"
                              "%s"
                              % results,
                              reply_markup=markup)

    # Empty the user_data dictionary
    user_data.clear()

    return CHOOSING


def fetch_data(user_data):
    """
    Fetch the data requested by the user
    """
    query = user_data.keys()

    if query and len(query) == 1:
        keyword = str(query[0]).encode("utf-8")
        search_term = user_data[keyword]

        keyword = keyword.lower()

        query = keyword + " " + search_term
    else:
        pass

    # Sample input: "1. Doctors: DR. SAMUEL AMAI"
    msg = build_query_response(query)
    
    print ("\n")
    print ("WE ARE HERE")
    print ("SMS_BUILDER MESSAGE")
    print (msg)
    print ("\n")
    # update.message.reply_text("WE ARE HERE"
    #                           "%s"
    #                           % query,
    #                           reply_markup=markup)

    # Empty the dictionary
    # user_data.clear()

    # return CHOOSING


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text("Catch you later %s!" % user.first_name,
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def help(bot, update):
    update.message.reply_text("I am here to help you")


def error(bot, update, error):
    logger.warning("Update % s caused error % s" % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    token = os.getenv("BOT_TOKEN")
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Clinical Officer|Doctor|Nurse|Health Facility|NHIF Hospital)$',
                                    regular_choice,
                                    pass_user_data=True),
                       ],

            QUERY: [MessageHandler(Filters.text,
                                   regular_choice,
                                   pass_user_data=True),
                    ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("help", help))

    # TO DO: Add settings
    # dp.add_handler(CommandHandler("settings", settings))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
