import youtube_dl
import os


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'worstaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '80',
    },
    {
            'key': 'FFmpegMetadata'
    }
    ],
    'progress_hooks': [my_hook],
    'outtmpl': '/app/audio-file/file.%(ext)s',
    'nocheckcertificate': True
}


def download(URL):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
