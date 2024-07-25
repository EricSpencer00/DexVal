import os
import statistics
import matplotlib.pyplot as plt
from pydexcom import Dexcom
from twilio.rest import Client
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from stat_functions import high_mgdl, low_mgdl, high_mmol, low_mmol

app = Flask(__name__)

# Configure SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///glucose.db'
db = SQLAlchemy(app)

# Define GlucoseReading model
class GlucoseReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    trend_arrow = db.Column(db.String(1))
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GlucoseReading {self.id}>'

# Initialize Dexcom client
dexcom_username = os.getenv("DEXCOM_USERNAME")
dexcom_password = os.getenv("DEXCOM_PASSWORD")
if not dexcom_username or not dexcom_password:
    raise ValueError("DEXCOM_USERNAME or DEXCOM_PASSWORD environment variables are not set.")
dexcom = Dexcom(dexcom_username, dexcom_password)

# Initialize Twilio client
twilio_account = os.getenv("account_sid")
twilio_token = os.getenv("auth_token")
twilio_phone_from = os.getenv("TWILIO_FROM")
twilio_phone_to = os.getenv("TWILIO_TO")
if not twilio_account or not twilio_token:
    raise ValueError("TWILIO_ACCOUNT or TWILIO_TOKEN environment variables are not set.")
client = Client(twilio_account, twilio_token)

# Function to categorize glucose levels
def categorize_glucose_mgdl(glucose_value, trend_arrow):
    if glucose_value < low_mgdl:
        return "Low"
    elif low_mgdl <= glucose_value < high_mgdl:
        return "In Range"
    else: # glucose_value >= high_mgdl
        return "High"
    
def categorize_glucose_mmol(glucose_value, trend_arrow):
    if glucose_value < low_mmol:
        return "Low"
    elif low_mmol <= glucose_value < high_mmol:
        return "In Range"
    else: # glucose_value >= high_mmol
        return "High"

# Route to fetch current glucose reading
@app.route('/')
def index():
    glucose_reading = dexcom.get_current_glucose_reading()
    glucose_state = categorize_glucose_mgdl(glucose_reading.value, glucose_reading.trend_arrow)
    
    # Save current glucose reading to the database
    new_reading = GlucoseReading(value=glucose_reading.value,
                                 trend_arrow=glucose_reading.trend_arrow)
    db.session.add(new_reading)
    db.session.commit()
    
    return render_template('index.html', glucose_reading=glucose_reading, glucose_state=glucose_state)

# Route to display glucose history graph
@app.route('/history')
def history():
    glucose_readings = GlucoseReading.query.all()
    glucose_values = [reading.value for reading in glucose_readings]
    timestamps = [reading.datetime for reading in glucose_readings]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, glucose_values, marker='o')
    plt.title('Glucose Readings Over Time')
    plt.xlabel('Time')
    plt.ylabel('Glucose Level (mg/dL)')
    plt.xticks(rotation=45)
    plt.grid(True)  
    plt.tight_layout()

    graph_path = '/static/glucose_history.png'
    plt.savefig('static/glucose_history.png')

    return render_template('history.html', graph_path=graph_path)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
