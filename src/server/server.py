from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pickle as p
import json
import sys
import os

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(dir,'..','predictor'))

import heart

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    result = heart.predict(data)
    return jsonify(result.tolist())

if __name__ == '__main__':
    model = heart.train_model()
    app.run(debug=True, host='0.0.0.0')