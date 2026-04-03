# 🏢 Smart Building Digital Twin

A fully functional Digital Twin platform simulating real-time IoT sensor data 
from a commercial building, with ML-powered anomaly detection, predictive 
maintenance risk scoring, and a live operational dashboard.

Built as a portfolio project targeting the SOLIS Group KTP Associate role 
(Smart Buildings R&D Engineer).

---

## 🏗️ Architecture
```
IoT Sensor Layer → Data Pipeline (SQLite) → ML Models → Streamlit Dashboard
```

---

## 🔧 Components

### 1. Simulated IoT Data Pipeline (`sensor_simulator.py`)
- Simulates 5 building zones: Floor 1, Floor 2, Server Room, Lobby, Canteen
- Generates real-time sensor readings: temperature, humidity, energy (kWh), occupancy
- Injects realistic anomalies (5% rate) — temperature spikes, energy surges
- Streams data into a SQLite database mimicking a live BMS data feed

### 2. Predictive Maintenance Models (`train_model.py`)
- **Isolation Forest** — unsupervised anomaly detection across all sensor streams
- **Random Forest Classifier** — supervised failure prediction using labelled anomaly data
- Models saved as `.pkl` files for reuse in the dashboard

### 3. Live Operational Dashboard (`dashboard.py`)
- Built with Streamlit
- Shows live sensor readings per zone with health status indicators
- Zone-level trend analysis for temperature and energy usage
- Anomaly log with timestamps and affected zones
- Risk scoring per zone using the trained Random Forest model

---

## 💻 Tech Stack

- **Python** — core language
- **SQLite** — lightweight real-time data storage
- **Scikit-learn** — Isolation Forest, Random Forest
- **Streamlit** — interactive dashboard
- **Pandas / NumPy / Matplotlib** — data processing and visualisation

---

## 🚀 Getting Started
```bash
# 1. Clone the repo
git clone https://github.com/Nivedita-Saha/smart-building-digital-twin.git
cd smart-building-digital-twin

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate sensor data
python3 sensor_simulator.py

# 5. Train ML models
python3 train_model.py

# 6. Launch dashboard
streamlit run dashboard.py
```

---

## 📊 Sample Output

- 500 sensor readings across 5 zones
- ~25 anomalies detected (5% contamination rate)
- 100% classification accuracy on labelled anomaly data
- Live dashboard refresh showing zone health, trends, and risk scores

---

## 🔗 Relevance to Industry

This project demonstrates core competencies required for Digital Twin 
engineering in smart buildings and facilities management:

- IoT data ingestion and pipeline design
- Supervised and unsupervised ML for predictive maintenance
- Real-time operational dashboarding
- Scalable architecture applicable to multi-site deployments

---

## 👩‍💻 Author

**Nivedita Saha**  
MSc Artificial Intelligence and Data Science (Distinction) — Keele University  
[Portfolio](https://www.nivsaha.com) | [GitHub](https://github.com/Nivedita-Saha) | [LinkedIn](https://www.linkedin.com/in/nivedita-saha-2833182a6)