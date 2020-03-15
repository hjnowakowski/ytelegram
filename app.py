from __future__ import unicode_literals

import logging
import os
import sys
import validators
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from downloader import download_audio_to_file, download_metadata_to_file, get_metadata_from_file

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()

mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

allowedUserIds = [
    643375696,
    464401808
]

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

    if update.effective_chat['id'] not in allowedUserIds:
        update.message.reply_text('Your user is not allowed to use this bot.')
        return

    if os.path.isfile('/app/audio-file/file.mp3'):
        metadata = get_metadata_from_file()
        context.bot.send_audio(title=metadata['title'],
                               performer=metadata['uploader'],
                               duration=metadata['duration'],
                               chat_id=update.effective_chat.id,
                               audio=open('/app/audio-file/file.mp3', 'rb'),
                               timeout=512)
    else:
        update.message.reply_text('You first need to provide a valid URL so i can download_audio_to_file a file\n'
                                  'Just send me a URL and after downloading it I can send it to you!')


def default_handler(update: Update, context: CallbackContext):

    if update.effective_chat['id'] not in allowedUserIds:
        update.message.reply_text('Your user is not allowed to use this bot.')
        return

    URL = update.effective_message.text
    if validators.url(URL):
        update.message.reply_text('Oh User! It\'s a url!\nIm downloading it, give me few minutes')
        download_audio_to_file(URL)
        download_metadata_to_file(URL)
        metadata = get_metadata_from_file()
        update.message.reply_text('Done downloading, Ill send it to you!\nThis might take a while...')
        context.bot.send_audio(title=metadata['title'],
                               performer=metadata['uploader'],
                               duration=metadata['duration'],
                               chat_id=update.effective_chat.id,
                               audio=open('/app/audio-file/file.mp3', 'rb'),
                               timeout=512)
    else:
        update.message.reply_text('Hello user!')


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("download", download_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, default_handler))

    run(updater)
