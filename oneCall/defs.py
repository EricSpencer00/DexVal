import os
import mysql.connector
from dotenv import load_dotenv
from pydexcom import Dexcom
from twilio.rest import Client
import requests
from dataclasses import dataclass

load_dotenv()

get_low_mgdl = 70
get_high_mgdl = 180
get_low_mmol = round(get_low_mgdl / 18.01559, 4)
get_high_mmol = round(get_high_mgdl / 18.01559, 4)

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

    # Auth0 Configurations
    auth0_client_id: str = os.getenv("AUTH0_CLIENT_ID")
    auth0_client_secret: str = os.getenv("AUTH0_CLIENT_SECRET")
    auth0_domain: str = os.getenv("AUTH0_DOMAIN")
    auth0_callback_url: str = os.getenv("AUTH0_CALLBACK_URL")

config = Config()

# Dexcom Connection Functions
def get_dexcom_connection():
    """Establish and return a connection to Dexcom using environment variables"""
    if not config.dexcom_username or not config.dexcom_password:
        raise DexcomConnectionError("Dexcom username and password must be set as environment variables.")
    
    try:
        return Dexcom(username=config.dexcom_username, password=config.dexcom_password)
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

# Auth0 configuration
def auth0_login():
    """Generate Auth0 login URL with appropriate parameters."""
    auth0_url = f"https://{config.auth0_domain}/authorize"
    params = {
        "client_id": config.auth0_client_id,
        "redirect_uri": config.auth0_callback_url,
        "response_type": "code",
        "scope": "openid profile email"
    }
    try:
        response = requests.get(auth0_url, params=params)
        return response.url
    except Exception as e:
        raise Exception(f"Failed to initiate Auth0 login: {e}")
    
def get_secret_key():
    """Return the Flask secret key to be used"""
    APP_SECRET_KEY = os.urandom(24).hex()
    return APP_SECRET_KEY

def get_low_mgdl():
    """Return the low glucose threshold in mg/dL"""
    return 70

def get_high_mgdl():
    """Return the high glucose threshold in mg/dL"""
    return 180

def get_low_mmol():
    """Return the low glucose threshold in mmol/L"""
    return round(get_low_mgdl() / 18.01559, 4)

def get_high_mmol():
    """Return the high glucose threshold in mmol/L"""
    return round(get_high_mgdl() / 18.01559, 4)

def set_range(units, low, high):
    """
    Set the low and high glucose thresholds in one unit, 
    and automatically update the corresponding values in the other unit.

    Parameters:
    units (str): The units of the glucose thresholds ("mgdl" or "mmol").
    low (float): The low glucose threshold.
    high (float): The high glucose threshold.
    """
    global get_low_mgdl, get_high_mgdl, get_low_mmol, get_high_mmol

    # Default values
    if low is None and units == "mgdl":
        low = 70
    if high is None and units == "mgdl":
        high = 180
    if low is None and units == "mmol":
        low = round(70 / 18.01559, 4)
    if high is None and units == "mmol":
        high = round(180 / 18.01559, 4)

    # Update thresholds based on the units
    if units == "mgdl":
        get_low_mgdl = lambda: low
        get_high_mgdl = lambda: high
        get_low_mmol = lambda: round(low / 18.01559, 4)
        get_high_mmol = lambda: round(high / 18.01559, 4)
    elif units == "mmol":
        get_low_mmol = lambda: low
        get_high_mmol = lambda: high
        get_low_mgdl = lambda: round(low * 18.01559, 4)
        get_high_mgdl = lambda: round(high * 18.01559, 4)
    else:
        raise ValueError("Invalid units. Must be 'mgdl' or 'mmol'.")

    print(f"Low: {get_low_mgdl()} mg/dL, {get_low_mmol()} mmol/L")
    print(f"High: {get_high_mgdl()} mg/dL, {get_high_mmol()} mmol/L")
