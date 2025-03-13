
import firebase_admin
from firebase_admin import credentials, firestore
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Connect to Firestore
import json
import os

# Load Firebase Key from GitHub Secret
firebase_key = json.loads(os.environ['FIREBASE_KEY'])
cred = credentials.Certificate(firebase_key)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Telegram Bot Token
BOT_TOKEN = "7859858304:AAEa-Cn-DZ1ldYDwes_K0w6fuh847WFcFOs"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Show", callback_data="show")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hello! I am your bot.", reply_markup=reply_markup)

async def show_data(update, context):
    users_ref = db.collection('users')  # Firebase /users reference
    docs = users_ref.stream()

    result = ""
    
    for doc in docs:
        user = doc.to_dict()
        if user.get('is_here'):
            result += f"👤 {user['nick']} | {user['tgnick']} | {user['name']}\n"

    # ✅ Answer the callback first to stop the "Loading..."
    await update.callback_query.answer()

    # ✅ Then send data in smaller messages
    for i in range(0, len(result), 4000):
        await update.callback_query.message.reply_text(result[i:i + 4000])

        
# Main Application
app = Application.builder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(show_data))

# Run the Bot
app.run_polling()
