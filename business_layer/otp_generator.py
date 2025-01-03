import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import bcrypt
from dotenv import load_dotenv
import os


def generate_otp():
    #generating the otp
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))

    #hashing the otp
    # otp = hash_otp(otp)

    #return the hash of the otp
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


def hash_otp(otp: str):
    byte_arr = otp.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_otp = bcrypt.hashpw(byte_arr, salt)
    return hashed_otp


def match_otp(entered_otp: str, hashed_otp: str):
    result = bcrypt.checkpw(entered_otp.encode('utf-8'), hashed_otp.encode('utf-8'))
    print(result, ' is the result of matching the otp')
    return result


def send_otp(receiver_email: str):
    print('sending otp ')
    msg = MIMEMultipart()
    email_payload = get_email_payload()
    msg["From"] = email_payload['sender']
    msg["To"] = receiver_email
    msg["Subject"] = email_payload['subject']
    msg.attach(MIMEText(email_payload['body'], "plain"))
    print(email_payload)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_payload['sender'], email_payload['password'])
            server.send_message(msg)
            user_otp = email_payload['body'].split(' ')[-1]
            print(user_otp)
            return hash_otp(user_otp)

    except Exception as exception:
        raise exception
