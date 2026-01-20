<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>F1 Real-Time Analytics Platform</title>
</head>

<body>

<div align="center">
  <img 
    src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z6cW15aW56aW56aW56aW56aW56aW56aW56aW56aW56aW56aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKSjRrfIPjeiVyM/giphy.gif"
    width="600"
    alt="F1 Telemetry Animation"
  />

  <h1>🏎️ F1 Real-Time Analytics Platform</h1>

  <p>
    <strong>Live Telemetry Ingestion • Anomaly Detection • ML Strategy Prediction</strong>
  </p>

  <p>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://fastapi.tiangolo.com/">
      <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
    </a>
    <a href="https://streamlit.io/">
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
    </a>
    <a href="https://scikit-learn.org/">
      <img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
    </a>
    <a href="https://www.sqlite.org/">
      <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
    </a>
  </p>
</div>

<hr />

<details>
  <summary><strong>Table of Contents</strong></summary>
  <ol>
    <li><a href="#about">About The Project</a></li>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#machine-learning">Machine Learning</a></li>
  </ol>
</details>

<hr />

<h2 id="about">🏎️ About The Project</h2>

<p>
  This is a full-stack data engineering and machine learning project that simulates a
  <strong>real-time Formula 1 race strategy console</strong>.
</p>

<p>
  Unlike static analysis, this platform processes race data as a <strong>live stream</strong>,
  mimicking race-wall conditions. It ingests lap-level telemetry, performs stateful
  stream processing, detects anomalies such as slow pit stops, and predicts pit-stop
  probability before it occurs.
</p>

<h3>Key Features</h3>
<ul>
  <li>📡 <strong>Live Ingestion System:</strong> Simulates real-time telemetry from the 2023 Bahrain GP using FastF1</li>
  <li>⚡ <strong>Stream Processing:</strong> Rolling average lap-time computation and anomaly detection in &lt;50ms</li>
  <li>🧠 <strong>Predictive ML:</strong> Real-time pit-stop probability scoring based on tyre data</li>
  <li>💾 <strong>Hybrid Storage:</strong> SQLite for persistence + in-memory deques for low-latency windowing</li>
  <li>📊 <strong>Interactive Dashboard:</strong> Auto-refreshing Streamlit UI for live monitoring</li>
</ul>

<hr />

<h2 id="architecture">🏗️ Architecture</h2>

<pre>
graph LR
    A[Simulator / API] -->|Raw Telemetry| B(Ingestion Service)
    B -->|Structured Event| C{Stream Processor}
    C -->|Rolling Stats| D[ML Engine]
    C -->|Race Events| E[SQLite DB]
    D -->|Predictions| E
    E -->|Read| F[FastAPI]
    F -->|JSON| G[Streamlit UI]
</pre>

<ul>
  <li><strong>Ingestion:</strong> Python generator emits lap events with simulated latency</li>
  <li><strong>Processing:</strong> Stateful stream processor maintains per-driver rolling windows</li>
  <li><strong>Storage:</strong> SQLite database for historical and analytical queries</li>
  <li><strong>API:</strong> FastAPI exposes structured race data</li>
  <li><strong>Frontend:</strong> Streamlit dashboard polls API every 2 seconds</li>
</ul>

<hr />

<h2 id="getting-started">🚀 Getting Started</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.8+</li>
  <li>Git</li>
</ul>

<h3>Installation</h3>

<pre>
git clone https://github.com/YOUR_USERNAME/f1-realtime-analytics.git
cd f1-realtime-analytics
</pre>

<h3>Create Virtual Environment</h3>

<pre>
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
</pre>

<h3>Install Dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

<h3>Prepare Data</h3>

<pre>
python ingestion/download_data.py
</pre>

<hr />

<h2 id="usage">🕹️ Usage</h2>

<p>Run the system using <strong>three terminals</strong>:</p>

<h3>Terminal 1: Ingestion Service</h3>
<pre>
python ingestion/ingestion_service.py
</pre>

<h3>Terminal 2: API Server</h3>
<pre>
uvicorn api.main:app --reload
</pre>
<p>API Docs: <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></p>

<h3>Terminal 3: Dashboard</h3>
<pre>
streamlit run dashboard/app.py
</pre>

<hr />

<h2 id="machine-learning">🧠 Machine Learning</h2>

<p>
  The platform uses a <strong>Logistic Regression</strong> model for pit-stop prediction.
</p>

<ul>
  <li><strong>Training Data:</strong> 2023 Bahrain GP telemetry</li>
  <li><strong>Features:</strong>
    <ul>
      <li>TyreLife (normalized lap count)</li>
      <li>Compound (Soft / Medium / Hard – one-hot encoded)</li>
    </ul>
  </li>
  <li><strong>Target:</strong> IsPittingNext (binary)</li>
  <li><strong>Performance:</strong> ~94% accuracy on held-out test set</li>
</ul>

<h3>Retrain Model</h3>
<pre>
python ml/train_model.py
</pre>

<hr />

<div align="center">
  <p>Built with ❤️ using Python</p>
</div>

</body>
</html>
