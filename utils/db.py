import sqlite3
import os

DB_NAME = "data/f1.db"

def get_db_connection():
    """Connects to the SQLite database."""
    # Ensure data folder exists
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Creates the necessary tables if they don't exist."""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Table 1: Race Telemetry
    c.execute('''
        CREATE TABLE IF NOT EXISTS race_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            driver TEXT,
            lap_number INTEGER,
            lap_time REAL,
            sector_1 REAL,
            sector_2 REAL,
            sector_3 REAL,
            compound TEXT,
            tyre_life INTEGER
        )
    ''')
    
    # Table 2: AI Predictions
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            driver TEXT,
            lap_number INTEGER,
            pit_stop_probability REAL,
            model_version TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"🗄️  Database initialized at {DB_NAME}")

def insert_lap_data(event, pit_prob=0.0):
    """Saves a single lap event and its prediction to the DB."""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Insert Telemetry
    c.execute('''
        INSERT INTO race_telemetry 
        (driver, lap_number, lap_time, sector_1, sector_2, sector_3, compound, tyre_life)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        event['Driver'], 
        event['LapNumber'], 
        event['LapTime'],
        event.get('Sector1Time', 0),
        event.get('Sector2Time', 0),
        event.get('Sector3Time', 0),
        event['Compound'],
        event['TyreLife']
    ))
    
    # Insert Prediction (only if significant)
    if pit_prob > 0:
        c.execute('''
            INSERT INTO predictions (driver, lap_number, pit_stop_probability, model_version)
            VALUES (?, ?, ?, ?)
        ''', (event['Driver'], event['LapNumber'], pit_prob, "v1.0"))
        
    conn.commit()
    conn.close()

# Run initialization immediately when imported (optional, but convenient here)
if __name__ == "__main__":
    init_db()