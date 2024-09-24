import os
import mysql.connector
from dotenv import load_dotenv
from pydexcom import Dexcom
from twilio.rest import Client
import requests
from dataclasses import dataclass

load_dotenv()

# Custom Exceptions
class DexcomConnectionError(Exception):
    pass

class DatabaseConnectionError(Exception):
    pass

class EmailCredentialsError(Exception):
    pass

class TwilioClientError(Exception):
    pass

@dataclass
class Config:
    dexcom_username: str = os.getenv("DEXCOM_USERNAME")
    dexcom_password: str = os.getenv("DEXCOM_PASSWORD")
    dexcom_client_id: str = os.getenv("DEXCOM_CLIENT_ID")
    dexcom_client_secret: str = os.getenv("DEXCOM_CLIENT_SECRET")
    dexcom_token_url: str = os.getenv("DEXCOM_TOKEN_URL")
    
    sql_host: str = os.getenv("sql_host")
    sql_user: str = os.getenv("sql_user")
    sql_password: str = os.getenv("sql_password")
    sql_database: str = os.getenv("sql_database")
    
    email_username: str = os.getenv("email_username")
    email_password: str = os.getenv("email_password")
    receiver_email: str = os.getenv("receiver_email")
    
    twilio_account_sid: str = os.getenv("twilio_account_sid")
    twilio_auth_token: str = os.getenv("twilio_auth_token")
    twilio_from: str = os.getenv("twilio_from")
    twilio_to: str = os.getenv("twilio_to")

config = Config()

# Dexcom Connection Functions
def get_dexcom_connection():
    """Establish and return a connection to Dexcom using environment variables"""
    if not config.dexcom_username or not config.dexcom_password:
        raise DexcomConnectionError("Dexcom username and password must be set as environment variables.")
    
    try:
        return Dexcom(config.dexcom_username, config.dexcom_password)
    except Exception as e:
        raise DexcomConnectionError(f"Failed to connect to Dexcom: {e}")

def get_access_token():
    """Get OAuth access token for Dexcom API"""
    if not config.dexcom_client_id or not config.dexcom_client_secret:
        raise DexcomConnectionError("Client ID and client secret must be set as environment variables.")
    
    payload = {
        "client_id": config.dexcom_client_id,
        "client_secret": config.dexcom_client_secret,
        "grant_type": "client_credentials"
    }
    try:
        response = requests.post(config.dexcom_token_url, data=payload)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        raise DexcomConnectionError(f"Failed to obtain access token: {e}")

# Database Connection Function
def get_sql_database_connection():
    """Connect to the SQL database using environment variables and return the connection"""
    try:
        connection = mysql.connector.connect(
            host=config.sql_host,
            user=config.sql_user,
            password=config.sql_password,
            database=config.sql_database
        )
        if connection.is_connected():
            print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as e:
        raise DatabaseConnectionError(f"Error connecting to MySQL database: {e}")

# Email Functions
def get_sender_email_credentials():
    """Retrieve sender's email credentials from environment variables"""
    if not config.email_username or not config.email_password:
        raise EmailCredentialsError("Email username and password must be set as environment variables.")
    
    return config.email_username, config.email_password

def get_receiver_email():
    """Retrieve receiver's email from environment variables"""
    if not config.receiver_email:
        raise EmailCredentialsError("Receiver email must be set as an environment variable.")
    
    return config.receiver_email

# Twilio Functions
def get_twilio_client():
    """Return Twilio client using environment variables"""
    if not all([config.twilio_account_sid, config.twilio_auth_token, config.twilio_from, config.twilio_to]):
        raise TwilioClientError("Twilio account SID, auth token, from, and to numbers must be set as environment variables.")
    
    try:
        return Client(config.twilio_account_sid, config.twilio_auth_token)
    except Exception as e:
        raise TwilioClientError(f"Failed to create Twilio client: {e}")

