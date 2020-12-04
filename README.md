# Project
The project is a dating website which implements the following features:
* Register/login with email verification
* Real-time websocket text chatrooms
* Machine learning-based inappropriate image removal detection

## Demo website
http://3.80.189.46/

## Prerequisites
* Python 3
* MySQL
* Redis

## Python packages
Install `pip  install Django mysqlclient Pillow python-resize-image channels channels_redis torch torchvision`
* Django: 3.1.3
* mysqlclient: 2.0.1
* Pillow: 8.0.1
* python-resize-image
* channels: 3.0.2
* channels_redis: 3.2.0
* torch: 1.7.0
* torchvision

## Setup
* Modify `finalweb/settings.py`
```python
# ...
DATABASES = {
    'default': {
        'USER': '<user>',
        'PASSWORD': '<password>',
        # ...
}
# ...
EMAIL_HOST_USER = '<gmail>'
EMAIL_HOST_PASSWORD = '<password>'
DEFAULT_FROM_EMAIL = '<gmail>'
```
* Create `dating` database:  `CREATE DATABASE dating CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
* Run migrations: `python manage.py migrate`
* Download [PyTorch model](https://drive.google.com/file/d/15lI_gRRgeBRzDtjWBvMMkuQTkm1H3cHB/view?usp=sharing) to `dating/detection/best.pt`. The model was trained [here](https://colab.research.google.com/drive/1iBQ9F7YlLBoWaNjH7tkpPIyHbZyRRMTD?usp=sharing).
* Start Redis server

## Running
* `python manage.py runserver`

## Unit tests
`./manage.py test` to run the test in `dating/tests.py`

## Error handling
* The website properly handles user errors such as wrong inputs by showing information on web pages.
* It doesn't consider developer errors like wrong setup or deployment.

## Citations
* [AlexNet](https://colab.research.google.com/github/bentrevett/pytorch-image-classification/blob/master/3_alexnet.ipynb)
* [Django register/login](https://www.cnblogs.com/derek1184405959/p/8567522.html)
* [Django real-time messaging](https://zhuanlan.zhihu.com/p/91642958)
