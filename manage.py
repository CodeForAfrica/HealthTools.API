from healthtools_ke_api import app
# from healthtools_ke_api.views.telegram_bot import setWebhook, PORT, CONTEXT

# if __name__ == "__main__":
#     app.run()



if __name__ == '__main__':
    # setWebhook()
 
    app.run(host='0.0.0.0',
            port=50000
            # ssl_context=CONTEXT,
            # debug=False)
