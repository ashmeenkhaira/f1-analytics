import fastf1
import pandas as pd
import os

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Enable caching (FastF1 saves data to a folder so it doesn't re-download every time)
# We will create a cache folder in the root
cache_dir = "data/cache"
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir) 

def download_race_data():
    print("⏳ Downloading 2023 Bahrain GP data... (this may take 1-2 mins)")
    
    # Load the race session (Year, Location, Session Type 'R' for Race)
    session = fastf1.get_session(2023, 'Bahrain', 'R')
    session.load(telemetry=False, laps=True, weather=False)
    
    # Get all laps for the race
    laps = session.laps
    
    # Select specific columns we care about for the dashboard
    # We want 'Driver', 'LapNumber', 'LapTime', 'Compound' (Tyres), etc.
    cols = ['Driver', 'LapNumber', 'LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time', 'Compound', 'TyreLife']
    
    # Pick a few exciting drivers to track (e.g., VER, ALO, HAM, LEC)
    # or just keep everyone. Let's filter for top drivers to keep the CSV clean for now.
    drivers = ['VER', 'ALO', 'HAM', 'LEC', 'SAI', 'RUS']
    laps_filtered = laps[laps['Driver'].isin(drivers)][cols].copy()
    
    # Convert timedelta to seconds (easier for JSON/Streamlit)
    # e.g., "1 min 30 sec" -> 90.0
    laps_filtered['LapTime'] = laps_filtered['LapTime'].dt.total_seconds()
    laps_filtered['Sector1Time'] = laps_filtered['Sector1Time'].dt.total_seconds()
    laps_filtered['Sector2Time'] = laps_filtered['Sector2Time'].dt.total_seconds()
    laps_filtered['Sector3Time'] = laps_filtered['Sector3Time'].dt.total_seconds()
    
    # Sort by LapNumber so we can "stream" it in order
    laps_filtered = laps_filtered.sort_values(by=['LapNumber', 'Driver'])
    
    # Save to CSV
    output_path = "data/f1_2023_bahrain.csv"
    laps_filtered.to_csv(output_path, index=False)
    print(f"✅ Data saved to {output_path}")
    print(laps_filtered.head())

if __name__ == "__main__":
    download_race_data()