from flask import Flask, redirect, render_template, request, jsonify, session, url_for
from DexcomAPI import defs, stat_functions as stats
import requests
# from auth0.v3.authentication import GetToken
# from auth0.v3.authentication import Users
from authlib.integrations.flask_client import OAuth
import requests
import os

app = Flask(__name__, template_folder='DexcomAPI/templates')
app.secret_key = os.getenv("APP_SECRET_KEY")

AUTH0_CALLBACK_URL = 'http://localhost:5003/callback'
AUTH0_CLIENT_ID = 'your_auth0_client_id'
AUTH0_CLIENT_SECRET = 'your_auth0_client_secret'
AUTH0_DOMAIN = 'your_auth0_domain'
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
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

@app.route('/')
def index():
    # Get current glucose data
    current_glucose_mgdl = stats.get_current_value_mdgl(dexcom) or 'N/A'
    current_glucose_mmol = stats.get_current_value_mmol(dexcom) or 'N/A'
    glucose_state_mdgl = stats.get_glucose_state_mdgl(dexcom) or 'N/A'
    glucose_state_mmol = stats.get_glucose_state_mmol(dexcom) or 'N/A'
    average_glucose_mgdl = stats.get_average_glucose_mgdl(dexcom) or 'N/A'
    average_glucose_mmol = stats.get_average_glucose_mmol(dexcom) or 'N/A'
    median_glucose_mgdl = stats.get_median_glucose_mgdl(dexcom) or 'N/A'
    median_glucose_mmol = stats.get_median_glucose_mmol(dexcom) or 'N/A'
    stdev_glucose_mgdl = stats.get_stdev_glucose_mgdl(dexcom) or 'N/A'
    stdev_glucose_mmol = stats.get_stdev_glucose_mmol(dexcom) or 'N/A'
    min_glucose_mgdl = stats.get_min_glucose_mgdl(dexcom) or 'N/A'
    min_glucose_mmol = stats.get_min_glucose_mmol(dexcom) or 'N/A'
    max_glucose_mgdl = stats.get_max_glucose_mgdl(dexcom) or 'N/A'
    max_glucose_mmol = stats.get_max_glucose_mmol(dexcom) or 'N/A'
    glucose_range_mgdl = stats.get_glucose_range_mgdl(dexcom) or 'N/A'
    glucose_range_mmol = stats.get_glucose_range_mmol(dexcom) or 'N/A'
    coef_variation_percentage = stats.get_coef_variation_percentage(dexcom) or 'N/A'
    glycemic_variability_index = stats.get_glycemic_variability_index(dexcom) or 'N/A'
    estimated_a1c = stats.get_estimated_a1c(dexcom) or 'N/A'
    time_in_range_percentage = stats.time_in_range_percentage or 'N/A' 

    # Render template with the glucose data
    return render_template('index.html', 
                           current_glucose_mgdl=current_glucose_mgdl,
                           current_glucose_mmol=current_glucose_mmol,
                           glucose_state_mdgl=glucose_state_mdgl,
                           glucose_state_mmol=glucose_state_mmol,
                           average_glucose_mgdl=average_glucose_mgdl,
                           average_glucose_mmol=average_glucose_mmol,
                           median_glucose_mgdl=median_glucose_mgdl,
                           median_glucose_mmol=median_glucose_mmol,
                           stdev_glucose_mgdl=stdev_glucose_mgdl,
                           stdev_glucose_mmol=stdev_glucose_mmol,
                           min_glucose_mgdl=min_glucose_mgdl,
                           min_glucose_mmol=min_glucose_mmol,
                           max_glucose_mgdl=max_glucose_mgdl,
                           max_glucose_mmol=max_glucose_mmol,
                           glucose_range_mgdl=glucose_range_mgdl,
                           glucose_range_mmol=glucose_range_mmol,
                           coef_variation_percentage=coef_variation_percentage,
                           glycemic_variability_index=glycemic_variability_index,
                           estimated_a1c=estimated_a1c,
                           time_in_range_percentage=time_in_range_percentage)

@app.route('/login')
def login():
    return auth0.authorize(callback=url_for('auth_callback', _external=True))

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

@app.route('/dexcom-signin')
def dexcom_signin():
    return redirect(f'https://api.dexcom.com/v2/oauth2/login?client_id={your_dexcom_client_id}&redirect_uri=http://localhost:5003/dexcom-callback&response_type=code&scope=offline_access')

# Dexcom callback route
@app.route('/dexcom-callback')
def dexcom_callback():
    # Exchange the auth code for an access token
    auth_code = request.args.get('code')
    url = "https://api.dexcom.com/v2/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": "http://localhost:5003/dexcom-callback",
        "client_id": "your_dexcom_client_id",
        "client_secret": "your_dexcom_client_secret"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        session['dexcom_token'] = response.json()['access_token']
        return redirect('/')
    else:
        return f"Error: {response.status_code} - {response.text}"


if __name__ == '__main__':
    app.run(port=5003, debug=True)
