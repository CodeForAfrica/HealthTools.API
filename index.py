from telegramHandler.manager import Manager, PORT, TOKEN, DEBUG

TOKEN = "420681993:AAHFFe65ocfB_OuoPlSqsk4LK_LcRMK0OLs"
def main():
    manager = Manager(TOKEN)

    if DEBUG:
        manager.start_polling()
    else:
        manager.start_webhook(listen="0.0.0.0", port=5000, url_path=TOKEN,
                              webhook_url="https://htapi-test.herokuapp.com/{}".format(TOKEN))


if __name__ == '__main__':
    main()