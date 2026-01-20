import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="F1 Live Analytics", layout="wide", page_icon="🏎️")

# --- HEADER ---
st.title("🏎️ F1 Real-Time Strategy Monitor")
st.markdown("Live telemetry ingestion • ML Pit Stop Predictions • SQLite History")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Control Panel")
    refresh_rate = st.slider("Refresh Rate (seconds)", 1, 5, 2)
    st.markdown("---")
    st.markdown("**System Status:**")
    try:
        r = requests.get(f"{API_URL}/")
        if r.status_code == 200:
            st.success("✅ API Online")
        else:
            st.error("❌ API Error")
    except:
        st.error("❌ API Offline")

# --- MAIN DASHBOARD LOOP ---
placeholder = st.empty()

while True:
    try:
        # 1. Fetch Data from API
        laps_res = requests.get(f"{API_URL}/laps/recent?limit=30")
        preds_res = requests.get(f"{API_URL}/predictions/recent?limit=5")
        
        laps_data = laps_res.json()
        preds_data = preds_res.json()
        
        with placeholder.container():
            # Create three columns for key metrics
            kpi1, kpi2, kpi3 = st.columns(3)

            if laps_data:
                df = pd.DataFrame(laps_data)
                
                # Metric 1: Latest Lap
                latest_lap = df.iloc[0]
                kpi1.metric(
                    label=f"🏁 Leader ({latest_lap['driver']})",
                    value=f"{latest_lap['lap_time']} s",
                    delta=f"Lap {latest_lap['lap_number']}"
                )
                
                # Metric 2: Fastest in Window
                fastest_lap = df['lap_time'].min()
                fastest_driver = df.loc[df['lap_time'] == fastest_lap, 'driver'].values[0]
                kpi2.metric(
                    label="⚡ Fastest (Recent)",
                    value=f"{fastest_lap} s",
                    delta=fastest_driver
                )
            
            # Metric 3: ML Alert
            if preds_data:
                latest_pred = preds_data[0]
                prob = latest_pred['pit_stop_probability']
                driver = latest_pred['driver']
                
                if prob > 0.3:
                    kpi3.metric(label="⚠️ AI Prediction", value="PIT LIKELY", delta=f"{driver} ({prob:.0%})", delta_color="inverse")
                else:
                    kpi3.metric(label="AI Prediction", value="Track Clear", delta="No anomalies")
            else:
                 kpi3.metric(label="AI Prediction", value="Waiting...", delta="Collecting data")

            # --- CHARTS ---
            st.markdown("### 📈 Live Lap Times")
            if laps_data:
                # Create a simple line chart comparing drivers
                chart_df = df[['lap_number', 'lap_time', 'driver']]
                fig = px.line(chart_df, x='lap_number', y='lap_time', color='driver', markers=True, title="Lap Time Trend (Last 30 Laps)")
                st.plotly_chart(fig, use_container_width=True)

            # --- RAW DATA TABLES ---
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ⏱️ Recent Telemetry")
                st.dataframe(df, height=250)
            
            with col2:
                st.markdown("#### 🤖 AI Predictions Log")
                if preds_data:
                    st.dataframe(pd.DataFrame(preds_data), height=250)
                else:
                    st.info("No predictions generated yet.")

        # Wait before refreshing
        time.sleep(refresh_rate)
        
    except Exception as e:
        st.error(f"Waiting for data... ({e})")
        time.sleep(5)