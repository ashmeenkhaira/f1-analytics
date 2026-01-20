from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI(title="F1 Real-Time Analytics API")

# Allow the dashboard (which might run on a different port) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join("data", "f1.db")

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database not found. Run ingestion first.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.get("/")
def health_check():
    """Simple check to see if API is running."""
    return {"status": "online", "service": "f1-analytics"}

@app.get("/laps/recent")
def get_recent_laps(limit: int = 20):
    """Fetch the latest N laps from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Get the most recent laps (highest ID)
    cursor.execute("SELECT * FROM race_telemetry ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/stats/driver/{driver_id}")
def get_driver_stats(driver_id: str):
    """Get basic stats for a specific driver."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate avg lap time and tyre age
    cursor.execute("""
        SELECT 
            AVG(lap_time) as avg_lap, 
            MAX(tyre_life) as current_tyre_age,
            COUNT(*) as laps_completed
        FROM race_telemetry 
        WHERE driver = ?
    """, (driver_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row or row['laps_completed'] == 0:
        raise HTTPException(status_code=404, detail="Driver not found")
        
    return dict(row)

@app.get("/predictions/recent")
def get_recent_predictions(limit: int = 5):
    """Fetch the latest AI predictions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # We join with telemetry to get more context if needed, but simple select is fine
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]