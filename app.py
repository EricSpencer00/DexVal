from flask import Flask, render_template, request, jsonify
from DexcomAPI import defs, stat_functions as stats

app = Flask(__name__, template_folder='DexcomAPI')

# Initialize Dexcom object with appropriate credentials
dexcom = defs.get_dexcom_connection()

@app.route('/')
def index():
    # Get current glucose data
    current_glucose_mgdl = stats.get_current_value_mdgl(dexcom) or 'N/A'
    current_glucose_mmol = stats.get_current_value_mmol(dexcom) or 'N/A'
    glucose_state_mdgl = stats.get_glucose_state_mdgl(dexcom) or 'N/A'
    glucose_state_mmol = stats.get_glucose_state_mmol(dexcom) or 'N/A'
    average_glucose_mgdl = stats.get_average_glucose_mgdl(dexcom) or 'N/A'
    average_glucose_mmol = stats.get_average_glucose_mmol(dexcom) or 'N/A'
    median_glucose_mgdl = stats.get_median_glucose_mgdl(dexcom) or 'N/A'
    median_glucose_mmol = stats.get_median_glucose_mmol(dexcom) or 'N/A'
    stdev_glucose_mgdl = stats.get_stdev_glucose_mgdl(dexcom) or 'N/A'
    stdev_glucose_mmol = stats.get_stdev_glucose_mmol(dexcom) or 'N/A'
    min_glucose_mgdl = stats.get_min_glucose_mgdl(dexcom) or 'N/A'
    min_glucose_mmol = stats.get_min_glucose_mmol(dexcom) or 'N/A'
    max_glucose_mgdl = stats.get_max_glucose_mgdl(dexcom) or 'N/A'
    max_glucose_mmol = stats.get_max_glucose_mmol(dexcom) or 'N/A'
    glucose_range_mgdl = stats.get_glucose_range_mgdl(dexcom) or 'N/A'
    glucose_range_mmol = stats.get_glucose_range_mmol(dexcom) or 'N/A'
    coef_variation_percentage = stats.get_coef_variation_percentage(dexcom) or 'N/A'
    glycemic_variability_index = stats.get_glycemic_variability_index(dexcom) or 'N/A'
    estimated_a1c = stats.get_estimated_a1c(dexcom) or 'N/A'
    time_in_range_percentage = stats.time_in_range_percentage or 'N/A' 

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

@app.route('/update_global_mdgl_range', methods=['POST'])
def update_mdgl():
    data = request.json
    stats.high_mgdl = data['high_mgdl']
    stats.low_mgdl = data['low_mgdl']
    return jsonify({"message": "mdgl value(s) updated successfully"}), 200

@app.route('/update_global_mmol_range', methods=['POST'])
def update_mmol():
    data = request.json
    stats.high_mmol = data['high_mmol']
    stats.low_mmol = data['low_mmol']
    return jsonify({"message": "mmol value(s) updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
