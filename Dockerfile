FROM python:3.7

ADD . /app
WORKDIR /app

RUN pip3 install pipenv

RUN pipenv lock  \
 && apt-get update \
 && mkdir "/app/audio-file" \
 && apt-get --assume-yes install ffmpeg \
 && pipenv install --dev --ignore-pipfile --system --deploy

CMD ["python3", "app.py"]
