#!/usr/bin/env bash

apt-get update
apt-get install -y python mercurial python-pip python-dev python-imaging g++

apt-get install -y virtualbox-guest-additions 

cd /vagrant/weatherapp
python setup.py develop
