import logging
import statistics
import defs

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
    """
    if current_reading is None or not glucose_readings:
        logging.error("Missing glucose data.")
        return {}

    glucose_values = [reading.value for reading in glucose_readings]
    glucose_stats = {
        "current_value": current_reading.value,
        "current_mmol": round(current_reading.value / 18.01559, 4),
        "current_trend_arrow": current_reading.trend_arrow,
        "average_mgdl": round(statistics.mean(glucose_values), 4),
        "average_mmol": round(statistics.mean(glucose_values) / 18.01559, 4),
        "median_mgdl": round(statistics.median(glucose_values), 4),
        "median_mmol": round(statistics.median(glucose_values) / 18.01559, 4),
        "stdev_mgdl": round(statistics.stdev(glucose_values), 4),
        "stdev_mmol": round(statistics.stdev(glucose_values) / 18.01559, 4),
        "min_mgdl": min(glucose_values),
        "min_mmol": round(min(glucose_values) / 18.01559, 4),
        "max_mgdl": max(glucose_values),
        "max_mmol": round(max(glucose_values) / 18.01559, 4),
        "time_in_range": round(len([g for g in glucose_values if defs.get_low_mgdl <= g <= defs.get_high_mgdl]) / len(glucose_values) * 100, 4),
        "glucose_range_mgdl": round(max(glucose_values) - min(glucose_values), 4),
        "glucose_range_mmol": round((max(glucose_values) - min(glucose_values)) / 18.01559, 4),
    }

    return glucose_stats

def generate_verbose_message(stats):
    """
    Generate a verbose message using precomputed statistics.
    """
    if not stats:
        return "Unable to generate glucose data message."

    message = (
        f"Current glucose: {stats['current_value']} mg/dL ({stats['current_trend_arrow']})\n"
        f"Average: {stats['average_mgdl']} mg/dL ({stats['average_mmol']} mmol/L)\n"
        f"Median: {stats['median_mgdl']} mg/dL ({stats['median_mmol']} mmol/L)\n"
        f"Min/Max: {stats['min_mgdl']} / {stats['max_mgdl']} mg/dL\n"
        f"Time in Range: {stats['time_in_range']}%\n"
        f"Glucose Range: {stats['glucose_range_mgdl']} mg/dL\n"
    )
    return message

#  write a main function



