#!/usr/bin/env python3
"""
Update BTC-USD historical dataset
- Scans for gaps in minute-level data
- Fetches historical data to fill gaps
- If most recent quote > 60 minutes old, fetches latest data
- Writes data file in sorted order from oldest to newest
"""

import csv
import os
import sys
import time
import urllib.request
import json
from datetime import datetime, timedelta

DATA_PATH = "/root/.openclaw/.openclaw/workspace/btc_usd_1m.csv"
API_URL = "https://min-api.cryptocompare.com/data/v2/histominute"

def fetch_data(limit=2000, to_ts=None):
    """Fetch minute-level BTC-USD data from CryptoCompare"""
    url = f"{API_URL}?fsym=BTC&tsym=USD&limit={limit}"
    if to_ts:
        url += f"&toTs={to_ts}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            if data.get("Response") == "Success":
                # Data comes in reverse order (newest first), so reverse it
                return list(reversed(data["Data"]["Data"]))
            else:
                print(f"API error: {data.get('Message', 'Unknown')}")
                return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def load_csv_data(path):
    """Load all data from CSV into a list of dicts"""
    if not os.path.exists(path):
        return []
    
    data = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'timestamp': int(row['timestamp']),
                'datetime': row['datetime'],
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': float(row['volume'])
            })
    return data

def find_gaps(data, max_gap_seconds=60):
    """Find gaps in the minute-level data. Returns list of (start, end) gap tuples."""
    if len(data) < 2:
        return []
    
    # Sort by timestamp
    sorted_data = sorted(data, key=lambda x: x['timestamp'])
    
    gaps = []
    for i in range(len(sorted_data) - 1):
        current_ts = sorted_data[i]['timestamp']
        next_ts = sorted_data[i + 1]['timestamp']
        
        # Expected difference is 60 seconds (1 minute)
        if next_ts - current_ts > max_gap_seconds:
            gaps.append((current_ts, next_ts))
    
    return gaps

def fetch_gap_data(gap_start_ts, gap_end_ts):
    """Fetch data to fill a specific gap"""
    # Calculate how many minutes we need
    gap_minutes = (gap_end_ts - gap_start_ts) // 60
    
    # Add some buffer to ensure we get the gap data
    fetch_minutes = gap_minutes + 10
    
    # Use toTs parameter to get data up to the gap end
    data = fetch_data(limit=min(fetch_minutes, 2000), to_ts=gap_end_ts)
    
    if not data:
        return []
    
    # Filter to only include data within the gap range
    filtered = [d for d in data if gap_start_ts <= d['time'] < gap_end_ts]
    return filtered

def fetch_gaps(gaps):
    """Fetch data to fill identified gaps"""
    all_new_data = []
    
    for i, (start_ts, end_ts) in enumerate(gaps):
        print(f"Gap {i+1}: {datetime.utcfromtimestamp(start_ts)} -> {datetime.utcfromtimestamp(end_ts)} ({(end_ts-start_ts)//60} min)")
        
        gap_data = fetch_gap_data(start_ts, end_ts)
        if gap_data:
            print(f"  Retrieved {len(gap_data)} data points")
            all_new_data.extend(gap_data)
        else:
            print(f"  Failed to retrieve data")
    
    return all_new_data

def update_if_stale(data, max_age_seconds=3600):
    """If most recent quote is older than max_age_seconds, fetch latest data"""
    if not data:
        return fetch_data(60) or []
    
    sorted_data = sorted(data, key=lambda x: x['timestamp'])
    latest_ts = sorted_data[-1]['timestamp']
    current_ts = int(time.time())
    
    age = current_ts - latest_ts
    print(f"Latest data age: {age} seconds ({age/60:.1f} minutes)")
    
    if age > max_age_seconds:
        print(f"Data is stale (> {max_age_seconds}s), fetching latest...")
        return fetch_data(2000) or []
    
    return []

def save_sorted(data, path):
    """Save data to CSV sorted from oldest to newest"""
    sorted_data = sorted(data, key=lambda x: x['timestamp'])
    
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'datetime', 'open', 'high', 'low', 'close', 'volume'])
        for row in sorted_data:
            writer.writerow([
                row['timestamp'],
                row['datetime'],
                row['open'],
                row['high'],
                row['low'],
                row['close'],
                row['volume']
            ])
    
    return len(sorted_data)

def main():
    print("=" * 50)
    print("BTC-USD Dataset Updater")
    print("=" * 50)
    
    # Load existing data
    print(f"\nLoading existing data from {DATA_PATH}...")
    existing_data = load_csv_data(DATA_PATH)
    print(f"Loaded {len(existing_data)} existing data points")
    
    if existing_data:
        sorted_existing = sorted(existing_data, key=lambda x: x['timestamp'])
        print(f"Date range: {sorted_existing[0]['datetime']} to {sorted_existing[-1]['datetime']}")
    
    # Step 1: Find gaps
    print("\n[1] Scanning for gaps...")
    gaps = find_gaps(existing_data)
    print(f"Found {len(gaps)} gap(s)")
    
    # Step 2: Fetch data to fill gaps
    new_data = []
    if gaps:
        print("\n[2] Fetching data to fill gaps...")
        new_data = fetch_gaps(gaps)
        print(f"Total fetched: {len(new_data)} new data points")
    
    # Step 3: Check if data is stale and fetch latest if needed
    print("\n[3] Checking if data needs update...")
    latest_data = update_if_stale(existing_data, max_age_seconds=3600)
    if latest_data:
        print(f"Fetched {len(latest_data)} latest data points")
        new_data.extend(latest_data)
    
    # Step 4: Merge and save sorted data
    if new_data or True:  # Always save to ensure sorted order
        print("\n[4] Merging and saving data...")
        
        # Build dict of existing data
        existing_dict = {(d['timestamp']): d for d in existing_data}
        original_count = len(existing_dict)
        
        # Add new data, avoiding duplicates
        new_count = 0
        for nd in new_data:
            ts = nd['time']
            if ts not in existing_dict:
                dt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                existing_dict[ts] = {
                    'timestamp': ts,
                    'datetime': dt,
                    'open': nd['open'],
                    'high': nd['high'],
                    'low': nd['low'],
                    'close': nd['close'],
                    'volume': nd.get('volumeto', 0)
                }
                new_count += 1
        
        # Save sorted
        count = save_sorted(list(existing_dict.values()), DATA_PATH)
        print(f"Saved {count} data points (sorted oldest to newest)")
        print(f"Added {new_count} new points")
        
        # Show new date range
        sorted_data = sorted(existing_dict.values(), key=lambda x: x['timestamp'])
        print(f"New date range: {sorted_data[0]['datetime']} to {sorted_data[-1]['datetime']}")
        
        # Check for remaining gaps
        remaining_gaps = find_gaps(list(existing_dict.values()))
        if remaining_gaps:
            print(f"\nWarning: {len(remaining_gaps)} gap(s) remain")
            for i, (s, e) in enumerate(remaining_gaps):
                print(f"  Gap {i+1}: {datetime.utcfromtimestamp(s)} -> {datetime.utcfromtimestamp(e)}")
        else:
            print("\n✓ All gaps filled - dataset is complete!")
    
    print("\nDone!")

if __name__ == "__main__":
    main()