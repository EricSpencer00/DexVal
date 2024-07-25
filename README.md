## main.py:

Text your phone number your current Glucose Number!

Display your CGM data to your terminal using Python + Pydexcom!

A Dexcom account with a physical CGM and data is required for the program to work.
A valid email address, and phone number with email-to-text support is required for alerts.
A MySQL database and program usage for longer than 24 hours are required for data storage longer than 24 hours.

## Instructions
Create an .env file with your Dexcom, Database, and Email credentials like so:
[Sample Environment Variables](env_sample.md)

After you have made your .env file, place it in the same working directory as the Python file.

You will need to allow your Dexcom's data to be accessed by Pydexcom's API system. Pydexcom only works using the Dexcom Share feature.

To do this:
- Make sure you have at least one follower on Dexcom Share, this can be yourself on a different account
- If your account is newer, you may use an email in place of a username, make sure you know which type you account is
- Then, make sure you are sharing the credentials for your Dexcom account, not the follower's account
- You will need to make sure your password is not only numbers, as this will cause Pydexcom to not recognize your password

You will need to install pydexcom and MySQL for all features to work, I installed MySQL using Homebrew on my Mac.

```
pip3 install pydexcom
```
```
brew install mysql
brew services start mysql
```

Example Output:
```
Your current glucose level is 149 mg/dL (steady →)
Time of reading: 2024-05-09 16:15:06
Glucose state: In Range
Average glucose level: 143.3056 mg/dL
Estimated A1C: 9.5817
Time in Range (70-150 mg/dL): 69.44%
Median Glucose: 128.0 mg/dL
Standard Deviation: 42.1561 mg/dL
Minimum Glucose: 65 mg/dL
Maximum Glucose: 240 mg/dL
Glucose Range: 175 mg/dL
Coef. of Variation: 29.4169%
Glycemic Variability Index: 98.03242686015963%
```
## slope.py
Predict the next values of your Dexcom graph!

Make sure your Dexcom credentials are in an .env file like before.

Install pydexcom, pandas, numpy, and skikit-learn for this script to work

```
pip3 install pydexcom scikit-learn pandas numpy
```

Example Output:
```
Current Glucose Value at 03:41PM (CDT): 157.00
Current time: 03:41PM (CDT) - Trend: 158.30

Predicting future glucose levels...
03:46PM (CDT) - Trend: 160.20
03:51PM (CDT) - Trend: 162.10
03:56PM (CDT) - Trend: 164.00
```

## arima.py

Predict the next values of your Dexcom graph!

Make sure your Dexcom credentials are in an .env file like before.

Install pydexcom, pandas, numpy, and skikit-learn for this script to work

```
pip3 install pydexcom scikit-learn pandas numpy
```

Example Output:
```
Current time: 11:37PM (CDT) - Trend: falling: 124.30

Predicting future glucose levels...
11:42PM (CDT) - Trend: falling: 120.93
11:47PM (CDT) - Trend: falling: 117.55
11:52PM (CDT) - Trend: falling: 114.18
11:57PM (CDT) - Trend: falling: 110.81
12:02AM (CDT) - Trend: falling: 107.43
12:07AM (CDT) - Trend: falling: 104.06
12:12AM (CDT) - Trend: falling: 100.69
12:17AM (CDT) - Trend: falling: 97.31
```
This information is based solely on data, and does not incorporate factors like insulin/carb correction. It's a good predictor of what would happen to you if you didn't do anything based on your current trends. The program takes the 20 previous points and predicts the next readings based on linear regression.

## Background information

Being a Type 1 Diabetic, a CGM is necessary for my day to day life. 
The Dexcom allows me to see my blood glucose levels throughout the day. 
Things like a Time in Range percentage and A1C estimator keep me alive and help 
make sure I am staying healthy.
Through a sensor on my body, a transmitter reads the level given to it by the sensor
and then transmits the number to my phone using Dexcom's cloud database.
Using Dexcom's g6 mobile app I can see this data, up to 24 hours.
Using Dexcom's Clarity mobile app I can see the data for the past year.
However, I am looking to do more than what the Clarity app does.
I want to learn how my habits, trends, and other factors can influence
my data. As of right now, all I can do is display data, but in the
future I hope to have even more functionality than apps like Sugarmate 
and Clarity




