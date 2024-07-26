# auto.py
''' 
    a reduced, simplified  main.py file that will
    run every five minutes with low amounts of data usage
'''

import smtplib
from pydexcom import Dexcom
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from defs import get_dexcom_connection, get_sender_email_credentials, get_receiver_email, get_database_connection
from stat_functions import concise_message_mdgl 

def send_notification(email_username, email_password, receiver_email, body):
    message = MIMEMultipart()
    # message["From"] = email_username
    message["To"] = receiver_email
    # message["Subject"] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        domain = email_username.split('@')[-1]
        smtp_server = f"smtp.{domain}"
        smtp_port = 587
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_username, email_password)
            server.sendmail(email_username, receiver_email, message.as_string())
        print("Message sent successfully")
    except Exception as e:
        print(f"error: {e}")

dexcom = get_dexcom_connection()
email_username, email_password = get_sender_email_credentials()
receiver_email = get_receiver_email()

glucose_data = dexcom.get_current_glucose_reading()
glucose_value = glucose_data.value
glucose_trend = glucose_data.trend_description

if glucose_value < 55 or glucose_value > 200:
    message = f"{glucose_value} + {glucose_trend}"
    print(message)

    # Send SMS notification
    receiver = get_receiver_email()
    send_notification(receiver, message)


