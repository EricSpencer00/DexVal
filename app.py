from flask import Flask, redirect, render_template, request, jsonify, session, url_for
from flask_caching import Cache
from DexcomAPI import defs, stat_functions as stats
import requests
from authlib.integrations.flask_client import OAuth
import requests
import os

app = Flask(__name__, 
            template_folder="DexcomAPI/templates", 
            static_folder="DexcomAPI/static")
app.config["CACHE_TYPE"] = "SimpleCache"  # Use SimpleCache for in-memory caching
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # Cache data for 5 minutes
cache = Cache(app)

@cache.memoize()
def get_cached_glucose_metrics(dexcom):
    return stats.get_glucose_metrics(dexcom)

app.secret_key = defs.get_secret_key()

# Initialize Dexcom object with appropriate credentials
dexcom = defs.get_dexcom_connection()

def safe_get_value(func, *args):
    """Helper function to safely get values or return 'N/A' if None."""
    return func(*args) or 'N/A'

@app.route('/')
def index():
    # Redirect to /show-dexcom-data to handle all glucose data logic
    return redirect('/show-dexcom-data')

@app.route('/update_global_mdgl_range', methods=['POST'])
def update_mdgl():
    data = request.json
    stats.high_mgdl = data['high_mgdl']
    stats.low_mgdl = data['low_mgdl']
    return jsonify({"message": "mdgl value(s) updated successfully"}), 200

@app.route('/update_global_mmol_range', methods=['POST'])
def update_mmol():
    data = request.json
    stats.high_mmol = data['high_mmol']
    stats.low_mmol = data['low_mmol']
    return jsonify({"message": "mmol value(s) updated successfully"}), 200

# Dexcom sign-in route
@app.route('/dexcom-signin')
def dexcom_signin():
    dexcom_client_id = os.getenv('DEXCOM_CLIENT_ID')
    redirect_uri = os.getenv('DEXCOM_REDIRECT_URI')
    dexcom_login_url = f"https://sandbox-api.dexcom.com/v2/oauth2/login?client_id={dexcom_client_id}&redirect_uri={redirect_uri}&response_type=code&scope=offline_access"
    return redirect(dexcom_login_url)

# Dexcom callback route
@app.route('/dexcom-callback')
def dexcom_callback():
    dexcom_client_id = os.getenv('DEXCOM_CLIENT_ID')
    dexcom_client_secret = os.getenv('DEXCOM_CLIENT_SECRET')
    auth_code = request.args.get('code')
    
    dexcom_token_url = "https://sandbox-api.dexcom.com/v2/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": "http://localhost:5001/dexcom-callback",
        "client_id": dexcom_client_id,
        "client_secret": dexcom_client_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(dexcom_token_url, data=payload, headers=headers)
    if response.status_code == 200:
        session['dexcom_token'] = response.json()['access_token']
        # return redirect('/')
        return redirect('/show-dexcom-data')
    else:
        return f"Error: {response.status_code} - {response.text}"
    
@app.route('/show-dexcom-data')
def show_dexcom_data():
    # Check if the user is authenticated
    access_token = session.get('dexcom_token')
    if not access_token:
        return redirect('/dexcom-signin')  # Redirect to sign-in if no token

    # Define the Dexcom API URL and headers
    dexcom_api_url = "https://sandbox-api.dexcom.com/v2/users/self/egvs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "startDate": "2023-10-01T00:00:00",  # Adjust start/end dates as needed
        "endDate": "2023-10-05T00:00:00"
    }

    # Make the API request
    response = requests.get(dexcom_api_url, headers=headers, params=params)
    if response.status_code == 200:
        # Fetch and process glucose data in one place
        glucose_data = stats.get_glucose_metrics(dexcom)
        if not glucose_data:
            return "Failed to retrieve glucose metrics."

        # Render the data on the template
        return render_template('index.html', **glucose_data)
    else:
        return f"Error: {response.status_code} - {response.text}"


if __name__ == '__main__':
    app.run(port=5001, debug=True)
