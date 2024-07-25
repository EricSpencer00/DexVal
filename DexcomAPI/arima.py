#arima.py

import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from pydexcom import Dexcom

# Initialize Dexcom client
dexcom_username = os.getenv("DEXCOM_USERNAME")
dexcom_password = os.getenv("DEXCOM_PASSWORD")
dexcom = Dexcom(dexcom_username, dexcom_password)

# Get glucose readings and put into DataFrame
glucose_reading = dexcom.get_glucose_readings(minutes=1440, max_count=288)
glucose_values = [reading.value for reading in glucose_reading]
timestamps = [reading.datetime for reading in glucose_reading]
trends = [reading.trend_description for reading in glucose_reading]

glucose_data = pd.DataFrame({
    "timestamps": timestamps,
    "glucose_values": glucose_values,
    "trends": trends
})

current_time = datetime.datetime.now().strftime("%I:%M%p")
current_glucose = glucose_data.iloc[0]["glucose_values"]
print(f"Current Glucose Value at {current_time} (CDT): {current_glucose:.2f}")

# Select the 20 most recent points
glucose_data = glucose_data.sort_values(by="timestamps", ascending=False).head(20)

# Prepare data
X = glucose_data[["timestamps", "trends"]]
y = glucose_data["glucose_values"]

X["timestamps"] = pd.to_datetime(X["timestamps"]).astype(int) // 10**9

# One-hot encode the 'trends' column
encoder = OneHotEncoder(handle_unknown='ignore', categories=[['falling', 'falling slightly', 'rising', 'rising slightly', 'down', 'up']])
trend_encoded = encoder.fit_transform(X[['trends']])

# Concatenate the encoded DataFrame with the original features
X_encoded = pd.concat([X.drop(columns=['trends']), pd.DataFrame(trend_encoded.toarray(), columns=encoder.get_feature_names_out(['trends']))], axis=1)

# Train the model
model = LinearRegression()
model.fit(X_encoded, y)

# Predict the next 9 values
last_timestamp = max(timestamps) if timestamps else datetime.datetime.now()

next_timestamps = [last_timestamp + datetime.timedelta(minutes=5) * (i+1) for i in range(9)]

next_predictions = pd.DataFrame({
    "timestamps": next_timestamps * len(encoder.categories_[0]),  # Repeat each timestamp for each trend
    "trends": np.repeat(encoder.categories_[0], 9)  # Repeat each trend for each timestamp
})

next_predictions["timestamps"] = pd.to_datetime(next_predictions["timestamps"]).astype(int) // 10**9

# One-hot encode the trends in the prediction DataFrame
next_trend_encoded = encoder.transform(next_predictions[['trends']])
next_trend_encoded_df = pd.DataFrame(next_trend_encoded.toarray(), columns=encoder.get_feature_names_out(['trends']))

# Concatenate the encoded DataFrame with the original features
next_timestamps_encoded = pd.concat([next_predictions.drop(columns=['trends']), next_trend_encoded_df], axis=1)

# Predict the glucose values for the next timestamps
next_glucose_values = model.predict(next_timestamps_encoded)
next_glucose_values = np.maximum(next_glucose_values, 0)

print(f"Current time: {datetime.datetime.now().strftime('%I:%M%p')} (CDT) - Trend: {next_glucose_values[0]:.2f}\n")
print("Predicting future glucose levels...")
for i in range(1, len(next_timestamps)):
    time_string = (datetime.datetime.now() + datetime.timedelta(minutes=5*i)).strftime('%I:%M%p')
    print(f"{time_string} (CDT) - Trend: {next_glucose_values[i]:.2f}")
