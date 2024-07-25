from flask import Flask
from flask import render_template
import DexcomAPI.stat_functions as stats
from DexcomAPI.defs import get_dexcom_connection
from pydexcom import Dexcom

app = Flask(__name__)

# Initialize Dexcom object with appropriate credentials
dexcom = get_dexcom_connection()

@app.route('/')
def index():
    # Get current glucose data
    current_glucose_mgdl = stats.get_current_value_mdgl(dexcom)
    current_glucose_mmol = stats.get_current_value_mmol(dexcom)
    glucose_state_mdgl = stats.get_glucose_state_mdgl(dexcom)
    glucose_state_mmol = stats.get_glucose_state_mmol(dexcom)
    average_glucose_mgdl = stats.get_average_glucose_mgdl(dexcom)
    average_glucose_mmol = stats.get_average_glucose_mmol(dexcom)
    median_glucose_mgdl = stats.get_median_glucose_mgdl(dexcom)
    median_glucose_mmol = stats.get_median_glucose_mmol(dexcom)
    stdev_glucose_mgdl = stats.get_stdev_glucose_mgdl(dexcom)
    stdev_glucose_mmol = stats.get_stdev_glucose_mmol(dexcom)
    min_glucose_mgdl = stats.get_min_glucose_mgdl(dexcom)
    min_glucose_mmol = stats.get_min_glucose_mmol(dexcom)
    max_glucose_mgdl = stats.get_max_glucose_mgdl(dexcom)
    max_glucose_mmol = stats.get_max_glucose_mmol(dexcom)
    glucose_range_mgdl = stats.get_glucose_range_mgdl(dexcom)
    glucose_range_mmol = stats.get_glucose_range_mmol(dexcom)
    coef_variation_percentage = stats.get_coef_variation_percentage(dexcom)
    glycemic_variability_index = stats.get_glycemic_variability_index(dexcom)
    estimated_a1c = stats.get_estimated_a1c(dexcom)
    time_in_range_percentage = stats.time_in_range_percentage

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

if __name__ == '__main__':
    app.run(debug=True)
