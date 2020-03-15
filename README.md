
# ytelegram, project in development




## How to run Heroku

heroku container:push web --app ytelegram-bot

heroku container:release web --app ytelegram-bot

heroku logs -t --app ytelegram-bot (-n 15000)

## How to run locally on docker 


docker rm ytelegram

docker image build -t ytelegram:2.0 .

