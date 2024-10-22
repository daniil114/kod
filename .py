import logging
import shelve
from gc import callbacks

from pyexpat.errors import messages
from select import select
from telegram import ForceReply, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext,
                          CallbackQueryHandler)
from enum import Enum
from api import gpt, image
from config import BOT_KEY1

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)



class ModelEnum(Enum):
    gpt_text = 1
    gpt_image = 2


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_id = user.id
    user_name = user.full_name
    pandora = shelve.open("pandora")
    if str(user_id) not in pandora.keys():
        user_data = {
            "user_name": user_name,
            "subs": "Free",
            "tokens": 20,
            "model": ModelEnum.gpt_text.value

        }
     pandora[str(user_id)] = user_data
    await update.message.reply_text(f"Ты можешь писать мне, и я отвечу. Пиши уже!!! {pandora[str(user_id)]["user_name"]}")
    pandora.close()

async  def profile(update: Update) -> None:
    user = update.effective_user
    user_id = str(user.id)
    pandora = shelve.open("pandora")
    subscription_type = pandora[str(user_id)]["subs"]
    tokens = pandora[str(user_id)]["tokens"]
    gpt_model = pandora[user_id]["model"]
    name = pandora[str(user_id)]["user_name"]
    profile_text = ()
    if tokens > 0:
        if gpt_model == ModelEnum.gpt_text.value:
            message = update.message.text
            answer = gpt(message)
            await update.message.reply_text(answer)
        if gpt_model == ModelEnum.gpt_text.value:
            message = update.message.text
            answer = image(message)
            await update.message.reply_photo(
                photo=answer[0],
                caption=answer[1]
            )
    else:
        mess = "Пополните баланс токенов в /store"
        await update.message.reply_text(mess)


    new_keyboard = [
        [InlineKeyboardButton("GPT 3.5", callback_data="1")],
        [InlineKeyboardButton("Stable Diffusion", callback_data="2")]
    ]

for row in new_keyboard:
    for button in row
        if button.callback_data == selected_option:
            new_button = InlineKeyboardButton(f"🐔 {button.text}"), callback_data=button.callback_data)
            row[row.index(button)] = new_button




async def mode(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("GPT 3.5", callback_data="1")],
        [InlineKeyboardButton("Stable Diffusion", callback_data="2")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Тут вы можете сменить модель нейросетей", reply_markup=reply_markup)




async def button(update: Update, context: CallbackContext):
    pandora = shelve.open("pandora")
    query = update.callback_query
    mode_gpt = query.data
    user_id_chat = str(query.from_user.id)
    user_model = pandora[user_id_chat]
    user_model["model"] = int(mode_gpt)
    pandora[user_id_chat] = user_model
    selected_option = query.data
    pandora.close()









async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        f"Это ваш профиль. 🫠\n"
        f"ID: {user_id}\n"
        f"Подписка: {subscription_type}\n\n"
        f"Лимиты: {tokens} token"
        "Чтобы начать, пиши /start \n"
        "За помощью пиши /help \n"
    )
    """Send a message when the command /help is issued."""
    await update.message.reply_text(help_text)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    """Echo the user message."""
    await update.message.reply_text(message)




def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7124893931:AAGJnzsnzQrIuTC6duAa3r9JSlpi2gjncZI").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
