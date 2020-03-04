import youtube_dl


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'worstaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    },
    {
            'key': 'FFmpegMetadata'
    }
    ],
    'progress_hooks': [my_hook],
    'outtmpl': '/app/audio-file/file.%(ext)s'
}


def download(URL):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
