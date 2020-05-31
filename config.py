import os


AUDIO_FILES_PATH = os.getenv("FILES_PATH")
MODE = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

allowedTelegramUserIds = [
    643375696,
    464401808
]

ydl_audio = {
    'format': 'worstaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '80',
    }, {
        'key': 'FFmpegMetadata'
    }],
    'nocheckcertificate': True
}
