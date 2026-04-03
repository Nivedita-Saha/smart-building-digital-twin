import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

def load_data():
    """Load sensor readings from the database."""
    conn = sqlite3.connect("building_twin.db")
    df = pd.read_sql_query("SELECT * FROM sensor_readings", conn)
    conn.close()
    return df

def train_anomaly_detector(df):
    """Train Isolation Forest for unsupervised anomaly detection."""
    features = ["temperature", "humidity", "energy_kwh", "occupancy"]
    X = df[features]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,  # we expect ~5% anomalies
        random_state=42
    )
    model.fit(X)

    # -1 = anomaly, 1 = normal → convert to 0/1
    df["iso_prediction"] = model.predict(X)
    df["iso_prediction"] = df["iso_prediction"].map({1: 0, -1: 1})

    print("Isolation Forest training complete.")
    print(f"Anomalies detected: {df['iso_prediction'].sum()} out of {len(df)} readings")
    return model, df

def train_failure_predictor(df):
    """Train Random Forest using anomaly_flag as the target label."""
    features = ["temperature", "humidity", "energy_kwh", "occupancy"]
    X = df[features]
    y = df["anomaly_flag"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nRandom Forest Classification Report:")
    print(classification_report(y_test, y_pred))
    return model

def save_models(iso_model, rf_model):
    """Save both models to disk."""
    with open("isolation_forest.pkl", "wb") as f:
        pickle.dump(iso_model, f)
    with open("random_forest.pkl", "wb") as f:
        pickle.dump(rf_model, f)
    print("\nModels saved: isolation_forest.pkl, random_forest.pkl")

if __name__ == "__main__":
    print("Loading data from database...")
    df = load_data()
    print(f"Loaded {len(df)} readings\n")

    print("Training anomaly detector (Isolation Forest)...")
    iso_model, df = train_anomaly_detector(df)

    print("\nTraining failure predictor (Random Forest)...")
    rf_model = train_failure_predictor(df)

    save_models(iso_model, rf_model)
    print("\nAll done.")