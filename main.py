from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text('Hello! I am your bot.')

updater = Updater(token='7859858304:AAEa-Cn-DZ1ldYDwes_K0w6fuh847WFcFOs', use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()