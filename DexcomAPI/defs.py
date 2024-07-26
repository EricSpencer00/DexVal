# defs.py

import os
import mysql.connector
import pydexcom
from dotenv import load_dotenv
from twilio.rest import Client
import requests

load_dotenv()

class DexcomConnectionError(Exception):
    pass

class DatabaseConnectionError(Exception):
    pass

class EmailCredentialsError(Exception):
    pass

class TwilioClientError(Exception):
    pass

def get_dexcom_connection():
    """Establish and return a connection to Dexcom using environment variables"""
    dexcom_username = os.getenv("dexcom_username")
    dexcom_password = os.getenv("dexcom_password")

    if not dexcom_username or not dexcom_password:
        raise DexcomConnectionError("Dexcom username and password must be set as environment variables.")

    try:
        return pydexcom.Dexcom(dexcom_username, dexcom_password)
    except Exception as e:
        raise DexcomConnectionError(f"Failed to connect to Dexcom: {e}")

def get_dexcom_connection_access():
    """Establish and return a connection to Dexcom using AuthLib OAuth request"""
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")

    if not client_id or not client_secret:
        raise DexcomConnectionError("Client ID and client secret must be set as environment variables.")

    try:
        access_token = get_access_token(client_id, client_secret)
        return access_token
    except Exception as e:
        raise DexcomConnectionError(f"Failed to obtain Dexcom access token: {e}")

def get_access_token(client_id, client_secret):
    token_url = "https://api.dexcom.com/v2/oauth2/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        raise DexcomConnectionError(f"Failed to obtain access token: {e}")

def get_database_connection():
    """Connect to the SQL database using environment variables and return the connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("sql_host"),
            user=os.getenv("sql_user"),
            password=os.getenv("sql_password"),
            database=os.getenv("sql_database")
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Error connecting to MySQL database: {e}")

def get_sender_email_credentials():
    """Retrieve sender's email credentials from environment variables"""
    email_username = os.getenv("email_username")
    email_password = os.getenv("email_password")

    if not email_username or not email_password:
        raise EmailCredentialsError("Email username and password must be set as environment variables.")

    return email_username, email_password

def get_receiver_email():
    """Retrieve receiver's email from environment variables"""
    receiver_email = os.getenv("receiver_email")

    if not receiver_email:
        raise EmailCredentialsError("Receiver email must be set as an environment variable.")

    return receiver_email

def get_twilio_client():
    """Return Twilio client using environment variables"""
    account_sid = os.getenv("twilio_account_sid")
    auth_token = os.getenv("twilio_auth_token")
    twilio_from = os.getenv("twilio_from")
    twilio_to = os.getenv("twilio_to")

    if not all([account_sid, auth_token, twilio_from, twilio_to]):
        raise TwilioClientError("Twilio account SID, auth token, from, and to numbers must be set as environment variables.")

    try:
        return Client(account_sid, auth_token, twilio_from, twilio_to)
    except Exception as e:
        raise TwilioClientError(f"Failed to create Twilio client: {e}")
