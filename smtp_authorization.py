import re
import random

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SMTPauthorizer:
    def __init__(self, secret, num_len=6):
        self.random_number = "".join([str(random.randint(1, 9)) for i in range(0, num_len)])
        self.re4mail = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        self.secret = secret
        self.last_confirmation_code = None

    def email_is_valid(self, email):
        return bool(re.fullmatch(self.re4mail, email))

    def send_confirmation_code(self, email):
        message = MIMEMultipart()
        message['From'] = self.secret['GM_LOGIN']
        message['To'] = email
        message['Subject'] = 'auth'
        message.attach(MIMEText(self.random_number, 'plain'))
        with smtplib.SMTP('smtp.gmail.com', 587) as session:
            session.starttls()
            session.login(self.secret['GM_LOGIN'], self.secret['GM_PASS'])
            text = message.as_string()
            session.sendmail(self.secret['GM_LOGIN'], email, text)
            session.quit()
        self.last_confirmation_code = self.random_number

    def confirm_email(self, code):
        assert self.last_confirmation_code, "First send an email! There is nothing to check here."
        return code == self.random_number
