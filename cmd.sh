#!/bin/bash

apt-get update;
apt-get --assume-yes install apt-utils;
apt-get --assume-yes install ffmpeg;

python3 app.py


