#!/usr/bin/env python3
"""
BTC-USD Volatility & Price Prediction Neural Network
Uses Python with PyTorch

Input: 60 minutes of OHLCV data
Output: volatility (std dev of returns) and price at t+15
"""

import csv
import math
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

DATA_PATH = "/root/.openclaw/.openclaw/workspace/btc_usd_1m.csv"
LOOKBACK = 60      # 60 minutes of history
FORWARD = 15       # Predict 15 minutes ahead
EPOCHS = 50
BATCH_SIZE = 32
LEARNING_RATE = 0.001

# Load data
def load_data(path):
    data = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': float(row['volume'])
            })
    return data

# Normalize using min-max
def normalize(data):
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
        'volume': d['volume']  # Keep raw for now
    } for d in data], min_val, max_val

# Create features
def create_features(data, lookback, forward):
    X, y_vol, y_price = [], [], []
    
    for i in range(lookback, len(data) - forward):
        window = data[i - lookback:i]
        
        # Features: 5 values * 60 minutes = 300 features
        features = []
        for d in window:
            features.extend([d['open'], d['high'], d['low'], d['close'], d['volume']])
        
        # Targets
        forward_prices = [data[j]['close'] for j in range(i, i + forward)]
        returns = []
        for j in range(len(forward_prices) - 1):
            if forward_prices[j] != 0:
                returns.append((forward_prices[j+1] - forward_prices[j]) / forward_prices[j])
        
        volatility = math.sqrt(sum(r*r for r in returns) / len(returns)) if returns else 0.0
        forward_price = forward_prices[-1]
        
        X.append(features)
        y_vol.append(volatility)
        y_price.append(forward_price)
    
    return X, y_vol, y_price

# Model
class PredictionModel(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4_vol = nn.Linear(32, 1)   # volatility head
        self.fc4_price = nn.Linear(32, 1) # price head
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(self.relu(self.fc2(x)))
        x = self.relu(self.fc3(x))
        volatility = self.fc4_vol(x)
        price = self.fc4_price(x)
        return volatility, price

# Main
print("Loading data...")
data = load_data(DATA_PATH)
print(f"Loaded {len(data)} data points")

print("Normalizing...")
normalized, min_val, max_val = normalize(data)

print(f"Creating features (lookback: {LOOKBACK}, forward: {FORWARD})...")
X, y_vol, y_price = create_features(normalized, LOOKBACK, FORWARD)
print(f"Training samples: {len(X)}")

# Convert to tensors
X_tensor = torch.tensor(X, dtype=torch.float32)
y_vol_tensor = torch.tensor(y_vol, dtype=torch.float32).reshape(-1, 1)
y_price_tensor = torch.tensor(y_price, dtype=torch.float32).reshape(-1, 1)

# Train/val split
split = int(len(X) * 0.8)
X_train, X_val = X_tensor[:split], X_tensor[split:]
y_vol_train, y_vol_val = y_vol_tensor[:split], y_vol_tensor[split:]
y_price_train, y_price_val = y_price_tensor[:split], y_price_tensor[split:]

print(f"Training set: {len(X_train)}, Validation: {len(X_val)}")

# DataLoader
train_dataset = TensorDataset(X_train, y_vol_train, y_price_train)
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Model
model = PredictionModel(LOOKBACK * 5)
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
mse = nn.MSELoss()

# Training
print("Starting training...")
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0.0
    
    for batch_X, batch_y_vol, batch_y_price in train_loader:
        optimizer.zero_grad()
        
        vol_pred, price_pred = model(batch_X)
        
        loss_vol = mse(vol_pred, batch_y_vol)
        loss_price = mse(price_pred, batch_y_price)
        loss = loss_vol + loss_price
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    # Validation
    model.eval()
    with torch.no_grad():
        vol_pred, price_pred = model(X_val)
        val_loss_vol = mse(vol_pred, y_vol_val).item()
        val_loss_price = mse(price_pred, y_price_val).item()
    
    if (epoch + 1) % 10 == 0:
        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{EPOCHS} - Train Loss: {avg_loss:.4f}, Val Vol: {val_loss_vol:.4f}, Val Price: {val_loss_price:.4f}")

print("Training complete!")

# Save model
torch.save(model.state_dict(), "/root/.openclaw/.openclaw/workspace/btc_model.pt")
print("Model saved to btc_model.pt")