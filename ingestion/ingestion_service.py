import sys
import os
import joblib
import pandas as pd
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.data_simulator import DataSimulator
from stream_processing.processor import StreamProcessor
from utils.db import init_db, insert_lap_data  # <--- NEW IMPORT

DATA_FILE = os.path.join("data", "f1_2023_bahrain.csv")
MODEL_PATH = os.path.join("data", "models", "pit_stop_model.pkl")

def start_ingestion():
    # 1. Initialize Database
    init_db()  # <--- Create tables on startup

    if not os.path.exists(DATA_FILE):
        return
    
    print("🧠 Loading ML Model...")
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model Loaded.")
    except Exception:
        model = None

    simulator = DataSimulator(DATA_FILE, sleep_interval=0.05) # Super fast for filling DB
    processor = StreamProcessor(window_size=5)
    
    print(f"🚀 Race Stream Started... Saving to DB.")
    
    try:
        for raw_event in simulator.stream():
            enriched_event = processor.process_event(raw_event)
            
            # --- ML PREDICTION ---
            pit_prob = 0.0
            if model:
                input_df = pd.DataFrame([[raw_event['TyreLife'], raw_event['Compound']]], 
                                      columns=['TyreLife', 'Compound'])
                pit_prob = model.predict_proba(input_df)[0][1]

            # --- DB SAVE ---
            insert_lap_data(raw_event, pit_prob) # <--- SAVE DATA HERE

            # --- VISUALS ---
            anomaly = enriched_event.get('anomaly')
            if anomaly == "PIT_STOP_SUSPECTED":
                print(f"🛑 {enriched_event['Driver']} Pitting (Saved to DB)")
            elif pit_prob > 0.4:
                 print(f"🔮 AI Warning: {enriched_event['Driver']} Pit Prob: {pit_prob:.1%}")

    except KeyboardInterrupt:
        print("\n🛑 Stopped.")

if __name__ == "__main__":
    start_ingestion()