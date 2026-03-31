#!/usr/bin/env python3
"""
Update BTC-USD historical dataset
Fetches latest minute-level data from CryptoCompare and appends to existing CSV
"""

import csv
import math
import os
import sys
import time
import urllib.request
import json

DATA_PATH = "/root/.openclaw/.openclaw/workspace/btc_usd_1m.csv"
API_URL = "https://min-api.cryptocompare.com/data/v2/histominute"

def fetch_latest(min_limit=60):
    """Fetch latest minute-level BTC-USD data"""
    url = f"{API_URL}?fsym=BTC&tsym=USD&limit={min_limit}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            if data.get("Response") == "Success":
                return data["Data"]["Data"]
            else:
                print(f"API error: {data.get('Message', 'Unknown')}")
                return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def load_existing_timestamps(path):
    """Load existing timestamps from CSV"""
    if not os.path.exists(path):
        return set()
    
    timestamps = set()
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.add(int(row['timestamp']))
    return timestamps

def append_to_csv(path, new_data, existing_timestamps):
    """Append new data points to CSV"""
    # Filter out duplicates
    new_points = [d for d in new_data if d['time'] not in existing_timestamps]
    
    if not new_points:
        print("No new data to add")
        return 0
    
    # Sort by timestamp
    new_points.sort(key=lambda x: x['time'])
    
    # Append to CSV
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        for d in new_points:
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(d['time']))
            writer.writerow([
                d['time'],
                dt,
                d['open'],
                d['high'],
                d['low'],
                d['close'],
                d.get('volumeto', 0)
            ])
    
    return len(new_points)

def main():
    print("Fetching latest BTC-USD data...")
    data = fetch_latest(2000)  # Get last ~1.5 days
    
    if not data:
        print("Failed to fetch data")
        sys.exit(1)
    
    print(f"Fetched {len(data)} data points")
    
    existing = load_existing_timestamps(DATA_PATH)
    print(f"Existing data points: {len(existing)}")
    
    count = append_to_csv(DATA_PATH, data, existing)
    print(f"Added {count} new data points")
    
    # Show date range
    with open(DATA_PATH, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if rows:
            print(f"Date range: {rows[0]['datetime']} to {rows[-1]['datetime']}")

if __name__ == "__main__":
    main()