
from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

HERE = os.path.dirname(__file__)
model = joblib.load(os.path.join(HERE, 'model.pkl'))
scaler = joblib.load(os.path.join(HERE, 'scaler.pkl'))
labels = ['sunny', 'rainy', 'windy', 'cloudy']

app = Flask(__name__, static_folder=os.path.join(HERE, '..', 'frontend'), static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    try:
        temp = float(data.get('temperature'))
        humidity = float(data.get('humidity'))
        pressure = float(data.get('pressure'))
        wind_speed = float(data.get('wind_speed'))
    except Exception as e:
        return jsonify({'error': 'Invalid input. Ensure temperature, humidity, pressure, wind_speed are numbers.'}), 400

    X = np.array([[temp, humidity, pressure, wind_speed]])
    Xs = scaler.transform(X)
    probs = model.predict_proba(Xs)
    # predict_proba returns list per label; get probability of class 1 for each
    probs_pos = [p[0][1] if hasattr(p, '__len__') else p[:,1] for p in probs] if False else None
    # scikit-learn returns different shapes depending on estimator - safer to use predict_proba per estimator
    probs_pos = []
    for est in model.estimators_:
        p = est.predict_proba(Xs)
        probs_pos.append(float(p[0,1]))

    preds = (np.array(probs_pos) >= 0.5).astype(int).tolist()
    result = {label: {'pred': int(pred), 'prob': float(prob)} for label, pred, prob in zip(labels, preds, probs_pos)}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
