FROM python:3.7

ADD . /app
WORKDIR /app

RUN pip3 install pipenv

RUN pipenv lock  \
 && mkdir "/app/audio-file" \
 && pipenv install --dev --ignore-pipfile --system --deploy

CMD ["bash", "/app/cmd.sh"]
