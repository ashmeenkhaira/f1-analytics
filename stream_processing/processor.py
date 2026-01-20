import collections

class StreamProcessor:
    def __init__(self, window_size=5):
        # Stores the last N lap times for each driver
        self.driver_history = collections.defaultdict(lambda: collections.deque(maxlen=window_size))
        
        # Track the fastest lap of the entire race
        self.best_lap_time = float('inf')
        self.best_lap_driver = None

    def process_event(self, event):
        """
        Takes a raw telemetry event, enriches it with stats, 
        and detects anomalies.
        """
        driver = event['Driver']
        lap_time = event['LapTime']
        
        # 1. Initialize result dictionary
        result = event.copy()
        result['anomaly'] = None
        
        # 2. Skip if LapTime is invalid
        if not lap_time or lap_time <= 0:
            return result

        # 3. Calculate Rolling Average & Detect Pit Stops
        history = self.driver_history[driver]
        if len(history) > 0:
            avg_time = sum(history) / len(history)
            result['rolling_avg'] = round(avg_time, 3)
            
            # ANOMALY: If lap is > 1.15x slower than average -> Likely Pit Stop
            if lap_time > avg_time * 1.15:
                result['anomaly'] = "PIT_STOP_SUSPECTED"
        else:
            result['rolling_avg'] = lap_time

        # 4. Check for FASTEST LAP
        if lap_time < self.best_lap_time:
            self.best_lap_time = lap_time
            self.best_lap_driver = driver
            result['anomaly'] = "FASTEST_LAP"

        # 5. Update History
        self.driver_history[driver].append(lap_time)
        
        return result