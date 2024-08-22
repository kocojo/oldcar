from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from joblib import load
import sqlite3
import pandas as pd
import numpy as np
app = Flask(__name__)
conn = sqlite3.connect('car.db')
data = pd.read_sql_query("SELECT * FROM data_of_car", conn)
suggestions1 = data['Name'].tolist()
app.secret_key = '231216546541621'
@app.route('/')
def index():
    return render_template('index.html')

# API gợi ý tìm kiếm cho thanh tìm kiếm 1
@app.route('/suggest1', methods=['GET'])
def suggest1():
    query = request.args.get('query', '').lower()
    filtered_suggestions = [s for s in suggestions1 if query in s.lower()]
    return jsonify(filtered_suggestions)
@app.route('/submit', methods=['POST'])
def print_output():
    data1 = request.form.to_dict()
    name = data1['name']
    try:
        year = int(data1['year'])
    except:
        flash('Wrong Input')
        return redirect(url_for('index'))
    try:
        km = int(data1['km'])
    except:
        flash('Wrong Input')
        return redirect(url_for('index'))
    map = {'First':1, 'Second':2, 'Third':3, 'Other':4}
    Owner_Type = map[data1['Owner_Type']]
    input = data.query(f"Name =='{name}' ").iloc[0]
    ordinal_mapping = {
        'Petrol': 1,
        'Diesel': 2,
        'LPG': 3,
        'CNG': 4,
    }
    input['Fuel_Type'] = ordinal_mapping[input['Fuel_Type']]
    ordinal_mapping = {
        'Manual': 1,
        'Automatic': 2,
    }
    input['Transmission'] = ordinal_mapping[input['Transmission']]
    x = np.array([[year], [km], [input['Fuel_Type']], [input['price_per_km']], [input['Transmission']], [Owner_Type],
                  [input['EngineCC']], [input['PowerPHP']], [input['Seats']]])
    loaded_model = load('forest_model.joblib')
    predictions = loaded_model.predict(x.T)
    predictions = predictions[0] * 0.012
    return render_template('index.html',results=str(predictions))
@app.route('/index1')
def new():
    return render_template('index1.html')
@app.route('/submit1', methods=['POST'])
def print_output1():
    data1 = request.form.to_dict()
    name = data1['name']
    try:
        year = int(data1['year'])
    except:
        flash('Wrong Input')
        return redirect(url_for('index'))
    try:
        km = int(data1['km'])
    except:
        flash('Wrong Input')
        return redirect(url_for('index'))
    map = {'First':1, 'Second':2, 'Third':3, 'Other':4}
    Owner_Type = map[data1['Owner_Type']]
    ordinal_mapping = {
        'Petrol': 1,
        'Diesel': 2,
        'LPG': 3,
        'CNG': 4,
    }
    data1['Fuel_Type'] = ordinal_mapping[data1['Fuel_Type']]
    ordinal_mapping = {
        'Manual': 1,
        'Automatic': 2,
    }
    data1['Transmission'] = ordinal_mapping[data1['Transmission']]
    try:
        x = np.array([[year], [km], [float(data1['Fuel_Type'])], [float(data1['price_per_km'])], [float(data1['Transmission'])], [Owner_Type],
                      [float(data1['EngineCC'])], [float(data1['PowerPHP'])], [float(data1['Seats'])]])
    except:
        flash('Wrong Input')
        return redirect(url_for('index'))
    loaded_model = load('forest_model.joblib')
    predictions = loaded_model.predict(x.T)
    predictions = predictions[0] * 0.012
    return render_template('index1.html',results=str(predictions))
if __name__ == "__main__":
    app.run(debug=True)
