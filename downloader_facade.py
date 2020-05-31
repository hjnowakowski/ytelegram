import youtube_dl
import config
import os
import copy


async def download(url, user_id):
    # create a copy of the config so threads don't overwrite each data
    local_ydl_audio_config = copy.deepcopy(config.ydl_audio)
    # make sure we have a directory created for a user
    if not os.path.exists(config.AUDIO_FILES_PATH + '/' + user_id):
        os.mkdir(config.AUDIO_FILES_PATH + '/' + user_id)
    # set outtmpl to ydl config
    local_ydl_audio_config['outtmpl'] = config.AUDIO_FILES_PATH + '/' + user_id + '/%(id)s.%(ext)s'
    # perform download
    await download_audio_to_file(url, local_ydl_audio_config)
    print('Done downloading!')


async def download_audio_to_file(url, local_config):
    with youtube_dl.YoutubeDL(local_config) as ydl:
        ydl.download([url])


def get_metadata(url):
    options = {
        'nocheckcertificate': True,
        'skip_download': True
    }
    return youtube_dl.YoutubeDL(options).extract_info(url)


def get_metadata_field(url, field):
    options = {
        'nocheckcertificate': True,
        'skip_download': True
    }
    return youtube_dl.YoutubeDL(options).extract_info(url)[field]
