from __future__ import unicode_literals

import os
import sys
import validators
# TODO: try to beautify imports
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, dispatcher
from downloader import download, get_metadata
import config
import asyncio


@dispatcher.run_async
def default_handler(update: Update, context: CallbackContext):
    # TODO: move hardcoded text to config.py
    if update.effective_chat['id'] not in config.allowedTelegramUserIds:
        update.message.reply_text('Your user is not allowed to use this bot.')
        return
    url = update.effective_message.text
    if not validators.url(url):
        update.message.reply_text('Hello user!\nThe message you provided is not a URL, please correct it.')
    else:
        metadata = get_metadata(url)
        update.message.reply_text('Hi! We are downloading ' + str(metadata['title']) +
                                  '\nPlease be patient,  downloading longer videos (~1.5h) might take up to few minutes')
        asyncio.run(download(url, str(update.effective_chat['id'])))
        update.message.reply_text('Done downloading, I\'m are sending it to you!')
        asyncio.run(send_audio(context, update, metadata))


async def send_audio(context, update, metadata):
    # TODO: remove redundant variable here
    var = context.bot.send_audio(title=metadata['title'],
                                 performer=metadata['uploader'],
                                 duration=metadata['duration'],
                                 chat_id=update.effective_chat.id,
                                 audio=open(
                                     config.AUDIO_FILES_PATH + '/' + str(update.effective_chat['id']) +
                                     "/" + metadata['id'] + ".mp3",
                                     'rb'),
                                 timeout=512)
    # TODO use logger instead
    print('Sent audio:\n', var, '\n     ---')


def init_updater(updater):
    # TODO: run this line if only on prod env
    # config.set_delete_file_rotation_time(config.DELETE_FILE_ROTATION_TIME_MIN)

    # TODO: Rename MODES
    if config.MODE == 'dev':
        updater.start_polling()
    elif config.MODE == 'prod':
        # TODO: move config to config
        port = int(os.environ.get("PORT", "8443"))
        heroku_app_name = os.environ.get("HEROKU_APP_NAME")
        # TODO: move hardcoded values to config
        updater.start_webhook(listen="0.0.0.0",
                              port=port,
                              url_path=config.TOKEN)
        # TODO: move url String to config
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(heroku_app_name, config.TOKEN))
    else:
        print('No MODE specified!')
        sys.exit(1)


if __name__ == '__main__':
    print('Starting...')
    telegram_updater = Updater(config.TOKEN, use_context=True)
    telegram_updater.dispatcher.add_handler(MessageHandler(Filters.text, default_handler))
    init_updater(telegram_updater)
