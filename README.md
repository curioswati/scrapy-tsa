# scrapy-tsa
Twitter sentiment analysis for Scrapy Project

## Introduction

The project aims to analyse twitter data for Scrapy tag and provide insights and visualizations.


## Installation

### create localsettings from sample and edit accordingly
$ cp scrapy-tsa/settings/sample_local.py scrapy-tsa/settings/local.py


### create postgres db
$ createdb -Upostgres scrapy-tsa

### how to run app
$ export DJANGO_SETTINGS_MODULE="scrapy-tsa.settings.local"
$ python manage.py runserver
