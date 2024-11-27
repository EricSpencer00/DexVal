import logging
import statistics
import defs
import json
import os
from defs import get_dexcom_connection
from pydexcom import Dexcom
from typing import List

def fetch_glucose_data(dexcom):
    """
    Fetch all necessary glucose data in a single call.
    """
    try:
        current_reading = dexcom.get_current_glucose_reading()
        glucose_readings = dexcom.get_glucose_readings(minutes=1440, max_count=288)
        return current_reading, glucose_readings
    except Exception as e:
        logging.error(f"Error fetching glucose data: {e}")
        return None, []
    

def process_glucose_data(current_reading, glucose_readings):
    """
    Preprocess glucose data and compute statistics.

    Args:
        current_reading: Current glucose reading
        glucose_readings: List of glucose readings 

    Returns:
        Dictionary of glucose statistics
        0: current_value
        1: current_trend_arrow
        2: time_in_range
        3: average_mgdl
        4: median_mgdl
        5: stdev_mgdl
        6: min_mgdl
        7: max_mgdl
        8: glucose_range_mgdl
        9: current_mmol
        10: average_mmol
        11: median_mmol
        12: stdev_mmol
        13: min_mmol
        14: max_mmol
        15: glucose_range_mmol
    """
    if current_reading is None or not glucose_readings:
        logging.error("Missing glucose data.")
        return {}

    glucose_values = [reading.value for reading in glucose_readings]
    glucose_stats = {
        "current_value": current_reading.value,
        "current_trend_arrow": current_reading.trend_arrow,
        "time_in_range": round(len([g for g in glucose_values if defs.get_low_mgdl <= g <= defs.get_high_mgdl]) / len(glucose_values) * 100, 4),

        "average_mgdl": round(statistics.mean(glucose_values), 4),
        "median_mgdl": round(statistics.median(glucose_values), 4),
        "stdev_mgdl": round(statistics.stdev(glucose_values), 4),
        "min_mgdl": min(glucose_values),
        "max_mgdl": max(glucose_values),
        "glucose_range_mgdl": round(max(glucose_values) - min(glucose_values), 4),

        "current_mmol": round(current_reading.value / 18.01559, 4),
        "average_mmol": round(statistics.mean(glucose_values) / 18.01559, 4),
        "median_mmol": round(statistics.median(glucose_values) / 18.01559, 4),
        "stdev_mmol": round(statistics.stdev(glucose_values) / 18.01559, 4),
        "min_mmol": round(min(glucose_values) / 18.01559, 4),
        "max_mmol": round(max(glucose_values) / 18.01559, 4),
        "glucose_range_mmol": round((max(glucose_values) - min(glucose_values)) / 18.01559, 4),
    }

    save_glucose_data(glucose_stats)

    return glucose_stats


def save_glucose_data(data, filename="glucose_data.json"):
    """
    Save glucose data to a JSON file.
    """
    if os.path.exists(filename):
        with open(filename, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []

    existing_data.append(data)

    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)


def generate_verbose_message(stats, units="mgdl"):
    """
    Generate a verbose message using precomputed statistics.
    """
    if not stats:
        return "Unable to generate glucose data message."

    if units == "mgdl":
        message = (
            f"Current glucose: {stats['current_value']} mg/dL ({stats['current_trend_arrow']})\n"
            f"Average: {stats['average_mgdl']} mg/dL ({stats['average_mmol']} mmol/L)\n"
            f"Median: {stats['median_mgdl']} mg/dL ({stats['median_mmol']} mmol/L)\n"
            f"Min/Max: {stats['min_mgdl']} / {stats['max_mgdl']} mg/dL\n"
            f"Time in Range: {stats['time_in_range']}%\n"
            f"Glucose Range: {stats['glucose_range_mgdl']} mg/dL\n"
        )
    elif units == "mmol": 
        message = (
            f"Current glucose: {stats['current_mmol']} mmol/L ({stats['current_trend_arrow']})\n"
            f"Average: {stats['average_mmol']} mmol/L ({stats['average_mgdl']} mg/dL)\n"
            f"Median: {stats['median_mmol']} mmol/L ({stats['median_mgdl']} mg/dL)\n"
            f"Min/Max: {stats['min_mmol']} / {stats['max_mmol']} mmol/L\n"
            f"Time in Range: {stats['time_in_range']}%\n"
            f"Glucose Range: {stats['glucose_range_mmol']} mmol/L\n"
        )
    return message

def generate_simple_message(stats, units="mgdl"):
    """
    Generate a simple message using precomputed statistics.
    """
    if not stats:
        return "Unable to generate glucose data message."

    if units == "mgdl":
        message = f"Current: {stats['current_value']} mg/dL ({stats['current_trend_arrow']})"
    elif units == "mmol":
        message = f"Current: {stats['current_mmol']} mmol/L ({stats['current_trend_arrow']})"
    return message


def set_range(units, low, high):
    """
    Set the low and high glucose thresholds.
    """
    if units == "mgdl":
        defs.get_low_mgdl = low
        defs.get_high_mgdl = high
    elif units == "mmol":
        defs.get_low_mgdl = round(low * 18.01559, 4)
        defs.get_high_mgdl = round(high * 18.01559, 4)
    return defs.get_low_mgdl, defs.get_high_mgdl

# create a plt graph of the glucose data
def get_graph(glucose_readings, low_mgdl=70, high_mgdl=180, output_path="glucose_plot.png"):
    """
    Create a simple line graph of glucose data.

    Args:
        glucose_readings: List of glucose readings
        low_mgdl: Low glucose threshold in mg/dL
        high_mgdl: High glucose threshold in mg/dL
        output_path: Output path for the graph

    Returns:
        Path to the saved graph
    """
    # Importing the necessary libraries
    import matplotlib.pyplot as plt
    import numpy as np

    # Get data from dexcom
    glucose_graph: List = glucose_readings
    glucose_values = [reading.value for reading in glucose_graph]
    timestamps = [reading.datetime for reading in glucose_graph]
    trend_arrows = [reading.trend_arrow for reading in glucose_graph]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, glucose_values, color='black', linewidth=1)

    low_glucose = [idx for idx, reading in enumerate(glucose_values) if reading < low_mgdl]
    in_range_glucose = [idx for idx, reading in enumerate(glucose_values) if low_mgdl <= reading <= high_mgdl]
    high_glucose = [idx for idx, reading in enumerate(glucose_values) if reading > high_mgdl]

    if low_glucose:
        plt.axhline(y=min(glucose_values), color='red', linestyle='--', linewidth=1, alpha=0.5, xmin=min(low_glucose)/len(glucose_values), xmax=max(low_glucose)/len(glucose_values))
    if high_glucose:
        plt.axhline(y=max(glucose_values), color='red', linestyle='--', linewidth=1, alpha=0.5, xmin=min(high_glucose)/len(glucose_values), xmax=max(high_glucose)/len(glucose_values))
    if in_range_glucose:
        plt.axhline(y=70, color='green', linestyle='--', linewidth=1, alpha=0.5, xmin=min(in_range_glucose)/len(glucose_values), xmax=max(in_range_glucose)/len(glucose_values))
        plt.axhline(y=150, color='green', linestyle='--', linewidth=1, alpha=0.5, xmin=min(in_range_glucose)/len(glucose_values), xmax=max(in_range_glucose)/len(glucose_values))

    for i, arrow in enumerate(trend_arrows):
        if arrow == "↑":
            plt.scatter(timestamps[i], glucose_values[i], color='orange', marker='^', s=25)
        elif arrow == "↓":
            plt.scatter(timestamps[i], glucose_values[i], color='red', marker='v', s=25)
        else:
            plt.scatter(timestamps[i], glucose_values[i], color='green', marker='o', s=25)

    plt.title('Dexcom Glucose Readings Over the Past Day')
    plt.xlabel('Time (Day / Hour)')
    plt.ylabel('Glucose Level (mg/dL)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()

    return output_path

# dexcom = get_dexcom_connection()
# glucose_readings = fetch_glucose_data(dexcom)
# get_graph(glucose_readings, low_mgdl=70, high_mgdl=180, output_path="glucose_plot.png")

# test the functions
dexcom = get_dexcom_connection()
current_reading, glucose_readings = fetch_glucose_data(dexcom)
stats = process_glucose_data(current_reading, glucose_readings)
print(stats)
message = generate_verbose_message(stats)
print(message)
message = generate_simple_message(stats)
print(message)
save_glucose_data(stats)
set_range("mgdl", 70, 180)
set_range("mmol", 4, 10)
get_graph(glucose_readings, low_mgdl=70, high_mgdl=180, output_path="glucose_plot.png")
set_range("mgdl", 70, 180)

