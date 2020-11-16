import time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .. import models
from ..jwthelper import jwt_encode
from ..mailhelper import sendmail


def send_verify_email(user):
    link = "http://127.0.0.1:8000/verify_email?token=%s" % (
        jwt_encode({
            "user_id": user.id,
            "exp": int(time.time() + 60*60*24*60)
        })
    )
    text = "Verify your email by opening %s" % link
    html = """\
    <html>
    <head></head>
    <body>
        Verify your email by opening <a href="%s">this link</a>
    </body>
    </html>
    """ % link
    sendmail(user.email, "Verify email", text, html)
