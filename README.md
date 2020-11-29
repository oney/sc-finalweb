## Prerequisites
* MySQL
* python
* Redis

## Python packages
Install `pip  install Django mysqlclient Pillow python-resize-image channels channels_redis torch torchvision`
* Django: 3.1.3
* mysqlclient: 2.0.1
* Pillow: 8.0.1
* python-resize-image: 
* channels: 3.0.2
* channels_redis: 3.2.0
* torch: 1.7.0
* torchvision

## Setup
* Modify `finalweb/settings.py`
```
...
DATABASES = {
    'default': {
        'USER': '<user>',
        'PASSWORD': '<password>',
        ...
}
```
* Create `dating` database:  `CREATE DATABASE dating CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
* Download [PyTorch model](https://drive.google.com/file/d/15lI_gRRgeBRzDtjWBvMMkuQTkm1H3cHB/view?usp=sharing) to `dating/detection/best8519.pt`

## Running
* `python manage.py runserver`


