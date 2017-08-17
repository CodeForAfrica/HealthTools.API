import logging
import os
import re
import requests
import string

from flask import Blueprint, request, current_app

from telegram import ReplyKeyboardMarkup, ParseMode, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, ConversationHandler, Filters,
                          MessageHandler, RegexHandler)

from healthtools_ke_api.views.build_query import BuildQuery
from healthtools_ke_api.settings import DEBUG, TGBOT

from telegram_handler import Manager

bq = BuildQuery()

telegram_bot = Blueprint("telegram_bot", __name__)

# # Enable event logging
# logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#                     level=logging.INFO)

# logger = logging.getLogger('telegram.bot')

# # States
# CHOOSING, TYPING_REPLY = range(2)

# # Custom keyboard with reply options
# reply_keyboard = [["Clinical Officer", "Doctor", "Nurse"],
#                   ["NHIF Accredited Hospital: Inpatient",
#                       "NHIF Accredited Hospital: Outpatient"],
#                   ["Health Facility"]]

# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
#                              resize_keyboard=True)


@telegram_bot.route('/', methods=['GET'])
# @telegram_bot.route('/telegram', methods=['GET'])
def setup_tg():
    
    manager = Manager(TGBOT["BOT_TOKEN"])
    manager.setup()


# def setup():
#     BOT_TOKEN = os.getenv('BOT_TOKEN')
#     updater = Updater(BOT_TOKEN)

#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher

#     # Add conversation handler with the states
#     conv_handler = ConversationHandler(
#         # Handler object to trigger the start of the conversation
#         entry_points=[CommandHandler('start', start)],

#         # Conversation states
#         states={
#             CHOOSING: [RegexHandler('^(Clinical Officer|Doctor|Nurse|Health Facility|NHIF Accredited Hospital)',
#                                     regular_choice,
#                                     pass_user_data=True),
#                        ],

#             TYPING_REPLY: [MessageHandler(Filters.text,
#                                           received_information,
#                                           pass_user_data=True),
#                            ],

#         },

#         fallbacks=[CommandHandler('cancel', cancel)],

#         # Allow user can restart a conversation with an entry point
#         allow_reentry=True
#     )

#     dp.add_handler(conv_handler)
#     dp.add_handler(MessageHandler([Filters.command], unknown))
#     dp.add_handler(CommandHandler("help", help))

#     # TO DO: Add settings
#     # dp.add_handler(CommandHandler("settings", settings))

#     # log all errors
#     dp.add_error_handler(error)

#     # Start the Bot
#     # To avoid the readTimeoutError set timeout
#     updater.start_polling(poll_interval=1.0, timeout=20)
#     # if DEBUG:
#     #     updater.start_polling(poll_interval=1.0, timeout=20)
#     # else:
#     #     updater.start_webhook(listen='127.0.0.1',
#     #                           port=5000, url_path=BOT_TOKEN)
#     #     updater.bot.set_webhook(webhook_url='https://health.the-star.co.ke/%s' % BOT_TOKEN,
#     #                             # certificate=open('cert.pem', 'rb')
#     #                             )

#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()


# def facts_to_str(user_data):
#     facts = list()

#     for key, value in user_data.items():
#         facts.append("%s - %s" % (key, value))

#     return "\n".join(facts).join(["\n", "\n"])


# def start(bot, update):
#     # id = update.message.from_user.id
#     chat_id = update.message.chat_id
#     user = update.message.from_user.first_name

#     logger.info("User %s started the conversation." % user.capitalize())

#     welcome_msg = (
#         "*Hello* %s.\n"
#         "My name is `Healthtools Bot`.\n\n"
#         "*Here's what I can do for you:*\n"
#         "1. Check to see if your doctor, nurse, or clinical officer is registered\n"
#         "2. Find out which facilities your NHIF card will cover in your county\n"
#         "3. Find the nearest doctor or health facility\n"  # Description of the app
#         "\nSend /cancel to stop talking to me.\n" % user
#     )

#     bot.send_message(
#         chat_id=chat_id,
#         text=welcome_msg,
#         parse_mode=ParseMode.MARKDOWN,
#         reply_markup=markup,
#     )

#     # Call the next function
#     return CHOOSING


# def regular_choice(bot, update, user_data):
#     """
#     Show summary of user choice and input
#     """
#     chat_id = update.message.chat_id

#     text = update.message.text
#     user_data['choice'] = text

#     msg = "Please enter the name of a `%s` you want to find" % text.title()

#     bot.send_message(
#         chat_id=chat_id,
#         text=msg,
#         parse_mode=ParseMode.MARKDOWN,
#     )

#     # Call next function: received_information
#     return TYPING_REPLY


# def received_information(bot, update, user_data):
#     """
#     Show summary of user choice and input
#     """
#     chat_id = update.message.chat_id

#     text = update.message.text
#     choice = user_data['choice']
#     user_data[choice] = text
#     del user_data['choice']

#     update.message.reply_text("Here's what you have asked me to search"
#                               "%s"
#                               % facts_to_str(user_data))

#     bot.sendChatAction(chat_id=chat_id, action="typing")

#     # Now we fetch the data
#     results = fetch_data(user_data)

#     # Remove multiple whitespaces
#     results = re.sub(" +", " ", str(results[0]))
#     search_msg = (
#         "*Search Results*\n"
#         "%s" % results
#     )

#     bot.send_message(
#         chat_id=chat_id,
#         text=search_msg,
#         parse_mode=ParseMode.MARKDOWN,
#         reply_markup=markup,
#     )

#     # Empty the user_data dictionary
#     user_data.clear()

#     return CHOOSING


# def fetch_data(user_data):
#     """
#     Fetch the data requested by the user
#     """

#     # TO DO: How many results to fetch
#     # If many, pagination
#     # Use InlineQueryHandler

#     query = user_data.keys()[-1]

#     if query:
#         keyword = str(query).encode("utf-8")
#         search_term = user_data[keyword]

#         if re.search("NHIF Accredited Hospital", keyword):
#             keyword = re.sub("accredited hospital: ", "",
#                              keyword, flags=re.IGNORECASE)

#         if keyword == "Health Facility":
#             keyword = "hf"

#         keyword = keyword.lower()
#         query = keyword + " " + search_term

#     else:
#         return "Keyword not valid"

#     search_results = bq.build_query_response(query)
#     return search_results


# def cancel(bot, update):
#     user = update.message.from_user
#     logger.info("User %s canceled the conversation." % user.first_name)
#     update.message.reply_text("Catch you later %s! Hope to talk to you soon" % user.first_name,
#                               reply_markup=ReplyKeyboardRemove())

#     return ConversationHandler.END


# def help(bot, update):
#     update.message.reply_text("I am here to help you")


# def unknown(bot, update):
#     bot.sendMessage(
#         chat_id=update.message.chat_id,
#         text="Sorry, I didn't understand that command.")


# def error(bot, update, error):
#     logger.warning("Update % s caused error % s" % (update, error))


# # def main():
# #     # Create the Updater and pass it your bot's token.
# #     TOKEN = current_app.config.get('BOT_TOKEN'),
# #     updater = Updater(TOKEN)

# #     # Get the dispatcher to register handlers
# #     dp = updater.dispatcher

# #     # Add conversation handler with the states
# #     conv_handler = ConversationHandler(
# #         # Handler object to trigger the start of the conversation
# #         entry_points=[CommandHandler('start', start)],

# #         # Conversation states
# #         states={
# #             CHOOSING: [RegexHandler('^(Clinical Officer|Doctor|Nurse|Health Facility|NHIF Accredited Hospital)',
# #                                     regular_choice,
# #                                     pass_user_data=True),
# #                        ],

# #             TYPING_REPLY: [MessageHandler(Filters.text,
# #                                           received_information,
# #                                           pass_user_data=True),
# #                            ],

# #         },

# #         fallbacks=[CommandHandler('cancel', cancel)],

# #         # Allow user can restart a conversation with an entry point
# #         allow_reentry=True
# #     )

# #     dp.add_handler(conv_handler)
# #     dp.add_handler(MessageHandler([Filters.command], unknown))
# #     dp.add_handler(CommandHandler("help", help))

# #     # TO DO: Add settings
# #     # dp.add_handler(CommandHandler("settings", settings))

# #     # log all errors
# #     dp.add_error_handler(error)

# #     # Start the Bot
# #     # To avoid the readTimeoutError set timeout
# #     if DEBUG:
# #         updater.start_polling(poll_interval=1.0, timeout=20)
# #     else:
# #         pass
# #         # updater.start_webhook(listen="0.0.0.0", port=HEROKU_PORT, url_path=BOT_TOKEN,
# #         #                       webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{BOT_TOKEN}")

# #     # Run the bot until you press Ctrl-C or the process receives SIGINT,
# #     # SIGTERM or SIGABRT. This should be used most of the time, since
# #     # start_polling() is non-blocking and will stop the bot gracefully.
# #     updater.idle()


# # if __name__ == '__main__':
# #     main()
