from flask import Flask, redirect, render_template, request, jsonify, session, url_for
from DexcomAPI import defs, stat_functions as stats
import requests
from authlib.integrations.flask_client import OAuth
import requests
import os

app = Flask(__name__, 
            template_folder="DexcomAPI/templates", 
            static_folder="DexcomAPI/static")
app.secret_key = defs.get_secret_key()

# Load environment variables for Auth0
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')

# Define Auth0 URLs
AUTH0_BASE_URL = f'https://{AUTH0_DOMAIN}'
AUTH0_ACCESS_TOKEN_URL = f'https://{AUTH0_DOMAIN}/oauth/token'
AUTH0_AUTHORIZE_URL = f'https://{AUTH0_DOMAIN}/authorize'

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_ACCESS_TOKEN_URL,
    authorize_url=AUTH0_AUTHORIZE_URL,
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# Initialize Dexcom object with appropriate credentials
dexcom = defs.get_dexcom_connection()

def safe_get_value(func, *args):
    """Helper function to safely get values or return 'N/A' if None."""
    return func(*args) or 'N/A'

@app.route('/')
def index():
    # Dictionary to store glucose data
    glucose_data = {
        'current_glucose_mgdl': safe_get_value(stats.get_current_value_mdgl, dexcom),
        'current_glucose_mmol': safe_get_value(stats.get_current_value_mmol, dexcom),
        'glucose_state_mdgl': safe_get_value(stats.get_glucose_state_mdgl, dexcom),
        'glucose_state_mmol': safe_get_value(stats.get_glucose_state_mmol, dexcom),
        'average_glucose_mgdl': safe_get_value(stats.get_average_glucose_mgdl, dexcom),
        'average_glucose_mmol': safe_get_value(stats.get_average_glucose_mmol, dexcom),
        'median_glucose_mgdl': safe_get_value(stats.get_median_glucose_mgdl, dexcom),
        'median_glucose_mmol': safe_get_value(stats.get_median_glucose_mmol, dexcom),
        'stdev_glucose_mgdl': safe_get_value(stats.get_stdev_glucose_mgdl, dexcom),
        'stdev_glucose_mmol': safe_get_value(stats.get_stdev_glucose_mmol, dexcom),
        'min_glucose_mgdl': safe_get_value(stats.get_min_glucose_mgdl, dexcom),
        'min_glucose_mmol': safe_get_value(stats.get_min_glucose_mmol, dexcom),
        'max_glucose_mgdl': safe_get_value(stats.get_max_glucose_mgdl, dexcom),
        'max_glucose_mmol': safe_get_value(stats.get_max_glucose_mmol, dexcom),
        'glucose_range_mgdl': safe_get_value(stats.get_glucose_range_mgdl, dexcom),
        'glucose_range_mmol': safe_get_value(stats.get_glucose_range_mmol, dexcom),
        'coef_variation_percentage': safe_get_value(stats.get_coef_variation_percentage, dexcom),
        'glycemic_variability_index': safe_get_value(stats.get_glycemic_variability_index, dexcom),
        'estimated_a1c': safe_get_value(stats.get_estimated_a1c, dexcom),
        'time_in_range_percentage': safe_get_value(lambda: stats.time_in_range_percentage)  # Assuming this is a direct variable
    }

    # Render template with glucose data
    return render_template('index.html', **glucose_data)

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('auth_callback', _external=True))

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

@app.route('/callback')
def auth_callback():
    token = auth0.authorize_access_token()  # Get token using Authlib
    session['auth_token'] = token
    userinfo = auth0.get('userinfo')
    session['profile'] = userinfo.json()
    return redirect('/')

# Dexcom sign-in route
@app.route('/dexcom-signin')
def dexcom_signin():
    dexcom_client_id = os.getenv('DEXCOM_CLIENT_ID')
    # redirect_uri = url_for('dexcom_callback', _external=True)
    redirect_uri = os.getenv('DEXCOM_REDIRECT_URI')
    return redirect(f'https://api.dexcom.com/v2/oauth2/login?client_id={dexcom_client_id}&redirect_uri={redirect_uri}&response_type=code&scope=offline_access')

# Dexcom callback route
@app.route('/dexcom-callback')
def dexcom_callback():
    dexcom_client_id = os.getenv('DEXCOM_CLIENT_ID')
    dexcom_client_secret = os.getenv('DEXCOM_CLIENT_SECRET')
    auth_code = request.args.get('code')
    
    dexcom_token_url = "https://api.dexcom.com/v2/oauth2/token"
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
        return redirect('/')
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == '__main__':
    app.run(port=5001, debug=True)
