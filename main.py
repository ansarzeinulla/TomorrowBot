
import firebase_admin
from firebase_admin import credentials, firestore
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Connect to Firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Telegram Bot Token
BOT_TOKEN = "7859858304:AAEa-Cn-DZ1ldYDwes_K0w6fuh847WFcFOs"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Show", callback_data="show")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Hello! I am your bot.", reply_markup=reply_markup)

# Show Data from Firestore
async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = db.collection('users').stream()
    users_data = ""
    
    for doc in query:
        users_data += f"{doc.id}: {doc.to_dict()}\n"
        
    await update.callback_query.message.reply_text(users_data)

# Main Application
app = Application.builder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(show_data))

# Run the Bot
app.run_polling()