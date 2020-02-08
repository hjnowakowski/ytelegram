from __future__ import unicode_literals

import logging
import os
import random
import sys

from downloader import download

from telegram import Update, InputMediaAudio, InlineQueryResultArticle
from telegram.ext import Updater, CommandHandler, CallbackContext

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()

mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)

def start_handler(update: Update, context: CallbackContext):
    logger.info("User {} started bot".format(update.effective_user["id"]))
    URL = " ".join(context.args)
    logger.info("Argument" + URL)
    # update.message.reply_text("Dobry, podaj proszę URL\nbędymy go potem ściągać\nżeby pobrać wyślij wiadomość o treści /random")
    if(mode == "prod"):
        download(URL)


def download_handler(update: Update, context: CallbackContext):
    number = random.randint(0, 10)
    logger.info("User {} randomed number {}".format(update.effective_user["id"], number))

    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('/app/audio-file/file.mp3', 'rb'))

    # InputMediaAudio('/app/audio-file/FZR0rG3HKIk.mp3', thumb=None, caption=None, parse_mode=None, duration=None, performer=None,
    #                          title='Przykład')

    update.message.reply_text("Random number: {}".format(number))


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("download", download_handler))

    run(updater)

