## Prerequisites
* MySQL
* python
* Redis

## Python packages
Install `pip  install Django mysqlclient Pillow channels channels_redis`
* Django: 3.1.3
* mysqlclient: 2.0.1
* Pillow: 8.0.1
* channels: 3.0.2
* channels_redis: 3.2.0

## Setup
* Create `dating` database:  `CREATE DATABASE dating CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

## Running
* `python manage.py runserver`

Make sure install PyTorch 1.7
Download detection model `best8519.pt`

