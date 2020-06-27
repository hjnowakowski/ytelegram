import os

AUDIO_FILES_PATH = os.getenv("FILES_PATH")
MODE = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

if os.getenv("PORT") is not None:
    HEROKU_PORT = int(os.getenv("PORT"))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")

HEROKU_WEBHOOK_URL = "https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN)

DELETE_FILE_ROTATION_ENABLED = False
DELETE_FILE_ROTATION_TIME = 10

SEND_AUDIO_FILE_TIMEOUT = 512
ALLOWED_TELEGRAM_USER_IDS = [int(user_id) for user_id in os.getenv("ALLOWED_TELEGRAM_USERS").split(' ')]

YDL_AUDIO_CONFIG = {
    'format': 'bestaudio[abr<=80]',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '80',
    }, {
        'key': 'FFmpegMetadata'
    }],
    'nocheckcertificate': True,
    'updatetime': False
}

YDL_METADATA_CONFIG = {
    'nocheckcertificate': True,
    'skip_download': True
}

# BOT'S MESSAGES

USER_NOT_ALLOWED_MSG = 'Your user is not allowed to use this bot.'
NOT_URL_MSG = 'Hello user!\nThe message you provided is not a URL, please correct it.'
START_DOWNLOADING_CONFIRMATION_MSG = 'Hi! We are downloading {}\n Please be patient, downloading longer videos (' \
                                     '~1.5h) might take up to few minutes.'
END_DOWNLOADING_CONFIRMATION_MSG = 'Done downloading, I\'m sending it to you!'
