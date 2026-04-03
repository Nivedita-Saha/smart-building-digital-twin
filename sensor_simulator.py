import random
import sqlite3
import time
from datetime import datetime
import pandas as pd
import numpy as np

# Building zones
ZONES = ["Floor_1", "Floor_2", "Server_Room", "Lobby", "Canteen"]

# Normal ranges per zone
ZONE_PROFILES = {
    "Floor_1":     {"temp": (19, 23), "humidity": (40, 60), "energy": (2.0, 5.0), "occupancy": (0, 50)},
    "Floor_2":     {"temp": (19, 23), "humidity": (40, 60), "energy": (2.0, 5.0), "occupancy": (0, 40)},
    "Server_Room": {"temp": (16, 20), "humidity": (30, 50), "energy": (8.0, 15.0), "occupancy": (0, 5)},
    "Lobby":       {"temp": (18, 24), "humidity": (35, 55), "energy": (1.0, 3.0), "occupancy": (0, 30)},
    "Canteen":     {"temp": (20, 25), "humidity": (45, 65), "energy": (3.0, 8.0), "occupancy": (0, 60)},
}

def init_database():
    """Create SQLite database and sensor_readings table."""
    conn = sqlite3.connect("building_twin.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            zone TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            energy_kwh REAL,
            occupancy INTEGER,
            anomaly_flag INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialised: building_twin.db")

def generate_reading(zone, inject_anomaly=False):
    """Generate a single sensor reading for a zone."""
    profile = ZONE_PROFILES[zone]
    
    temp    = round(random.uniform(*profile["temp"]), 2)
    humidity = round(random.uniform(*profile["humidity"]), 2)
    energy  = round(random.uniform(*profile["energy"]), 3)
    occupancy = random.randint(*profile["occupancy"])
    anomaly_flag = 0

    # Randomly inject anomaly (5% chance, or forced)
    if inject_anomaly or random.random() < 0.05:
        temp += random.uniform(8, 15)   # sudden temperature spike
        energy *= random.uniform(2, 4)  # energy surge
        anomaly_flag = 1

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "zone": zone,
        "temperature": temp,
        "humidity": humidity,
        "energy_kwh": energy,
        "occupancy": occupancy,
        "anomaly_flag": anomaly_flag
    }

def insert_reading(reading):
    """Insert a reading into the database."""
    conn = sqlite3.connect("building_twin.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sensor_readings 
        (timestamp, zone, temperature, humidity, energy_kwh, occupancy, anomaly_flag)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        reading["timestamp"],
        reading["zone"],
        reading["temperature"],
        reading["humidity"],
        reading["energy_kwh"],
        reading["occupancy"],
        reading["anomaly_flag"]
    ))
    conn.commit()
    conn.close()

def run_simulator(cycles=100, interval=0.5):
    """Run the simulator for a given number of cycles."""
    print(f"Starting sensor simulator — {cycles} cycles, {interval}s interval")
    for i in range(cycles):
        for zone in ZONES:
            reading = generate_reading(zone)
            insert_reading(reading)
        if (i + 1) % 10 == 0:
            print(f"  Cycle {i+1}/{cycles} complete")
        time.sleep(interval)
    print("Simulation complete.")

if __name__ == "__main__":
    init_database()
    run_simulator(cycles=100, interval=0.1)