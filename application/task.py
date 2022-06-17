from django.core.mail import send_mail, EmailMessage

from AuthenticationSystem import settings
from AuthenticationSystem.celery import app
from application.models import UserInfo


@app.task(name="send_email_notification")
def send_email_notification():
    users = UserInfo.objects.all()
    try:
        for data in users:
            msg = EmailMessage(
                'AIT Registration',
                "check email",
                'Alpine Insitude Of Techonology',
                [data.email],

            )
            msg.content_subtype = "html"
            msg.send()
    except:
        print("error")
