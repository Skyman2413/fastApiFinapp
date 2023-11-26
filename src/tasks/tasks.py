import smtplib
from email.message import EmailMessage

from celery import Celery

from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.google.com"
SMTP_PORT = 456

celery = Celery('tasks', broker='redis://:gjhnatkm@192.168.3.19/1')


def get_email_template(username, email_address):
    email = EmailMessage()
    email["Subject"] = "FastApiEdu"
    email["From"] = SMTP_USER
    email["To"] = email_address
    email.set_content(
        f'<div>Привет, {username}</div>'
    )
    return email


@celery.task()
def my_first_task(username: str, email_address: str):
    email = get_email_template(username, email_address)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)