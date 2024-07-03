# app.py
'''
Initialize a webapp using Flask
'''
from flask import Flask, render_template, request, redirect, url_for
from main import get_dexcom_connection
import os
import smtplib
from pydexcom import Dexcom
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from defs import get_dexcom_connection, get_sender_email_credentials, get_receiver_email, get_database_connection
from stat_functions import verbose_message_mgdl, verbose_message_mmol, concise_message_mdgl, concise_message_mmol
# from database import insert_glucose_readings.

app = Flask(__name__)

try:
    dexcom = get_dexcom_connection()
except ValueError as e:
    f"Error: {e}", 500
    dexcom = None

email_username, email_password = get_sender_email_credentials()
receiver_email = get_receiver_email()

@app.route('/')
def index():
    if dexcom:
        verbose_mgdl = verbose_message_mgdl(dexcom)
        verbose_mmol = verbose_message_mmol(dexcom)
        concise_mdgl = concise_message_mdgl(dexcom)
        concise_mmol = concise_message_mmol(dexcom)
    else:
        verbose_mgdl = verbose_mmol = concise_mdgl = concise_mmol = "Error connecting to Dexcom"

    return render_template('index.html', verbose_mgdl=verbose_mgdl, verbose_mmol=verbose_mmol,
                           concise_mdgl=concise_mdgl, concise_mmol=concise_mmol)

@app.route('/send-email', methods=['POST'])
def send_email():

    if not dexcom:
        return "Error: Cannot send email without Dexcom connection"

    message = MIMEMultipart()
    message["From"] = email_username
    message["To"] = receiver_email
    message.attach(MIMEText(concise_message_mdgl(dexcom), 'plain'))

    try:
        domain = email_username.split('@')[-1]
        smtp_server = f"smtp.{domain}"
        smtp_port = 587
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_username, email_password)
            server.sendmail(email_username, receiver_email, message.as_string())
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error: {e}"
    
# Comment out until solution towards dynamic database found
'''@app.route('/insert-to-database')
def insert_to_database():
    db = get_database_connection()
    db_name = os.getenv("sql_database")

    try: 
        insert_glucose_readings(dexcom, db, db_name)
        return "Data inserted into database successfully"
    except Exception as e:
        return f"Error: {e}"
    finally:
        db.close()'''

if __name__ == '__main__':
    app.run(debug = True)