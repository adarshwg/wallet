import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


def generate_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    return otp


def configure():
    load_dotenv()


def get_email_payload():
    configure()
    return {
        "sender": os.getenv('sender_email_id'),
        "subject": "OTP Verification",
        "body": f'Your MudraPay OTP is {generate_otp()}',
        "password": os.getenv('app_code')
    }


def send_otp(receiver_email: str):
    print('sending otp ')
    msg = MIMEMultipart()
    email_payload = get_email_payload()
    msg["From"] = email_payload['sender']
    msg["To"] = receiver_email
    msg["Subject"] = email_payload['subject']
    msg.attach(MIMEText(email_payload['body'], "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_payload['sender'], email_payload['password'])
            server.send_message(msg)
            user_otp = email_payload['body'].split(' ')[-1]
            print(user_otp)
            return user_otp

    except Exception as exception:
        raise exception
