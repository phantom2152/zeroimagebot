from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import telegram
import os
try:
    from PIL import Image
except ImportError:
    import image
import pytesseract

# created by @im_raveen
# ocr_bot
# new_updates_soon

TOKEN = os.getenv("BOT_TOKEN")
APP_NAME = os.getenv("APP_NAME")

def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! welcome to the product of @thezerobots', )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(''' /start to start the bot 
                              
                              /donate to donate the creator
                               
                              after uploading your image reply image with 
                             
                             /img_to_txt to retrive information from given image
                             
                             /report to report problem of bot to owner
                             
                             /creator to know the creator
                             
                             /source_code to get the source code
                             
                             
                             
                              ''')


def hi(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text('hi bro')


filename = "pic.png"


def image_coversion(update, context):
    # file_id = update.message.photo[-1].file_id
    # newFile = context.bot.get_file(file_id)
    # newFile.download(filename)
    update.message.reply_text(
        'recived your image ! processing ... reply image with /img_to_txt to retrive image ')


def text(update, context):
    """Send a message when the command /img_to_txt is issued. """
    id = update.message.chat_id
    context.bot.get_file(update.message.reply_to_message.photo[-1]).download(
        custom_path=f"img/{id}.jpg")
    pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"
    string = (pytesseract.image_to_string(
        Image.open(f"img/{id}.jpg")))
    try:
        update.message.reply_text(string)
    except Exception:
        update.message.reply_text("Unable to retrive image")


def report(update, context):
    update.message.reply_text(''' Found a problem in bot ?
                              report it in @thezerobots
                              ''')


def creator(update, context):
    update.message.reply_text('creator - @im_raveen')


def donate(update, context):
    keyboard = [
        [
            telegram.InlineKeyboardButton("Contribute",
                                          url="https://github.com/raveen-2003"),
            telegram.InlineKeyboardButton(
                "upi", url="https://upayi.me/selvirajesh76@okhdfcbank/15"),
        ],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Thank you for comming forward ! , your donations makes our bot Alive and encourages us to give more updates in near future", reply_markup=reply_markup)


def source_code(update, context):
    keyboard = [
        [
            telegram.InlineKeyboardButton("Source Code",
                                          url="https://github.com/raveen-2003/zeroimagebot"),
        ],
    ]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Source code of @thezeroimagebot is available i github", reply_markup=reply_markup)



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)
    PORT = int(os.environ.get('PORT', '8443'))
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("img_to_txt", text))
    dispatcher.add_handler(CommandHandler("report", report))
    dispatcher.add_handler(CommandHandler("donate", donate))
    dispatcher.add_handler(CommandHandler("source_code", source_code))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, hi))
    dispatcher.add_handler(MessageHandler(Filters.photo, image_coversion))

    # Start the Bot
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN,
                          webhook_url=f"https://{APP_NAME}.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
