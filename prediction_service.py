#!/usr/bin/env python3
"""
Crypto Prediction Service
Flask REST API that uses neural network to predict price probabilities

Endpoints:
- POST /api/predict - Predict probability of target price being equaled/exceeded
- POST /api/retrain - Retrain the neural network
- GET /health - Health check
- POST /api/shutdown - Graceful shutdown
"""

import os
import csv
import math
import threading
import time
import subprocess
import sqlite3
import urllib.request
import json

import torch
import torch.nn as nn
from flask import Flask, request, jsonify

app = Flask(__name__)

# Config
MODEL_PATH = "/root/.openclaw/.openclaw/workspace/crypto-predict-py/btc_model.pt"
DATA_SERVICE_URL = "http://localhost:5000"
DB_PATH = "/root/.openclaw/.openclaw/workspace/crypto_data.db"
LOOKBACK = 60
FORWARD = 15

# Neural Network Model (same architecture as training)
class PredictionModel(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4_vol = nn.Linear(32, 1)
        self.fc4_price = nn.Linear(32, 1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(self.relu(self.fc2(x)))
        x = self.relu(self.fc3(x))
        volatility = self.fc4_vol(x)
        price = self.fc4_price(x)
        return volatility, price

model = None
model_loaded = False

def load_model():
    """Load the trained model"""
    global model, model_loaded
    if os.path.exists(MODEL_PATH):
        model = PredictionModel(LOOKBACK * 5)
        model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
        model.eval()
        model_loaded = True
        print("Model loaded successfully")
    else:
        print(f"Model not found at {MODEL_PATH}")
        model_loaded = False

def get_quotes_from_service(symbol, start_ts, minutes):
    """Get quotes from the crypto data service"""
    from datetime import datetime, timedelta
    start_dt = datetime.utcfromtimestamp(start_ts).strftime('%Y-%m-%d %H:%M:%S')
    url = f"{DATA_SERVICE_URL}/api/quotes?symbol={symbol}&start={start_dt.replace(' ', '%20')}&minutes={minutes}"
    try:
        resp = urllib.request.urlopen(url, timeout=30)
        return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def get_latest_from_db(symbol, count):
    """Get latest quotes from local database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT * FROM quotes 
                 WHERE symbol = ? ORDER BY timestamp DESC LIMIT ?''',
              (symbol, count))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def normalize_data(data):
    """Normalize data using min-max scaling"""
    closes = [d['close'] for d in data]
    min_val = min(closes)
    max_val = max(closes)
    range_val = max_val - min_val
    if range_val == 0:
        range_val = 1
    
    return [{
        'open': (d['open'] - min_val) / range_val,
        'high': (d['high'] - min_val) / range_val,
        'low': (d['low'] - min_val) / range_val,
        'close': (d['close'] - min_val) / range_val,
        'volume': d['volume']
    } for d in data], min_val, max_val

def create_features(window):
    """Create feature vector from window"""
    features = []
    for d in window:
        features.extend([d['open'], d['high'], d['low'], d['close'], d['volume']])
    return features

def predict_price(features):
    """Make prediction using the model"""
    if not model_loaded:
        return None, None
    
    with torch.no_grad():
        x = torch.tensor([features], dtype=torch.float32)
        vol_pred, price_pred = model(x)
        return vol_pred.item(), price_pred.item()

def calculate_probability(predicted_price, target_price, volatility, min_price, max_price):
    """
    Calculate probability of target being equaled or exceeded
    Using simple normal distribution approximation
    """
    if volatility is None or volatility <= 0:
        # If no volatility, use deterministic prediction
        return 1.0 if predicted_price >= target_price else 0.0
    
    # Normalize target to [0,1] range
    range_val = max_price - min_price
    if range_val == 0:
        range_val = 1
    
    norm_target = (target_price - min_price) / range_val
    norm_predicted = predicted_price
    
    # Calculate z-score
    z_score = (norm_target - norm_predicted) / (volatility + 1e-6)
    
    # Probability of price >= target (one-tailed)
    # Using approximation
    from math import erf
    prob = 0.5 * (1 + erf(z_score / math.sqrt(2)))
    
    return max(0.0, min(1.0, prob))

# API Endpoints

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict probability of target price being equaled or exceeded
    
    Request body:
    {
        "symbol": "BTC-USD",
        "target_price": 70000,
        "end_time": "2026-03-31 04:00:00"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON body provided"}), 400
    
    symbol = data.get('symbol', 'BTC-USD')
    target_price = data.get('target_price')
    end_time_str = data.get('end_time')
    
    if not target_price or not end_time_str:
        return jsonify({"error": "target_price and end_time are required"}), 400
    
    # Parse end time
    from datetime import datetime
    try:
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
        end_ts = int(end_time.timestamp())
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400
    
    # Get current time
    current_ts = int(datetime.utcnow().timestamp())
    
    # Calculate how many minutes ahead
    minutes_ahead = max(1, (end_ts - current_ts) // 60)
    
    # Get recent data (lookback + forward window)
    total_needed = LOOKBACK + minutes_ahead + 10
    quotes = get_latest_from_db(symbol, total_needed)
    
    if len(quotes) < LOOKBACK:
        return jsonify({"error": "Insufficient data for prediction"}), 400
    
    # Use the last LOOKBACK points as input
    input_data = quotes[:LOOKBACK]
    normalized, min_val, max_val = normalize_data(input_data)
    features = create_features(normalized)
    
    # Make prediction
    volatility, predicted_price = predict_price(features)
    
    if predicted_price is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    # Denormalize prediction
    range_val = max_val - min_val
    actual_predicted = predicted_price * range_val + min_val
    
    # Calculate probability
    probability = calculate_probability(
        actual_predicted, 
        target_price, 
        volatility,
        min_val,
        max_val
    )
    
    return jsonify({
        "symbol": symbol,
        "target_price": target_price,
        "end_time": end_time_str,
        "predicted_price": round(actual_predicted, 2),
        "volatility": round(volatility, 6) if volatility else None,
        "probability_exceed": round(probability, 4),
        "minutes_ahead": minutes_ahead
    })

@app.route('/api/retrain', methods=['POST'])
def retrain():
    """
    Retrain the neural network using all collected quote data
    
    Optional body:
    {
        "epochs": 50,
        "batch_size": 32
    }
    """
    data = request.get_json() or {}
    epochs = data.get('epochs', 50)
    batch_size = data.get('batch_size', 32)
    
    # Run training in background
    def train_model():
        print("Starting model retraining...")
        
        # Get all data from database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM quotes WHERE symbol='BTC-USD' ORDER BY timestamp")
        rows = c.fetchall()
        conn.close()
        
        if len(rows) < LOOKBACK + FORWARD:
            print("Insufficient data for training")
            return
        
        # Convert to dict format
        data = []
        for r in rows:
            data.append({
                'open': r[3], 'high': r[4], 'low': r[5], 
                'close': r[6], 'volume': r[7]
            })
        
        # Normalize
        normalized, min_val, max_val = normalize_data(data)
        
        # Create features
        X, y_vol, y_price = [], [], []
        for i in range(LOOKBACK, len(data) - FORWARD):
            window = normalized[i - LOOKBACK:i]
            features = create_features(window)
            
            forward_prices = [data[j]['close'] for j in range(i, i + FORWARD)]
            returns = []
            for j in range(len(forward_prices) - 1):
                if forward_prices[j] != 0:
                    returns.append((forward_prices[j+1] - forward_prices[j]) / forward_prices[j])
            
            volatility = math.sqrt(sum(r*r for r in returns) / len(returns)) if returns else 0.0
            
            X.append(features)
            y_vol.append(volatility)
            y_price.append(forward_prices[-1])
        
        # Convert to tensors
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_vol_tensor = torch.tensor(y_vol, dtype=torch.float32).reshape(-1, 1)
        y_price_tensor = torch.tensor(y_price, dtype=torch.float32).reshape(-1, 1)
        
        # Train model
        global model
        model = PredictionModel(LOOKBACK * 5)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        mse = nn.MSELoss()
        
        split = int(len(X) * 0.8)
        X_train, X_val = X_tensor[:split], X_tensor[split:]
        y_vol_train, y_vol_val = y_vol_tensor[:split], y_vol_tensor[split:]
        y_price_train, y_price_val = y_price_tensor[:split], y_price_tensor[split:]
        
        for epoch in range(epochs):
            model.train()
            for i in range(0, len(X_train), batch_size):
                batch_x = X_train[i:i+batch_size]
                batch_yv = y_vol_train[i:i+batch_size]
                batch_yp = y_price_train[i:i+batch_size]
                
                optimizer.zero_grad()
                vol_pred, price_pred = model(batch_x)
                loss = mse(vol_pred, batch_yv) + mse(price_pred, batch_yp)
                loss.backward()
                optimizer.step()
            
            if (epoch + 1) % 10 == 0:
                model.eval()
                with torch.no_grad():
                    vol_pred, price_pred = model(X_val)
                    val_loss = mse(vol_pred, y_vol_val).item() + mse(price_pred, y_price_val).item()
                print(f"Epoch {epoch+1}/{epochs}, Val Loss: {val_loss:.4f}")
        
        # Save model
        torch.save(model.state_dict(), MODEL_PATH)
        global model_loaded
        model_loaded = True
        print("Model retraining complete!")
    
    # Run training in background thread
    thread = threading.Thread(target=train_model)
    thread.start()
    
    return jsonify({"status": "retraining_started", "message": "Model retraining started in background"})

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM quotes")
        count = c.fetchone()[0]
    except:
        count = 0
    conn.close()
    
    return jsonify({
        "status": "ok",
        "model_loaded": model_loaded,
        "quotes_in_db": count
    })

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """Graceful shutdown"""
    print("Shutdown requested...")
    
    def shutdown_server():
        import os
        os._exit(0)
    
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    else:
        threading.Timer(1, shutdown_server).start()
    
    return jsonify({"status": "shutting_down"})

if __name__ == '__main__':
    print("Loading model...")
    load_model()
    print("Starting prediction service on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)