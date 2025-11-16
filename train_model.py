
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def generate_synthetic(n=2000, random_state=42):
    rng = np.random.RandomState(random_state)
    # features: temperature (C), humidity (%), pressure (hPa), wind_speed (m/s)
    temperature = rng.normal(loc=15, scale=10, size=n)   # -10 .. 40 roughly
    humidity = rng.uniform(10, 100, size=n)
    pressure = rng.normal(loc=1013, scale=8, size=n)
    wind_speed = rng.exponential(scale=2.0, size=n)

    X = pd.DataFrame({
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'wind_speed': wind_speed
    })

    # create multi-labels with simple rules + noise
    # sunny: high temp, low humidity, low clouds (simulate)
    sunny = (temperature > 20) & (humidity < 60) & (wind_speed < 6)
    # rainy: high humidity and moderate/low pressure
    rainy = (humidity > 75) & (pressure < 1016)
    # windy: high wind_speed
    windy = wind_speed > 6.0
    # cloudy: moderate humidity and not sunny
    cloudy = (humidity >= 40) & (humidity <= 90) & (~sunny)

    # add randomness
    flip = rng.rand(n)
    sunny = np.where(flip < 0.02, ~sunny, sunny)
    rainy = np.where(flip < 0.01, ~rainy, rainy)
    windy = np.where(flip < 0.01, ~windy, windy)
    cloudy = np.where(flip < 0.03, ~cloudy, cloudy)

    y = pd.DataFrame({
        'sunny': sunny.astype(int),
        'rainy': rainy.astype(int),
        'windy': windy.astype(int),
        'cloudy': cloudy.astype(int)
    })

    return X, y

def train_and_save(out_dir='.', random_state=42):
    X, y = generate_synthetic(n=2500, random_state=random_state)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    clf = OneVsRestClassifier(LogisticRegression(solver='liblinear', max_iter=200))
    clf.fit(X_train_s, y_train)

    # evaluate
    preds = clf.predict(X_test_s)
    print("Classification report on test set:")
    print(classification_report(y_test, preds, target_names=y.columns))

    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(clf, os.path.join(out_dir, 'model.pkl'))
    joblib.dump(scaler, os.path.join(out_dir, 'scaler.pkl'))
    print(f"Saved model and scaler to {out_dir}")

if __name__ == '__main__':
    train_and_save(out_dir=os.path.join(os.path.dirname(__file__), '.'))
