from __future__ import unicode_literals

import os
import sys
import validators
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, dispatcher
from downloader_facade import download, get_metadata, get_metadata_field
import config
import asyncio


@dispatcher.run_async
def default_handler(update: Update, context: CallbackContext):
    if update.effective_chat['id'] not in config.allowedTelegramUserIds:
        update.message.reply_text('Your user is not allowed to use this bot.')
        return
    url = update.effective_message.text
    if not validators.url(url):
        update.message.reply_text('Hello user!\nThe message you provided is not a URL, please correct it.')
    else:
        asyncio.run(download(url, str(update.effective_chat['id'])))
        metadata = get_metadata(url)
        print(metadata)
        update.message.reply_text('Done downloading, Ill send it to you!\nThis might take a while...')
        asyncio.run(send_audio(context, update, metadata))


async def send_audio(context, update, metadata):
    var = context.bot.send_audio(title=metadata['title'],
                                 performer=metadata['uploader'],
                                 duration=metadata['duration'],
                                 chat_id=update.effective_chat.id,
                                 audio=open(
                                     config.AUDIO_FILES_PATH + '/' + str(update.effective_chat['id']) +
                                     "/" + metadata['id'] + ".mp3",
                                     'rb'),
                                 timeout=512)
    print('Sent audio:\n', var, '\n     ---')


def run_updater(updater):
    if config.MODE == 'dev':
        updater.start_polling()
    elif config.MODE == 'prod':
        port = int(os.environ.get("PORT", "8443"))
        heroku_app_name = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=port,
                              url_path=config.TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(heroku_app_name, config.TOKEN))
    else:
        print('No MODE specified!')
        sys.exit(1)


if __name__ == '__main__':
    print('Starting...')
    telegram_updater = Updater(config.TOKEN, use_context=True)
    telegram_updater.dispatcher.add_handler(MessageHandler(Filters.text, default_handler))
    run_updater(telegram_updater)
