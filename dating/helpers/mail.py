import time
from django.core.mail import send_mail
from ..helpers import jwt_encode


sendcount = 0


def send_verify_email(user):
    '''
    Send verification email

    **Parameters**

        user: *dating.models.User.User*
            The user

    '''
    global sendcount
    sendcount += 1
    # restrict sendcount within 20 to prevent attacks
    # (this site is just for testing)
    if sendcount > 20:
        return

    link = "http://3.80.189.46/verify_email?token=%s" % (
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

    send_mail(
        "Verify email",
        text,
        'wanyang8610@gmail.com',
        [user.email],
        html_message=html,
        fail_silently=False,
    )
