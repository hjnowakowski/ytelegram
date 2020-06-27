import os
import config
import subprocess as sp


def get_audio_file_path(user_id, video_id):
    return "{files_path}/{user_id}/{video_id}.mp3" \
        .format(files_path=config.AUDIO_FILES_PATH, user_id=user_id, video_id=video_id)


def activate_delete_file_rotation():
    cron_job_path = "/etc/cron.d/delete-audio-files-cron"
    delete_files_cron_job = "* * * * * find {} -type f -mmin +{} -exec rm -f -- {{}} \\; \n" \
        .format(config.AUDIO_FILES_PATH, config.DELETE_FILE_ROTATION_TIME)
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


def verify_execution_environment():
    print("Verification")
    # cron
    # FFmpeg
    # files_path exists
