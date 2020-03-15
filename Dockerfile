FROM hjnowakowski/python-ffmpeg:latest

ADD . /app
WORKDIR /app

RUN pipenv lock  \
 && mkdir "/app/audio-file" \
 && pipenv install --dev --ignore-pipfile --system --deploy

CMD ["python3", "app.py"]
