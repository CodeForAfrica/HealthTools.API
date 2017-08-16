import logging
import os
import re
import requests
import string

from telegram import Bot, ReplyKeyboardMarkup, ParseMode, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, ConversationHandler, Filters,
                          MessageHandler, RegexHandler)

from healthtools_ke_api.views.build_query import BuildQuery
from healthtools_ke_api.settings import DEBUG


class Manager(object):
    def __init__(self, token):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.bot = Bot(token)
        self.updater = Updater(bot=self.bot)
        self.dispatcher = self.updater.dispatcher
        self.build_query = BuildQuery()
        self._setup_commands()

        self.state = {}

        # States
        self.CHOOSING, self.TYPING_REPLY = range(2)

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
        self.logger.debug('Start polling...')
        for setup in self.setups.values():
            setup.start()
        self.updater.start_polling()
        self.updater.idle()

    def start_webhook(self, webhook_url, listen, port, url_path):
        """
        Activates schedulers of all setups, setups webhook, and
        starts small http server to listen for updates via this webhook.
        """
        self.logger.debug('Start webhook...')
        for setup in self.setups.values():
            setup.start()
        self.updater.start_webhook(listen=listen, port=port, url_path=url_path)
        self.updater.bot.set_webhook(webhook_url)
        self.updater.idle()

    def _setup_commands(self):
        self.dispatcher.add_handler(CommandHandler('help', self.help))
        # Add conversation handler with the states
        conv_handler = ConversationHandler(
            # Handler object to trigger the start of the conversation
            entry_points=[CommandHandler('start', self.start)],

            # Conversation states
            states={
                self.CHOOSING: [RegexHandler('^(Clinical Officer|Doctor|Nurse|Health Facility|NHIF Accredited Hospital)',
                                             self.regular_choice,
                                             pass_user_data=True),
                                ],

                self.TYPING_REPLY: [MessageHandler(Filters.text,
                                                   self.received_information,
                                                   pass_user_data=True),
                                    ],

            },

            fallbacks=[CommandHandler('cancel', self.cancel)],

            # Allow user can restart a conversation with an entry point
            allow_reentry=True
        )
        self.dispatcher.add_handler(
            CallbackQueryHandler(self.command_accept_choice))
        self.dispatcher.add_handler(
            MessageHandler(Filters.command, self.unknown))
        self.dispatcher.add_error_handler(self.error)
        self.dispatcher.add_handler(conv_handler)

    def facts_to_str(self, user_data):
        facts = list()

        for key, value in user_data.items():
            facts.append("%s - %s" % (key, value))

        return "\n".join(facts).join(["\n", "\n"])

    def start(self, bot, update):
        self.logger.debug('Bot started.......')
        # id = update.message.from_user.id
        chat_id = update.message.chat_id
        user = update.message.from_user.first_name

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
        return self.CHOOSING

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
        return self.TYPING_REPLY

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
                                  % facts_to_str(user_data))

        bot.sendChatAction(chat_id=chat_id, action="typing")

        # Now we fetch the data
        results = fetch_data(user_data)

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

        return self.CHOOSING

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
        logger.info("User %s canceled the conversation." % user.first_name)
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
        logger.warning("Update % s caused error % s" % (update, error))


manager = Manager(os.getenv('BOT_TOKEN'))
