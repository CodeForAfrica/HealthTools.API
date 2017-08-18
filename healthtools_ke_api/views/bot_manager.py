import logging
import os
import re
import requests
import string
import time

from queue import Queue
from threading import Thread

from telegram import Bot, ReplyKeyboardMarkup, ParseMode, ReplyKeyboardRemove, WebhookInfo
from telegram.ext import (Dispatcher, Updater, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, RegexHandler)
from healthtools_ke_api.views.build_query import BuildQuery
from healthtools_ke_api.settings import DEBUG, TGBOT

TOKEN = TGBOT["BOT_TOKEN"]
SERVER_IP = TGBOT["SERVER_IP"]
PORT = TGBOT["TELEGRAM_PORT"]
CERT_FILE = TGBOT["CERT_FILE"]
KEY_FILE = TGBOT["KEY_FILE"]
WEBHOOK_URL = TGBOT["BOT_WEBHOOK_URL"]

# States
CHOOSING, TYPING_REPLY = range(2)

# Enable logging
if DEBUG:
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Manager(object):
    def __init__(self, token):
        self.logger = logging.getLogger(
            "ht.telegram.bot." + self.__class__.__name__)
        self.token = token

        self.bot = Bot(token)

        self.updater = Updater(bot=self.bot)
        self.dispatcher = self.updater.dispatcher

        self.build_query = BuildQuery()
        self._setup_commands()

        # Custom keyboard with reply options
        self.reply_keyboard = [["Clinical Officer", "Doctor", "Nurse"],
                               ["NHIF Accredited Hospital: Inpatient",
                                "NHIF Accredited Hospital: Outpatient"],
                               ["Health Facility"]]

        self.markup = ReplyKeyboardMarkup(
            self.reply_keyboard, one_time_keyboard=True)

    def start_polling(self):
        """
        Activates schedulers of all setups, and starts polling updates from Telegram.
        """
        # self.logger.debug('Start polling')
        self.logger.info('Start polling')

        # Delete any webhook
        self.updater.bot.set_webhook()

        self.updater.start_polling(poll_interval=1.0, timeout=20)
        self.updater.idle()

    def start_webhook(self, webhook_url, listen, port, url_path, cert=None, key=None):
        """
        Activates schedulers of all setups, setups webhook, and
        starts small http server to listen for updates via this webhook.
        """
        # self.logger.debug('Start webhook')
        self.logger.info('Start webhook')

        # Delete any webhook to avoid Conflict: terminated by other setWebhook
        self.updater.bot.set_webhook()
        self.updater.start_webhook(listen=listen, port=port,
                                   url_path=url_path, cert=cert, key=key,
                                   webhook_url=webhook_url)

        time.sleep(5)  # to avoid error 4RetryAfter: Flood control exceeded
        self.updater.bot.set_webhook(url=webhook_url)

        print ("\nWebhook set: %s \n", self.bot.getWebhookInfo().url)
        self.updater.idle()

    def setup(self):
        if DEBUG:
            self.start_polling()
        else:
            self.start_webhook(
                webhook_url=WEBHOOK_URL,
                listen=SERVER_IP,
                port=int(PORT),
                url_path=self.token,
                cert=CERT_FILE,
                key=KEY_FILE
            )

    def _setup_commands(self):
        self.dispatcher.add_handler(CommandHandler('help', self.help))
        # Add conversation handler with the states
        self.dispatcher.add_handler(ConversationHandler(
            # Handler object to trigger the start of the conversation
            entry_points=[CommandHandler('start', self.start)],

            # Conversation states
            states={
                CHOOSING: [RegexHandler('^(Clinical Officer|Doctor|Nurse|Health Facility|NHIF Accredited Hospital)',
                                        self.regular_choice,
                                        pass_user_data=True),
                           ],

                TYPING_REPLY: [MessageHandler(Filters.text,
                                              self.received_information,
                                              pass_user_data=True),
                               ],

            },

            fallbacks=[CommandHandler('cancel', self.cancel)],

            # Allow user can restart a conversation with an entry point
            allow_reentry=True
        ))

        # self.dispatcher.add_handler(conv_handler)
        self.dispatcher.add_handler(
            MessageHandler(Filters.command, self.unknown))
        self.dispatcher.add_error_handler(self.error)

    def facts_to_str(self, user_data):
        facts = list()

        for key, value in user_data.items():
            facts.append("%s - %s" % (key, value))

        return "\n".join(facts).join(["\n", "\n"])

    def start(self, bot, update):

        chat_id = update.message.chat_id
        user = update.message.from_user.first_name

        # self.logger.debug('Conversation started by % s' % user)
        self.logger.info('Conversation started by % s' % user)

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
            reply_markup=self.markup,
        )

        # Call the next function
        # return self.CHOOSING
        return CHOOSING

    # TODO: Handle edited_message in these too
    def regular_choice(self, bot, update, user_data):
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
        # return self.TYPING_REPLY
        return TYPING_REPLY

    def received_information(self, bot, update, user_data):
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
                                  % self.facts_to_str(user_data))

        bot.sendChatAction(chat_id=chat_id, action="typing")

        # Now we fetch the data
        results = self.fetch_data(user_data)

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
            reply_markup=self.markup,
        )

        # Empty the user_data dictionary
        user_data.clear()

        # Call functi0n regular_choice
        # return self.CHOOSING
        return CHOOSING

    def fetch_data(self, user_data):
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

        search_results = self.build_query.build_query_response(query)
        return search_results

    def cancel(self, bot, update):
        user = update.message.from_user
        self.logger.info("User %s canceled the conversation." %
                         user.first_name)
        update.message.reply_text("Catch you later %s! Hope to talk to you soon" % user.first_name,
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def help(self, bot, update):
        update.message.reply_text("I am here to help you")

    def unknown(self, bot, update):
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Sorry, I didn't understand that command.")

    def error(self, bot, update, error):
        self.logger.warning("Update % s caused error % s" % (update, error))


manager = Manager(TOKEN)
manager.setup()
