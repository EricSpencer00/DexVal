#stat_functions.py
import statistics
import logging
import matplotlib.pyplot as plt
from typing import List
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

current_glucose_mgdl = None
current_glucose_mmol = None
time_of_reading = None
glucose_state = None
average_glucose_mgdl = None
average_glucose_mmol = None
estimated_a1c = None
time_in_range_percentage = None
median_glucose_mgdl = None
median_glucose_mmol = None
stdev_glucose_mgdl = None
stdev_glucose_mmol = None
high_mgdl = 180 # Default high glucose level
low_mgdl = 70 # Default low glucose level
high_mmol = 8.3 # Default high glucose level
low_mmol = 3.9 # Default low glucose level
min_glucose_mgdl = None
min_glucose_mmol = None
max_glucose_mgdl = None
max_glucose_mmol = None
glucose_range_mgdl = None
glucose_range_mmol = None
coef_variation_percentage = None
glycemic_variability_index = None

def update_value(variable_name, new_value):
    globals()[variable_name] = new_value

def set_high_mgdl(dexcom, value):
    global high_mgdl
    high_mgdl = value

def set_low_mgdl(dexcom, value):
    global low_mgdl
    low_mgdl = value

def set_high_mmol(dexcom, value):
    global high_mmol
    high_mmol = value

def set_low_mmol(dexcom, value):
    global low_mmol
    low_mmol = value

def get_current_trend_arrow(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    trend_arrow = glucose_reading.trend_arrow
    return trend_arrow

def get_current_trend_description(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    trend_description = glucose_reading.trend_description
    return trend_description

def get_current_value_mdgl(dexcom):
    try:
        glucose_reading = dexcom.get_current_glucose_reading()
        if not glucose_reading:
            logging.error("Failed to get glucose reading.")
            return None
        
        glucose_value = glucose_reading.value
        logging.debug(f"Glucose reading value: {glucose_value}")
        return glucose_value
    except Exception as e:
        logging.error(f"An error occurred while getting current glucose value: {e}")
        return None

def get_current_value_mmol(dexcom):
    try:
        glucose_reading = dexcom.get_current_glucose_reading()
        if glucose_reading is None:
            logging.error("Failed to get glucose reading.")
            return None
        
        glucose_value = glucose_reading.mmol
        logging.debug(f"Glucose reading value (mmol/L): {glucose_value}")
        return glucose_value
    except Exception as e:
        logging.error(f"An error occurred while getting current glucose value (mmol/L): {e}")
        return None

def get_glucose_graph(dexcom):
    glucose_graph = dexcom.get_glucose_readings(minutes=1440, max_count=288)
    return glucose_graph

def get_glucose_values(dexcom):
    glucose_graph = get_glucose_graph(dexcom)
    glucose_values = [reading.value for reading in glucose_graph]
    return glucose_values

def get_glucose_state_mdgl(dexcom):
    try:
        glucose_value = get_current_value_mdgl(dexcom)
        if glucose_value is None:
            return "Unknown"
        
        if glucose_value < low_mgdl:
            return "Low"
        elif glucose_value > high_mgdl:
            return "High"
        else:
            return "In Range"
    except Exception as e:
        logging.error(f"An error occurred while determining glucose state (mg/dL): {e}")
        return "Unknown"

def get_glucose_state_mmol(dexcom):
    try:
        glucose_value = get_current_value_mmol(dexcom)
        if glucose_value is None:
            return "Unknown"
        
        if glucose_value < low_mmol:
            return "Low"
        elif glucose_value > high_mmol:
            return "High"
        else:
            return "In Range"
    except Exception as e:
        logging.error(f"An error occurred while determining glucose state (mmol/L): {e}")
        return "Unknown"

def get_average_glucose_mgdl(dexcom):
    glucose_values = get_glucose_values(dexcom)
    return round(statistics.mean(glucose_values), 4)

def get_average_glucose_mmol(dexcom):
    average_glucose_mgdl = get_average_glucose_mgdl(dexcom)
    return round(average_glucose_mgdl / 18.01559, 4)

def get_median_glucose_mgdl(dexcom):
    glucose_values = get_glucose_values(dexcom)
    return round(statistics.median(glucose_values), 4)

def get_median_glucose_mmol(dexcom):
    median_glucose_mgdl = get_median_glucose_mgdl(dexcom)
    return round(median_glucose_mgdl / 18.01559, 4)

def get_stdev_glucose_mgdl(dexcom):
    glucose_values = get_glucose_values(dexcom)
    return round(statistics.stdev(glucose_values), 4)

def get_stdev_glucose_mmol(dexcom):
    stdev_glucose_mgdl = get_stdev_glucose_mgdl(dexcom)
    return round(stdev_glucose_mgdl / 18.01559, 4)

def get_min_glucose_mgdl(dexcom):
    glucose_values = get_glucose_values(dexcom)
    return min(glucose_values)

def get_min_glucose_mmol(dexcom):
    min_glucose_mgdl = get_min_glucose_mgdl(dexcom)
    return round(min_glucose_mgdl / 18.01559, 4)

def get_max_glucose_mgdl(dexcom):
    glucose_values = get_glucose_values(dexcom)
    return max(glucose_values)

def get_max_glucose_mmol(dexcom):
    max_glucose_mgdl = get_max_glucose_mgdl(dexcom)
    return round(max_glucose_mgdl / 18.01559, 4)

def get_glucose_range_mgdl(dexcom):
    min_glucose_mgdl = get_min_glucose_mgdl(dexcom)
    max_glucose_mgdl = get_max_glucose_mgdl(dexcom)
    return int((max_glucose_mgdl - min_glucose_mgdl) * 100) / 100

def get_glucose_range_mmol(dexcom):
    glucose_range_mgdl = get_glucose_range_mgdl(dexcom)
    return round(glucose_range_mgdl / 18.01559, 4)

def get_coef_variation_percentage(dexcom):
    stdev_glucose_mgdl = get_stdev_glucose_mgdl(dexcom) # it does not matter if you use mmol/L or md/gL here
    average_glucose_mgdl = get_average_glucose_mgdl(dexcom)
    return round((stdev_glucose_mgdl / average_glucose_mgdl) * 100, 4)

def get_glycemic_variability_index(dexcom):
    glucose_values = get_glucose_values(dexcom)
    average_glucose_mgdl = statistics.mean(glucose_values) # it does not matter if you use mmol/L or md/gL here
    stdev_glucose_mgdl = statistics.stdev(glucose_values)

    glycemic_variability_index = (stdev_glucose_mgdl / average_glucose_mgdl) * 100

    return glycemic_variability_index

def get_estimated_a1c(dexcom):
    average_glucose_mdgl = get_average_glucose_mgdl(dexcom)
    estimated_a1c = (average_glucose_mdgl + 46.7) / 28.7
    round(estimated_a1c, 4)
    return estimated_a1c

def verbose_message_mgdl(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading() # get_current_value_mgdl
    glucose_value = glucose_reading.value
    trend_arrow = glucose_reading.trend_arrow # get_current_trend
    glucose_graph = dexcom.get_glucose_readings(minutes=1440, max_count=288) # glucose graph
    glucose_values = [reading.value for reading in glucose_graph] # get_glucose_values

    glucose_state = "Low" if glucose_value < low_mgdl else "High" if glucose_value > high_mgdl else "In Range" # get_glucose_state_mdgl

    average_glucose_mgdl = round(statistics.mean(glucose_values), 4)
    median_glucose_mgdl = round(statistics.median(glucose_values), 4)
    stdev_glucose_mgdl = round(statistics.stdev(glucose_values), 4)
    min_glucose_mgdl = min(glucose_values)
    max_glucose_mgdl = max(glucose_values)
    glucose_range_mgdl = int((max_glucose_mgdl - min_glucose_mgdl) * 100) / 100

    in_range_glucose = [g for g in glucose_values if low_mgdl <= g <= high_mgdl]
    time_in_range_percentage = round((len(in_range_glucose) / len(glucose_values)) * 100, 4)

    mgdl_above_high = sum(reading - high_mgdl for reading in glucose_values if reading > high_mgdl)
    mgdl_below_low = sum(low_mgdl - reading for reading in glucose_values if reading < low_mgdl)
    total_area = (max_glucose_mgdl - high_mgdl) * time_in_range_percentage / 100 + mgdl_above_high + mgdl_below_low
    glycemic_variability_index = ((mgdl_above_high + mgdl_below_low) / total_area) * 100

    average_glucose_mmol = round(average_glucose_mgdl / 18.01559, 4)
    estimated_a1c = round((28.7 * average_glucose_mmol + 46.7) / 28.7, 4)

    message_body = f"Your current glucose level is {glucose_value} mg/dL ({glucose_reading.trend_description} {trend_arrow})\n" \
                   f"Time of reading: {glucose_reading.datetime}\n" \
                   f"Glucose state: {glucose_state}\n" \
                   f"Average glucose level: {average_glucose_mgdl} mg/dL\n" \
                   f"Estimated A1C: {estimated_a1c}\n" \
                   f"Time in Range ({low_mgdl}-{high_mgdl} mg/dL): {time_in_range_percentage:.2f}%\n" \
                   f"Median Glucose: {median_glucose_mgdl} mg/dL\n" \
                   f"Standard Deviation: {stdev_glucose_mgdl} mg/dL\n" \
                   f"Minimum Glucose: {min_glucose_mgdl} mg/dL\n" \
                   f"Maximum Glucose: {max_glucose_mgdl} mg/dL\n" \
                   f"Glucose Range: {glucose_range_mgdl} mg/dL\n" \
                   f"Coef. of Variation: {round((stdev_glucose_mgdl / average_glucose_mgdl) * 100, 4)}%\n" \
                   f"Glycemic Variability Index: {glycemic_variability_index}%" \
                   f"Time in Range ({low_mgdl}-{high_mgdl} mg/dL): {time_in_range_percentage:.2f}%\n"

    return message_body

def verbose_message_mmol(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    glucose_value = glucose_reading.value
    trend_arrow = glucose_reading.trend_arrow
    glucose_graph = dexcom.get_glucose_readings(minutes=1440, max_count=288)
    glucose_values = [reading.value for reading in glucose_graph]

    glucose_values_mmol = [round(value / 18.01559, 1) for value in glucose_values]
    glucose_value_mmol = round(glucose_value / 18.01559, 1)

    glucose_state = "Low" if glucose_value_mmol < low_mmol else "High" if glucose_value_mmol > high_mmol else "In Range"

    average_glucose_mmol = round(statistics.mean(glucose_values_mmol), 1)
    median_glucose_mmol = round(statistics.median(glucose_values_mmol), 1)
    stdev_glucose_mmol = round(statistics.stdev(glucose_values_mmol), 1)
    min_glucose_mmol = min(glucose_values_mmol)
    max_glucose_mmol = max(glucose_values_mmol)
    glucose_range_mmol = int((max_glucose_mmol - min_glucose_mmol) * 100) / 100

    in_range_glucose = [g for g in glucose_values_mmol if 3.9 <= g <= 8.3]
    time_in_range_percentage = round((len(in_range_glucose) / len(glucose_values_mmol)) * 100, 1)

    mmol_above_high = sum(reading - high_mmol / 18.01559 for reading in glucose_values_mmol if reading > high_mmol)
    mmol_below_low = sum(low_mmol - reading for reading in glucose_values_mmol if reading < low_mmol)
    total_area = (max_glucose_mmol - high_mmol) * time_in_range_percentage / 100 + mmol_above_high + mmol_below_low
    glycemic_variability_index = ((mmol_above_high + mmol_below_low) / total_area) * 100

    # Use ADAG formula to estimate A1C
    estimated_a1c = round((28.7 * average_glucose_mmol + 46.7) / 28.7, 1)

    message_body = f"Your current glucose level is {glucose_value_mmol} mmol/L ({glucose_reading.trend_description} {trend_arrow})\n" \
                   f"Time of reading: {glucose_reading.datetime}\n" \
                   f"Glucose state: {glucose_state}\n" \
                   f"Average glucose level: {average_glucose_mmol} mmol/L\n" \
                   f"Estimated A1C: {estimated_a1c}\n" \
                   f"Time in Range ({low_mmol}-{high_mmol} mmol/L): {time_in_range_percentage:.1f}%\n" \
                   f"Median Glucose: {median_glucose_mmol} mmol/L\n" \
                   f"Standard Deviation: {stdev_glucose_mmol} mmol/L\n" \
                   f"Minimum Glucose: {min_glucose_mmol} mmol/L\n" \
                   f"Maximum Glucose: {max_glucose_mmol} mmol/L\n" \
                   f"Glucose Range: {glucose_range_mmol} mmol/L\n" \
                   f"Coef. of Variation: {round((stdev_glucose_mmol / average_glucose_mmol) * 100, 1)}%\n" \
                   f"Glycemic Variability Index: {glycemic_variability_index}%" \
                   f"Time in Range ({low_mmol}-{high_mmol} mmol/L): {time_in_range_percentage:.1f}%\n"

    return message_body

def concise_message_mdgl(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    trend = glucose_reading.trend_description
    return f"{glucose_reading} and {trend}" 

def concise_message_mmol(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    glucose_reading_mmol = round(glucose_reading.value / 18.01559, 1)
    trend = glucose_reading.trend_description
    return f"{glucose_reading_mmol} mmol/L and {trend}"

def generate_bit_board(dexcom, height=5, width=20):
    # Normalize values to fit within the height of the bit board
    values = dexcom.get_glucose_readings(minutes=1440, max_count=width)
    values = [reading.value for reading in values]

    max_value = max(values) if values else 1
    min_value = min(values) if values else 0
    value_range = max_value - min_value if max_value != min_value else 1
    normalized_values = [(v - min_value) / value_range * (height - 1) for v in values]
    
    # Create an empty board
    board = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Place 'x' on the board according to normalized values
    for i, value in enumerate(normalized_values):
        if i < width:
            row = height - 1 - int(value)
            board[row][i] = 'x'
    
    # Print the board
    for row in board:
        print(''.join(row))

def generate_glucose_graph(dexcom, output_path='static/dexcom_glucose_graph.png'):
    glucose_graph: List = dexcom.get_glucose_readings(minutes=1440, max_count=288)
    glucose_values = [reading.value for reading in glucose_graph]
    timestamps = [reading.datetime for reading in glucose_graph]
    trend_arrows = [reading.trend_arrow for reading in glucose_graph]

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, glucose_values, color='black', linewidth=1)

    low_glucose = [idx for idx, reading in enumerate(glucose_values) if reading < 70]
    in_range_glucose = [idx for idx, reading in enumerate(glucose_values) if 70 <= reading <= 150]
    high_glucose = [idx for idx, reading in enumerate(glucose_values) if reading > 150]

    if low_glucose:
        plt.axhline(y=min(glucose_values), color='red', linestyle='--', linewidth=1, alpha=0.5, xmin=min(low_glucose)/len(glucose_values), xmax=max(low_glucose)/len(glucose_values))
    if high_glucose:
        plt.axhline(y=max(glucose_values), color='red', linestyle='--', linewidth=1, alpha=0.5, xmin=min(high_glucose)/len(glucose_values), xmax=max(high_glucose)/len(glucose_values))
    if in_range_glucose:
        plt.axhline(y=70, color='green', linestyle='--', linewidth=1, alpha=0.5, xmin=min(in_range_glucose)/len(glucose_values), xmax=max(in_range_glucose)/len(glucose_values))
        plt.axhline(y=150, color='green', linestyle='--', linewidth=1, alpha=0.5, xmin=min(in_range_glucose)/len(glucose_values), xmax=max(in_range_glucose)/len(glucose_values))

    for i, arrow in enumerate(trend_arrows):
        if arrow == "↑":
            plt.scatter(timestamps[i], glucose_values[i], color='green', marker='^', s=50)
        elif arrow == "↓":
            plt.scatter(timestamps[i], glucose_values[i], color='red', marker='v', s=50)
        else:
            plt.scatter(timestamps[i], glucose_values[i], color='orange', marker='o', s=50)

    plt.title('Dexcom Glucose Readings Over the Past Day')
    plt.xlabel('Time (Day / Hour)')
    plt.ylabel('Glucose Level (mg/dL)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()