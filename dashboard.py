import streamlit as st
import sqlite3
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(
    page_title="Smart Building Digital Twin",
    page_icon="🏢",
    layout="wide"
)

def load_data():
    conn = sqlite3.connect("building_twin.db")
    df = pd.read_sql_query(
        "SELECT * FROM sensor_readings ORDER BY timestamp DESC",
        conn
    )
    conn.close()
    return df

def load_models():
    with open("isolation_forest.pkl", "rb") as f:
        iso_model = pickle.load(f)
    with open("random_forest.pkl", "rb") as f:
        rf_model = pickle.load(f)
    return iso_model, rf_model

def get_risk_score(model, row):
    features = [[row["temperature"], row["humidity"],
                 row["energy_kwh"], row["occupancy"]]]
    prob = model.predict_proba(features)[0][1]
    return round(prob * 100, 1)

# ── Header ──
st.title("🏢 Smart Building Digital Twin")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")

# ── Load data and models ──
df = load_data()
iso_model, rf_model = load_models()

ZONES = ["Floor_1", "Floor_2", "Server_Room", "Lobby", "Canteen"]

# ── Latest readings per zone ──
st.subheader("📡 Live Sensor Readings")
latest = df.groupby("zone").first().reset_index()

cols = st.columns(len(ZONES))
for i, zone in enumerate(ZONES):
    row = latest[latest["zone"] == zone].iloc[0]
    risk = get_risk_score(rf_model, row)
    flag = "🔴" if row["anomaly_flag"] == 1 else "🟢"
    with cols[i]:
        st.metric(label=f"{flag} {zone.replace('_', ' ')}",
                  value=f"{row['temperature']}°C",
                  delta=f"Energy: {row['energy_kwh']} kWh")
        st.caption(f"Humidity: {row['humidity']}%")
        st.caption(f"Occupancy: {row['occupancy']}")
        st.caption(f"Risk Score: {risk}%")

st.markdown("---")

# ── Zone selector for charts ──
st.subheader("📈 Zone Trend Analysis")
selected_zone = st.selectbox("Select Zone", ZONES)
zone_df = df[df["zone"] == selected_zone].sort_values("timestamp").tail(100)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(zone_df["timestamp"], zone_df["temperature"],
            color="tomato", linewidth=1.5)
    ax.set_title(f"Temperature — {selected_zone.replace('_', ' ')}")
    ax.set_ylabel("°C")
    plt.xticks(rotation=45, fontsize=6)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(zone_df["timestamp"], zone_df["energy_kwh"],
            color="steelblue", linewidth=1.5)
    ax.set_title(f"Energy Usage — {selected_zone.replace('_', ' ')}")
    ax.set_ylabel("kWh")
    plt.xticks(rotation=45, fontsize=6)
    plt.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# ── Anomaly log ──
st.subheader("⚠️ Anomaly Log")
anomalies = df[df["anomaly_flag"] == 1][
    ["timestamp", "zone", "temperature", "energy_kwh", "occupancy"]
].head(20)

if anomalies.empty:
    st.success("No anomalies detected.")
else:
    st.dataframe(anomalies, use_container_width=True)

st.markdown("---")

# ── Raw data explorer ──
st.subheader("🗄️ Raw Sensor Data")
st.dataframe(df.head(50), use_container_width=True)