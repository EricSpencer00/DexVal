import statistics

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
high_mgdl = None
low_mgdl = None
high_mmol = None
low_mmol = None
min_glucose_mgdl = None
min_glucose_mmol = None
max_glucose_mgdl = None
max_glucose_mmol = None
glucose_range_mgdl = None
glucose_range_mmol = None
coef_variation_percentage = None
glycemic_variability_index = None

def set_high_mgdl(dexcom):
    global high_mgdl
    high_mgdl = 180

def set_low_mgdl(dexcom):
    global low_mgdl
    low_mgdl = 70

def set_high_mmol(dexcom):
    global high_mmol
    high_mmol = 8.3

def set_low_mmol(dexcom):
    global low_mmol
    low_mmol = 3.9

def get_current_trend_arrow(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    trend_arrow = glucose_reading.trend_arrow
    return trend_arrow

def get_current_trend_description(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    trend_description = glucose_reading.trend_description
    return trend_description

def get_current_value_mdgl(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    glucose_value = glucose_reading.value
    return glucose_value

def get_current_value_mmol(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    glucose_value = glucose_reading.mmol
    return glucose_value

def get_glucose_graph(dexcom):
    glucose_graph = dexcom.get_glucose_readings(minutes=1440, max_count=288)
    return glucose_graph

def get_glucose_values(dexcom):
    glucose_graph = get_glucose_graph(dexcom)
    glucose_values = [reading.value for reading in glucose_graph]
    return glucose_values

def get_glucose_state_mdgl(dexcom):
    glucose_value = get_current_value_mdgl(dexcom)
    glucose_state = "Low" if glucose_value < low_mgdl else "High" if glucose_value > high_mgdl else "In Range"
    return glucose_state

def get_glucose_state_mmol(dexcom):
    glucose_value = get_current_value_mmol(dexcom)
    glucose_state = "Low" if glucose_value < low_mmol else "High" if glucose_value > high_mmol else "In Range"
    return glucose_state

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
    average_glucose_mmol = get_average_glucose_mmol(dexcom)
    return round((28.7 * average_glucose_mmol + 46.7) / 28.7, 4)

def verbose_message_mgdl(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading() # get_current_value_mgdl
    glucose_value = glucose_reading.value
    trend_arrow = glucose_reading.trend_arrow # get_current_trend
    glucose_graph = dexcom.get_glucose_readings(minutes=1440, max_count=288) # glucose graph
    glucose_values = [reading.value for reading in glucose_graph] # get_glucose_values

    glucose_state = "Low" if glucose_value < 70 else "High" if glucose_value > 150 else "In Range" # get_glucose_state_mdgl

    average_glucose_mgdl = round(statistics.mean(glucose_values), 4)
    median_glucose_mgdl = round(statistics.median(glucose_values), 4)
    stdev_glucose_mgdl = round(statistics.stdev(glucose_values), 4)
    min_glucose_mgdl = min(glucose_values)
    max_glucose_mgdl = max(glucose_values)
    glucose_range_mgdl = int((max_glucose_mgdl - min_glucose_mgdl) * 100) / 100

    in_range_glucose = [g for g in glucose_values if 70 <= g <= 150]
    time_in_range_percentage = round((len(in_range_glucose) / len(glucose_values)) * 100, 4)

    mgdl_above_180 = sum(reading - 180 for reading in glucose_values if reading > 180)
    mgdl_below_70 = sum(70 - reading for reading in glucose_values if reading < 70)
    total_area = (max_glucose_mgdl - 180) * time_in_range_percentage / 100 + mgdl_above_180 + mgdl_below_70
    glycemic_variability_index = ((mgdl_above_180 + mgdl_below_70) / total_area) * 100

    average_glucose_mmol = round(average_glucose_mgdl / 18.01559, 4)
    estimated_a1c = round((28.7 * average_glucose_mmol + 46.7) / 28.7, 4)

    message_body = f"Your current glucose level is {glucose_value} mg/dL ({glucose_reading.trend_description} {trend_arrow})\n" \
                   f"Time of reading: {glucose_reading.datetime}\n" \
                   f"Glucose state: {glucose_state}\n" \
                   f"Average glucose level: {average_glucose_mgdl} mg/dL\n" \
                   f"Estimated A1C: {estimated_a1c}\n" \
                   f"Time in Range (70-150 mg/dL): {time_in_range_percentage:.2f}%\n" \
                   f"Median Glucose: {median_glucose_mgdl} mg/dL\n" \
                   f"Standard Deviation: {stdev_glucose_mgdl} mg/dL\n" \
                   f"Minimum Glucose: {min_glucose_mgdl} mg/dL\n" \
                   f"Maximum Glucose: {max_glucose_mgdl} mg/dL\n" \
                   f"Glucose Range: {glucose_range_mgdl} mg/dL\n" \
                   f"Coef. of Variation: {round((stdev_glucose_mgdl / average_glucose_mgdl) * 100, 4)}%\n" \
                   f"Glycemic Variability Index: {glycemic_variability_index}%"

    return message_body

def verbose_message_mmol(dexcom):
    glucose_reading = dexcom.get_current_glucose_reading()
    glucose_value = glucose_reading.value
    trend_arrow = glucose_reading.trend_arrow
    glucose_graph = dexcom.get_glucose_readings(minutes=1440, max_count=288)
    glucose_values = [reading.value for reading in glucose_graph]

    glucose_values_mmol = [round(value / 18.01559, 1) for value in glucose_values]
    glucose_value_mmol = round(glucose_value / 18.01559, 1)

    glucose_state = "Low" if glucose_value_mmol < 3.9 else "High" if glucose_value_mmol > 8.3 else "In Range"

    average_glucose_mmol = round(statistics.mean(glucose_values_mmol), 1)
    median_glucose_mmol = round(statistics.median(glucose_values_mmol), 1)
    stdev_glucose_mmol = round(statistics.stdev(glucose_values_mmol), 1)
    min_glucose_mmol = min(glucose_values_mmol)
    max_glucose_mmol = max(glucose_values_mmol)
    glucose_range_mmol = int((max_glucose_mmol - min_glucose_mmol) * 100) / 100

    in_range_glucose = [g for g in glucose_values_mmol if 3.9 <= g <= 8.3]
    time_in_range_percentage = round((len(in_range_glucose) / len(glucose_values_mmol)) * 100, 1)

    mgdl_above_180 = sum(reading - 180 / 18.01559 for reading in glucose_values_mmol if reading > 10)
    mgdl_below_70 = sum(10 - reading for reading in glucose_values_mmol if reading < 3.9)
    total_area = (max_glucose_mmol - 10) * time_in_range_percentage / 100 + mgdl_above_180 + mgdl_below_70
    glycemic_variability_index = ((mgdl_above_180 + mgdl_below_70) / total_area) * 100

    # Use ADAG formula to estimate A1C
    estimated_a1c = round((28.7 * average_glucose_mmol + 46.7) / 28.7, 1)

    message_body = f"Your current glucose level is {glucose_value_mmol} mmol/L ({glucose_reading.trend_description} {trend_arrow})\n" \
                   f"Time of reading: {glucose_reading.datetime}\n" \
                   f"Glucose state: {glucose_state}\n" \
                   f"Average glucose level: {average_glucose_mmol} mmol/L\n" \
                   f"Estimated A1C: {estimated_a1c}\n" \
                   f"Time in Range (3.9-8.3 mmol/L): {time_in_range_percentage:.1f}%\n" \
                   f"Median Glucose: {median_glucose_mmol} mmol/L\n" \
                   f"Standard Deviation: {stdev_glucose_mmol} mmol/L\n" \
                   f"Minimum Glucose: {min_glucose_mmol} mmol/L\n" \
                   f"Maximum Glucose: {max_glucose_mmol} mmol/L\n" \
                   f"Glucose Range: {glucose_range_mmol} mmol/L\n" \
                   f"Coef. of Variation: {round((stdev_glucose_mmol / average_glucose_mmol) * 100, 1)}%\n" \
                   f"Glycemic Variability Index: {glycemic_variability_index}%"

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