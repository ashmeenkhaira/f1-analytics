import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib
import os

# 1. Load Data
DATA_PATH = "data/f1_2023_bahrain.csv"
MODEL_PATH = "data/models/pit_stop_model.pkl"

def train():
    print("🧠 Training Pit Stop Prediction Model...")
    
    if not os.path.exists(DATA_PATH):
        print("❌ Error: Data file not found.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # 2. Feature Engineering (Create Labels)
    # We want to predict if a driver pits in the NEXT lap.
    # Logic: If TyreLife drops (e.g., 20 -> 1), it means they just pitted.
    # So the PREVIOUS row was the "In Lap".
    
    # Shift TyreLife back by -1 to see the "next" value
    df['NextTyreLife'] = df.groupby('Driver')['TyreLife'].shift(-1)
    
    # If NextTyreLife is 1.0 (fresh tyres) AND Current TyreLife > 1, then Pitted = 1
    df['IsPittingNext'] = ((df['NextTyreLife'] == 1.0) & (df['TyreLife'] > 1)).astype(int)
    
    # Drop NaNs (last lap has no next lap)
    df = df.dropna(subset=['IsPittingNext'])
    
    # Features we use for prediction
    X = df[['TyreLife', 'Compound']]
    y = df['IsPittingNext']
    
    print(f"📊 Training on {len(df)} laps. Found {y.sum()} pit stop examples.")

    # 3. Build the ML Pipeline
    # We need to turn 'Compound' (Text) into numbers using OneHotEncoder
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['Compound'])
        ],
        remainder='passthrough' # Keep TyreLife as is
    )
    
    # Logistic Regression is great for binary probabilities
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression())
    ])
    
    # 4. Train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model Accuracy: {acc:.2%}")
    
    # 6. Save Model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"💾 Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()