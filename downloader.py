import youtube_dl
import json

ydl_audio = {
    'format': 'worstaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '80',
    }, {
        'key': 'FFmpegMetadata'
    }],
    'outtmpl': '/app/audio-file/file.%(ext)s',
    'nocheckcertificate': True
}


async def download_audio_to_file(URL):
    with youtube_dl.YoutubeDL(ydl_audio) as ydl:
        ydl.download([URL])


ydl_metadata = {
    'skip_download': True,
    'writeinfojson': True,
    'outtmpl': '/app/audio-file/metadata.%(ext)s',
    'nocheckcertificate': True
}


async def download_metadata_to_file(URL):
    with youtube_dl.YoutubeDL(ydl_metadata) as ydl:
        print(ydl.download([URL]))


def get_metadata_from_file():
    with open('/app/audio-file/metadata.info.json', 'r') as json_file:
        return json.load(json_file)
