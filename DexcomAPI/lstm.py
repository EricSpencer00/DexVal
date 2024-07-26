# import os
# import datetime
# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import OneHotEncoder
# from tensorflow.keras import Sequential
# from tensorflow.keras import LSTM, Dense
# from pydexcom import Dexcom

# # Initialize Dexcom client
# dexcom_username = os.getenv("DEXCOM_USERNAME")
# dexcom_password = os.getenv("DEXCOM_PASSWORD")
# dexcom = Dexcom(dexcom_username, dexcom_password)

# # Get glucose readings and put into DataFrame
# glucose_reading = dexcom.get_glucose_readings(minutes=1440, max_count=288)
# glucose_values = [reading.value for reading in glucose_reading]
# timestamps = [reading.datetime for reading in glucose_reading]
# trends = [reading.trend_description for reading in glucose_reading]

# glucose_data = pd.DataFrame({
#     "timestamps": timestamps,
#     "glucose_values": glucose_values,
#     "trends": trends
# })

# # Convert timestamps to datetime
# glucose_data["timestamps"] = pd.to_datetime(glucose_data["timestamps"])

# current_time = datetime.datetime.now().strftime("%I:%M %p")
# current_glucose = glucose_data.iloc[0]["glucose_values"]
# print(f"Current Glucose Value at {current_time} (CDT): {current_glucose:.2f}")

# # Sort by timestamps and select the 144 most recent points
# glucose_data = glucose_data.sort_values(by="timestamps", ascending=False).head(144)

# # Prepare data
# X = glucose_data[["timestamps", "trends"]]
# y = glucose_data["glucose_values"]

# # Preprocess timestamps
# X['hour'] = X['timestamps'].dt.hour
# X['minute'] = X['timestamps'].dt.minute

# # One-hot encode the 'trends' column
# encoder = OneHotEncoder(handle_unknown='ignore', categories=[['falling', 'falling slightly', 'rising', 'rising slightly', 'down', 'up']])
# trend_encoded = encoder.fit_transform(X[['trends']])

# # Drop original timestamp and trend columns
# X_encoded = X.drop(columns=['timestamps', 'trends'])

# # Concatenate one-hot encoded trends and numerical features
# X_encoded = pd.concat([X_encoded, pd.DataFrame(trend_encoded.toarray(), columns=encoder.get_feature_names_out(['trends']))], axis=1)

# # Reshape data for LSTM
# X_lstm = X_encoded.values.reshape((X_encoded.shape[0], 1, X_encoded.shape[1]))

# # Define the LSTM model
# model = Sequential()
# model.add(LSTM(50, activation='relu', input_shape=(X_lstm.shape[1], X_lstm.shape[2])))
# model.add(Dense(1))
# model.compile(optimizer='adam', loss='mse')

# # Train the model
# model.fit(X_lstm, y, epochs=100, verbose=0)

# # Predict the next 9 values
# last_timestamp = max(timestamps) if timestamps else datetime.datetime.now()

# next_timestamps = [last_timestamp + datetime.timedelta(minutes=5 * i) for i in range(1, 10)]

# next_predictions = pd.DataFrame({
#     "timestamps": next_timestamps * len(encoder.categories_[0]),  # Repeat each timestamp for each trend
#     "trends": np.repeat(encoder.categories_[0], 9)  # Repeat each trend for each timestamp
# })

# # Preprocess future timestamps
# next_predictions['hour'] = next_predictions['timestamps'].dt.hour
# next_predictions['minute'] = next_predictions['timestamps'].dt.minute

# # One-hot encode the trends in the prediction DataFrame
# next_trend_encoded = encoder.transform(next_predictions[['trends']])

# # Drop original timestamp and trend columns
# next_predictions_encoded = next_predictions.drop(columns=['timestamps', 'trends'])

# # Concatenate one-hot encoded trends and numerical features
# next_predictions_encoded = pd.concat([next_predictions_encoded, pd.DataFrame(next_trend_encoded.toarray(), columns=encoder.get_feature_names_out(['trends']))], axis=1)

# # Reshape data for LSTM
# next_predictions_lstm = next_predictions_encoded.values.reshape((next_predictions_encoded.shape[0], 1, next_predictions_encoded.shape[1]))

# # Predict the glucose values for the next timestamps
# next_glucose_values = model.predict(next_predictions_lstm).flatten()
# next_glucose_values = np.maximum(next_glucose_values, 0)

# print(f"\nCurrent time: {datetime.datetime.now().strftime('%I:%M %p')} (CDT)")
# print("Predicting future glucose levels...")
# for i in range(len(next_timestamps)):
#     time_string = next_timestamps[i].strftime('%I:%M %p')
#     print(f"{time_string} (CDT) - Trend: {next_predictions['trends'].iloc[i]}: {next_glucose_values[i]:.2f}")
