from flask import Flask, redirect, render_template, request, jsonify, session, url_for
import requests
import os

app = Flask(__name__, template_folder="DexcomAPI/templates", static_folder="DexcomAPI/static")
app.secret_key = os.getenv('SECRET_KEY')  # Store this securely

# Dexcom OAuth client ID and secret
DEXCOM_CLIENT_ID = os.getenv('DEXCOM_CLIENT_ID')
DEXCOM_CLIENT_SECRET = os.getenv('DEXCOM_CLIENT_SECRET')
DEXCOM_REDIRECT_URI = os.getenv('DEXCOM_REDIRECT_URI')

# --- Helper Functions ---

def is_logged_in():
    """Check if user is authenticated with Dexcom."""
    return 'dexcom_token' in session

def get_dexcom_data():
    """Fetch Dexcom glucose data for the logged-in user."""
    access_token = session.get('dexcom_token')
    dexcom_api_url = "https://api.dexcom.com/v2/users/self/egvs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    # Set date range (modify as per your needs)
    params = {
        "startDate": "2023-10-01T00:00:00",  
        "endDate": "2023-10-05T00:00:00"
    }

    response = requests.get(dexcom_api_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()  # Glucose data
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# --- Routes ---

# Landing page route
@app.route('/')
def index():
    if not is_logged_in():
        return redirect('/login')  # Redirect to login if not authenticated
    else:
        try:
            glucose_data = get_dexcom_data()  # Get glucose data after login
            return render_template('dexcom_data.html', glucose_data=glucose_data)
        except Exception as e:
            return str(e)  # Handle any exceptions (like expired token)

# Login page route
@app.route('/login')
def login():
    return render_template('login.html')  # Show the login page

# Dexcom sign-in route (Starts the OAuth process)
@app.route('/dexcom-signin')
def dexcom_signin():
    dexcom_login_url = (
        f"https://api.dexcom.com/v2/oauth2/login?"
        f"client_id={DEXCOM_CLIENT_ID}&redirect_uri={DEXCOM_REDIRECT_URI}&"
        f"response_type=code&scope=offline_access"
    )
    return redirect(dexcom_login_url)

# Dexcom callback route (Handle the OAuth callback)
@app.route('/dexcom-callback')
def dexcom_callback():
    auth_code = request.args.get('code')
    
    dexcom_token_url = "https://api.dexcom.com/v2/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": DEXCOM_REDIRECT_URI,
        "client_id": DEXCOM_CLIENT_ID,
        "client_secret": DEXCOM_CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(dexcom_token_url, data=payload, headers=headers)
    if response.status_code == 200:
        session['dexcom_token'] = response.json()['access_token']  # Store token in session
        return redirect('/')  # Redirect to index to show glucose data
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- Run the App ---

if __name__ == '__main__':
    app.run(port=5001, debug=True)
