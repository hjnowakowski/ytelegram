<h1 align="center">ytelegram</h1>

<p>
  <img src="https://img.shields.io/badge/version-0.9-blue.svg?cacheSeconds=2592000" />
  <a href="https://twitter.com/hjnowakowski">
    <img alt="Twitter: hjnowakowski" src="https://img.shields.io/twitter/follow/hjnowakowski.svg?style=social" target="_blank" />
  </a>
</p>

![Heroku CD](https://github.com/hjnowakowski/ytelegram/workflows/Heroku%20CD/badge.svg)

## Description

<div align="center"> 
<img src="readme-assets/ytelegram-demo.gif">
</div>

The `ytelegram` is a self-hosted project that makes it easy to download youtube videos in audio form directly from the Telegram app. Project uses `python-telegram-bot` to easily access telegram API and `youtube-dl` to download the content from the web. Some features are yet to be done, see Issues section for more information. If you are downloading a lot of content from YouTube, consider doing so by subscribing to their paid plan.

Note that project is not finished and may contain bugs/unfinished features.

## Deployment

Setup required environemnt variables from [config.py](https://github.com/hjnowakowski/ytelegram/blob/master/config.py) and run the following commands:

### Heroku

```bash
heroku container:push web --app <heroku-app-name>
heroku container:release web --app <heroku-app-name>
heroku logs -t --app <heroku-app-name>
```

### locally with Docker 

``` bash
docker rm ytelegram
docker image build -t ytelegram:2.0 .
docker run --env-file .env ytelegram:2.0
```

## Author

👤 **Henryk Nowakowski**

* Twitter: [@hjnowakowski](https://twitter.com/hjnowakowski)
* Github: [@hjnowakowski](https://github.com/hjnowakowski)


