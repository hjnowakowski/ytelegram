<h1 align="center">ytelegram</h1>

<p>
  <img src="https://img.shields.io/badge/version-0.9-blue.svg?cacheSeconds=2592000" />
  <a href="https://twitter.com/hjnowakowski">
    <img alt="Twitter: hjnowakowski" src="https://img.shields.io/twitter/follow/hjnowakowski.svg?style=social" target="_blank" />
  </a>
</p>

## Description
<div align="center"> 
<img src="readme-assets/ytelegram-demo.gif">
</div>


Projec


## How it works




## Features per version

1.0 (currently 0.9):
- 

limitations: 
- 




## Deployment

### Heroku

`heroku container:push web --app <app-name>`

`heroku container:release web --app <app-name>`

`heroku logs -t --app <app-name>`

### locally via Docker 


`docker rm ytelegram`

`docker image build -t ytelegram:2.0 .`

`docker run --env-file .env ytelegram:2.0`


## Q&A (about decisions made threw out the development process)

- why download json metadata separately instead of relying on 
        `{
            'key': 'FFmpegMetadata'
        }`
- why preferred quality is set to 80 

`'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '80',
    },`

- why not use s3 for keeping files 

- why only one user can use it 

- how i limited the users that can use the service (+ how to check for user id)

- why i dont support video 

- why I choose heroku 


## Author

👤 **Henryk Nowakowski**

* Twitter: [@hjnowakowski](https://twitter.com/hjnowakowski)
* Github: [@hjnowakowski](https://github.com/hjnowakowski)


