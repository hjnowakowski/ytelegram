FROM hjnowakowski/python-ffmpeg:latest

ADD . /app
WORKDIR /app

RUN pipenv lock
RUN pipenv install --dev --ignore-pipfile --system --deploy

RUN apt-get update && apt-get -y install cron

CMD ["python3", "app.py"]
