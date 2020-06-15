import os
import subprocess as sp

AUDIO_FILES_PATH = os.getenv("FILES_PATH")
MODE = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

DELETE_FILE_ROTATION_TIME_MIN = 10

allowedTelegramUserIds = [
    643375696,
    464401808
]

ydl_audio = {
    'format': 'bestaudio/best',
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

# TODO: move this method to utils file
def set_delete_file_rotation_time(minutes):
    cron_job_path = "/etc/cron.d/delete-audio-files-cron"
    delete_files_cron_job = "* * * * * find {} -type f -mmin +{} -exec rm -f -- {{}} \\; \n"\
        .format(AUDIO_FILES_PATH, minutes)
    try:
        with open(cron_job_path, "w") as file:
            file.write(delete_files_cron_job)
    except IOError as exc:
        print(exc)
    os.chmod(cron_job_path, 644)
    # add the new cronjob to crontab
    sp.run(["crontab", cron_job_path])
    # run cron process
    sp.run(["cron"])


# TODO: move to utils
def verify_execution_environment():
    print("Verification")
    # cron
    # FFmpeg
    # files_path exists
