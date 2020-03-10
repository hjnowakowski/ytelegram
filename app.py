from __future__ import unicode_literals

import logging
import os
import random
import sys
import validators

from downloader import download

from telegram import Update, InputMediaAudio, InlineQueryResultArticle
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

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


def download_handler(update: Update, context: CallbackContext):
    if os.path.isfile('/app/audio-file/file.mp3'):
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('/app/audio-file/file.mp3', 'rb'),
                               timeout=512)
    else:
        update.message.reply_text('You first need to provide a valid URL so i can download a file\n'
                                  'Just send me a URL and after downloading it I can send it to you!')


def default_handler(update: Update, context: CallbackContext):
    URL = update.effective_message.text
    if validators.url(URL):
        update.message.reply_text('Oh User! It\'s a url!\nIm downloading it, give me few minutes')
        download(URL)
        update.message.reply_text('Done downloading, Ill send it to you!\nThis might take a while...')
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('/app/audio-file/file.mp3', 'rb'),
                               timeout=512)
    else:
        update.message.reply_text('Hello user!')


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("download", download_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, default_handler))

    run(updater)
