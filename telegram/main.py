
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler,
    filters, ContextTypes
)

TOKEN = "8763599176:AAGFh0nsCc6TptLmA9sSOkqEPRsBAIFzIKg"



#sessions
user_states = {}
logged_in_users = set()

# mernu
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Register", callback_data="register")],
        [InlineKeyboardButton("Login", callback_data="login")],
        [InlineKeyboardButton("Generate API", callback_data="api")]
    ])

# start 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выберите действие:", reply_markup=menu())

# buttons
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "register":
        user_states[user_id] = "reg_username"
        await query.message.reply_text("Введите username:")

    elif query.data == "login":
        user_states[user_id] = "login_username"
        await query.message.reply_text("Введите username:")

    elif query.data == "api":
        if user_id not in logged_in_users:
            await query.message.reply_text("Сначала войдите!")
            return

# text
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    state = user_states.get(user_id)

    # register
    if state == "reg_username":
        user_states[user_id] = ("reg_email", text)
        await update.message.reply_text("Введите email:")

    elif isinstance(state, tuple) and state[0] == "reg_email":
        user_states[user_id] = ("reg_password", state[1], text)
        await update.message.reply_text("Введите пароль:")

    elif isinstance(state, tuple) and state[0] == "reg_password":
        username = state[1]
        email = state[2]
        password = text.encode()


        try:

            await update.message.reply_text("Регистрация успешна ✅")
        except Exception as e:
            await update.message.reply_text("Ошибка: пользователь уже существует")

        user_states[user_id] = None

    # login
    elif state == "login_username":
        user_states[user_id] = ("login_password", text)
        await update.message.reply_text("Введите пароль:")

    elif isinstance(state, tuple) and state[0] == "login_password":
        username = state[1]
        password = text.encode()

        user_states[user_id] = None


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()