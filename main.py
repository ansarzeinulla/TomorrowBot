import firebase_admin
from firebase_admin import credentials, firestore
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import json
import os
firebase_key = os.getenv('FIREBASE_KEY')
if firebase_key:
    firebase_key = json.loads(firebase_key)
cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)
db = firestore.client()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Who is here", callback_data="show_who_is_here")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hello! I am your bot.", reply_markup=reply_markup)

async def show_who_is_here(update, context):
    users_ref = db.collection('users')
    docs = users_ref.stream()
    docs_list = list(docs)
    num_users = len(docs_list)
    result = ""
    
    for doc in docs_list:
        user = doc.to_dict()
        if user.get('ishere'):
            result += f"👤 {user['nick']} | {user['tgnick']} | {user['name']}\n"

    await update.callback_query.answer()
    if len(result) == 0:
        await update.callback_query.message.reply_text("No users are at Tomorrow School.")
        return
    else:
        for i in range(0, len(result), 4000):
            await update.callback_query.message.reply_text(result[i:i + 4000])



# Main Application
app = Application.builder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(show_who_is_here))

# Run the Bot
app.run_polling()