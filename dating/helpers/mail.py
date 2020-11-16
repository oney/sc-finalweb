
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


sendcount = 0

def sendmail(receiver, subject, text, html):
    global sendcount
    sendcount += 1
    if sendcount > 20:
        return
    # https://stackoverflow.com/a/48755417/2790103 turn on Less secure app access
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    sender = "wanyang8610@gmail.com"

    server.login(sender, os.environ.get('email_password'))

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
