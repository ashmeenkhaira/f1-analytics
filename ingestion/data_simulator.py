import pandas as pd
import time
import os

class DataSimulator:
    def __init__(self, data_path, sleep_interval=0.5):
        self.data_path = data_path
        self.sleep_interval = sleep_interval
        
        # Verify file exists
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"❌ File not found: {data_path}")
            
        self.data = pd.read_csv(data_path)

    def stream(self):
        """Yields one lap event at a time."""
        print(f"🏎️  Replaying Race from {self.data_path}...")
        
        for index, row in self.data.iterrows():
            event = row.to_dict()
            yield event
            time.sleep(self.sleep_interval)
            
        print("🏁 Race Simulation Ended.")