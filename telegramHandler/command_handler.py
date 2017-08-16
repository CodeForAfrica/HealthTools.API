import logging
import sys
import os

from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from telegramHandler.handler import (error, help, start,
                                     regular_choice, received_information,
                                     cancel)

TOKEN = os.getenv("BOT_TOKEN")

dispatcher = None
bot = Bot(TOKEN)


def setup():
    '''Telegram Bot dispatcher setup'''

    global dispatcher
    dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

    conv_handler = ConversationHandler(
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
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(CommandHandler("help", help))

    # TO DO: Add settings
    # dispatcher.add_handler(CommandHandler("settings", settings))

    # log all errors
    dispatcher.add_error_handler(error)

    return dispatcher


def webhook(update):
    global dispatcher
    # Manually get updates and pass to dispatcher
    dispatcher.process_update(update)
