import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from template.tasks.base import BaseTask
from template._celery import app as celery
from template.config import Config


@celery.task(name='users.send_registration_confirmation_email', base=BaseTask)
def send_email(to, subject, **kwargs):
    message = MIMEMultipart('alternative')
    message["Subject"] = subject
    message["From"] = Config.MAIL_DEFAULT_SENDER
    message['To'] = to
    message.attach(MIMEText(kwargs.get('text_body'), 'plain', 'utf-8'))
    message.attach(MIMEText(kwargs.get('html_body'), 'html', 'utf-8'))
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
        # TODO: Send email here
        server.sendmail(
            Config.MAIL_DEFAULT_SENDER, to, message.as_string()
        )
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 
    return True
