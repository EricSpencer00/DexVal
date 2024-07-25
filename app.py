from flask import Flask

app = Flask(__name__)

def get_current_value_mdgl(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    glucose_value = glucose_reading.value
    return glucose_value

# @app.route('/')
# def index():
#     dexcom = Dexcom('username', 'password')  # Initialize your Dexcom object with the appropriate credentials
#     glucose_value = get_current_value_mdgl(dexcom)
#     return render_template('index.html', glucose_value=glucose_value)

if __name__ == '__main__':
    app.run(debug=True)