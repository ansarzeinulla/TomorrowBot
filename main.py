from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your bot.')

app = Application.builder().token('7859858304:AAEa-Cn-DZ1ldYDwes_K0w6fuh847WFcFOs').build()

app.add_handler(CommandHandler('start', start))

app.run_polling()
