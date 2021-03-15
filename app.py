from __future__ import unicode_literals

import sys
import validators
import config
import asyncio
import utils
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, dispatcher
from downloader import download, get_metadata


def default_handler(update: Update, context: CallbackContext):
    if update.effective_chat['id'] not in config.ALLOWED_TELEGRAM_USER_IDS:
        update.message.reply_text(config.USER_NOT_ALLOWED_MSG)
        return
    url = update.effective_message.text
    if not validators.url(url):
        update.message.reply_text(config.NOT_URL_MSG)
    else:
        metadata = get_metadata(url)
        update.message.reply_text(config.START_DOWNLOADING_CONFIRMATION_MSG.format(str(metadata['title'])))
        asyncio.run(download(url, str(update.effective_chat['id'])))
        update.message.reply_text(config.END_DOWNLOADING_CONFIRMATION_MSG)
        asyncio.run(send_audio(context, update, metadata))


async def send_audio(context, update, metadata):
    context.bot.send_audio(
        title=metadata['title'],
        performer=metadata['uploader'],
        duration=metadata['duration'],
        chat_id=update.effective_chat.id,
        audio=open(utils.get_audio_file_path(str(update.effective_chat['id']), metadata['id']), 'rb'),
        timeout=config.SEND_AUDIO_FILE_TIMEOUT)
    # TODO use logger instead
    print('Sent audio file')


def init_updater(updater):
    if config.DELETE_FILE_ROTATION_ENABLED:
        utils.activate_delete_file_rotation()
    if config.MODE == 'local' or config.MODE == 'local-docker':
        updater.start_polling()
    elif config.MODE == 'heroku':
        updater.start_webhook(listen="0.0.0.0",
                              port=config.HEROKU_PORT,
                              url_path=config.TOKEN)
        updater.bot.set_webhook(config.HEROKU_WEBHOOK_URL)
    else:
        print('No MODE specified!')
        sys.exit(1)


if __name__ == '__main__':
    print('Starting... :)')
    telegram_updater = Updater(config.TOKEN, use_context=True)
    telegram_updater.dispatcher.add_handler(MessageHandler(Filters.text, default_handler, run_async=True))
    init_updater(telegram_updater)
