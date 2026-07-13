import os
import pickle

import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'xgboost.sav')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler.sav')
FEATURE_FIELDS = [
    'ph value',
    'Hardness',
    'Solids',
    'Chloramines',
    'Sulfate',
    'Conductivity',
    'Organic carbon',
    'Trihalomethanes',
    'Turbidity',
]



def load_pickle(path):
    with open(path, 'rb') as file:
        return pickle.load(file)


model = load_pickle(MODEL_PATH)
scaler = load_pickle(SCALER_PATH)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        try:
            values = [float(request.form[field]) for field in FEATURE_FIELDS]
        except (KeyError, ValueError):
            return render_template(
                'index.html',
                error='Please enter valid numbers for every field.',
            )

        # create numpy array for all the inputs
        val = np.array(values)

        # transform the input data using pre fitted standard scaler
        data = scaler.transform([val])

        # make a prediction for the given data
        res = model.predict(data)[0]

        if res == 1:
            outcome = 'Potable'
        else:
            outcome = 'Not potable'
        return render_template('index.html', result=outcome)
    return render_template('index.html')

# run application
if __name__ == "__main__":
    app.run(debug=True)
