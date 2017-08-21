import json
import logging
import os
import re
import requests
import string
import time

from flask import Flask, Blueprint, request, jsonify, current_app

from queue import Queue
from threading import Thread

from telegram import Bot, Update, ReplyKeyboardMarkup, ParseMode, ReplyKeyboardRemove, WebhookInfo
from telegram.ext import (Dispatcher, Updater, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, RegexHandler)

from healthtools_ke_api.views.build_query import BuildQuery
from healthtools_ke_api.settings import DEBUG, TGBOT

TOKEN = TGBOT["BOT_TOKEN"]
SERVER_IP = TGBOT["SERVER_IP"]
# PORT = TGBOT["TELEGRAM_PORT"]
# CERT_FILE = TGBOT["CERT_FILE"]
# KEY_FILE = TGBOT["KEY_FILE"]

# WEBHOOK_URL = TGBOT["BOT_WEBHOOK_URL"]
WEBHOOK_URL = "https://htapi-test.herokuapp.com"
WEBHOOK_URL = WEBHOOK_URL + "/" + TOKEN

# CONTEXT = (CERT_FILE, KEY_FILE)

# States
CHOOSING, TYPING_REPLY = range(2)


# Enable logging
if DEBUG:
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


logger = logging.getLogger("telegram.bot.Manager")

bot = Bot(TOKEN)

# if DEBUG:
updater = Updater(bot=bot)
dp = updater.dispatcher
# else:
#     update_queue = Queue()
#     dp = Dispatcher(bot, update_queue)
    # dp = Dispatcher(bot, None, workers=0)
    # thread = Thread(
    #     target=dispatcher.start, name='dispatcher')
    # thread.start()

build_query = BuildQuery()

# Custom keyboard with reply options
reply_keyboard = [["Clinical Officer", "Doctor", "Nurse"],
                  ["NHIF Accredited Hospital: Inpatient",
                   "NHIF Accredited Hospital: Outpatient"],
                  ["Health Facility"]]

markup = ReplyKeyboardMarkup(
    reply_keyboard, one_time_keyboard=True)


def start_polling():
    """
    Activates schedulers of all setups, and starts polling updates from Telegram.
    """

    logger.info('Start polling')

    # Delete any webhook
    updater.bot.set_webhook()

    updater.start_polling(poll_interval=1.0, timeout=20)
    updater.idle()


# def set_webhook(webhook_url, listen, port, url_path, cert=None, key=None):
def set_webhook(webhook_url, cert=None, key=None):
    """
    Activates schedulers of all setups, setups webhook, and
    starts small http server to listen for updates via this webhook.
    """

    # logger.debug('Start webhook')
    logger.info('Start webhook')

    # Delete any webhook to avoid Conflict: terminated by other setWebhook
    bot.deleteWebhook()

    # # Using nginx
    # time.sleep(5)  # to avoid error 4RetryAfter: Flood control exceeded

    # updater.start_webhook(listen='127.0.0.1', port=5000, url_path='TOKEN1')
    # updater.bot.set_webhook(url='https://example.com/TOKEN1',
    #                                 certificate=open('cert.pem', 'rb'))

    # Using the integrated webhook server
    # updater.start_webhook(listen=listen, port=port,
    #                            url_path=url_path, cert=cert, key=key,
    #                            webhook_url=webhook_url)

    # Using Heroku
    time.sleep(5)
    updater.start_webhook(listen="0.0.0.0", port=5000, url_path=TOKEN)
    updater.bot.set_webhook(url=webhook_url)
    print ("\nWebhook set: %s \n", bot.getWebhookInfo().url)
    updater.idle()

    # time.sleep(5)  # to avoid error 4RetryAfter: Flood control exceeded
    # bot.setWebhook(url=webhook_url
                #    certificate=CERT_FILE
                #    )

    # print ("\nWebhook set: %s \n", bot.getWebhookInfo().url)
    # updater.idle()

# def webhook():
#     logger.info('Start webhook')
#     update = telegram.update.Update.de_json(request.get_json(force=True))
#     bot.sendMessage(chat_id=update.message.chat_id, text='Hello, there')

# return 'OK'


def setup():
    """
    Set up how to receive new updates for the bot
    1. If DEBUG=True, use polling
    2. else, we use a webhook
    """
    if DEBUG:
        start_polling()
    else:
        set_webhook(
            webhook_url=WEBHOOK_URL,
            # listen=SERVER_IP,
            # port=int(PORT),
            # url_path=token,
            # cert=CERT_FILE,
            # key=KEY_FILE
        )

        # thread = Thread(target=dispatcher.start, name='dispatcher')
        # thread.start()

        # return (update_queue, dispatcher)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append("%s - %s" % (key, value))

    return "\n".join(facts).join(["\n", "\n"])


def start(bot, update):

    chat_id = update.message.chat_id
    user = update.message.from_user.first_name

    # logger.debug('Conversation started by % s' % user)
    logger.info('Conversation started by % s' % user)

    welcome_msg = (
        "*Hello* %s.\n"
        "My name is `Healthtools Bot`.\n\n"
        "*Here's what I can do for you:*\n"
        "1. Check to see if your doctor, nurse, or clinical officer is registered\n"
        "2. Find out which facilities your NHIF card will cover in your county\n"
        "3. Find the nearest doctor or health facility\n"
        "\nSend /cancel to stop talking to me.\n" % user
    )

    bot.send_message(
        chat_id=chat_id,
        text=welcome_msg,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup,
    )

    # Call the next function
    # return CHOOSING
    return CHOOSING

# TODO: Handle edited_message in these too


def regular_choice(bot, update, user_data):
    """
    Show summary of user choice and input
    """
    chat_id = update.message.chat_id

    text = update.message.text
    user_data['choice'] = text

    msg = "Please enter the name of a `%s` you want to find" % text.title()

    bot.send_message(
        chat_id=chat_id,
        text=msg,
        parse_mode=ParseMode.MARKDOWN,
    )

    # Call next function: received_information
    # return TYPING_REPLY
    return TYPING_REPLY


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
                              % facts_to_str(user_data))

    bot.sendChatAction(chat_id=chat_id, action="typing")

    # Now we fetch the data
    results = fetch_data(user_data)

    print("\n")
    print(results)

    # Remove multiple whitespaces
    results = re.sub(" +", " ", str(results[0]))
    search_msg = (
        "*Search Results*\n"
        "%s" % results
    )

    bot.send_message(
        chat_id=chat_id,
        text=search_msg,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup,
    )

    # Empty the user_data dictionary
    user_data.clear()

    # Call functi0n regular_choice
    # return CHOOSING
    return CHOOSING


def fetch_data(user_data):
    """
    Fetch the data requested by the user
    """

    # TO DO: How many results to fetch
    # If many, pagination
    # Use InlineQueryHandler

    query = user_data.keys()[-1]

    if query:
        keyword = str(query).encode("utf-8")
        search_term = user_data[keyword]

        if re.search("NHIF Accredited Hospital", keyword):
            keyword = re.sub("accredited hospital: ", "",
                             keyword, flags=re.IGNORECASE)

        if keyword == "Health Facility":
            keyword = "hf"

        keyword = keyword.lower()
        query = keyword + " " + search_term

    else:
        return "Keyword not valid"

    search_results = build_query.build_query_response(query)
    return search_results


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." %
                user.first_name)
    update.message.reply_text("Catch you later %s! Hope to talk to you soon" % user.first_name,
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def help(bot, update):
    update.message.reply_text("I am here to help you")


def unknown(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text="Sorry, I didn't understand that command.")


def error(bot, update, error):
    logger.warning("Update % s caused error % s" % (update, error))


def main():
    dp.add_handler(CommandHandler('help', help))
    # Add conversation handler with the states
    dp.add_handler(ConversationHandler(
        # Handler object to trigger the start of the conversation
        entry_points=[CommandHandler('start', start)],

        # Conversation states
        states={
            CHOOSING: [RegexHandler('^(Clinical Officer|Doctor|Nurse|Health Facility|NHIF Accredited Hospital)',
                                    regular_choice,
                                    pass_user_data=True),
                       ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],

        },

        fallbacks=[CommandHandler('cancel', cancel)],

        # Allow user can restart a conversation with an entry point
        allow_reentry=True
    ))

    # dispatcher.add_handler(conv_handler)
    dp.add_handler(
        MessageHandler(Filters.command, unknown))
    dp.add_error_handler(error)

    if DEBUG:
        start_polling()
    else:
        # thread = Thread(target=dp.start, name='dp')
        # thread.start()

        # return (update_queue, dp)
        set_webhook(
            webhook_url=WEBHOOK_URL
            # cert=CERT_FILE,
            # key=KEY_FILE
        )

main()


telegram_bot = Flask(__name__)


@telegram_bot.route('/' + TOKEN, methods=['GET', 'POST'])
def webhook():
    if request.method == "POST":

        # retrieve the message in JSON and then transform it to Telegram object

        print ("\n-----WE ARE HERE: request.get_json-----")
        print ("\nBase URL:", request.base_url)
        print ("\nurl_root:", request.url_root)
        print ("\nrequest.json:", request.get_json())
        print ("\n")

        update = Update.de_json(request.get_json(force=True), bot)

        logger.info("Update received! " + update.message.text)
        dp.process_update(update)
        update_queue.put(update)
        return "OK"
    else:
        pass
        # return redirect("https://telegram.me/links_forward_bot", code=302)


@telegram_bot.route('/', methods=['GET', 'POST'])
def index():
    return "OK"
    # return redirect("https://telegram.me/links_forward_bot", code=302)


if __name__ == '__main__':

    # if not DEBUG:
    #     set_webhook(
    #         webhook_url=WEBHOOK_URL
    #         # cert=CERT_FILE,
    #         # key=KEY_FILE
    #     )
    # else:
    #     pass

    telegram_bot.run(host='0.0.0.0',
                     #  port=int(PORT),
                     port=5000
                     #  ssl_context=CONTEXT,
                     #  debug=True
                     )
