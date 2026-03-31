#!/usr/bin/env python3
"""
CLI tool to query crypto quotes
Usage: python3 query_quotes.py <symbol> <samples>
Example: python3 query_quotes.py BTC-USD 5

This script:
1. Starts the crypto data service if not already running
2. Queries quotes at 1-minute intervals
3. Prints timestamp, symbol, and OHLCV values
4. Shuts down the service if it started it
"""

import requests
import subprocess
import sys
import time
import os
import signal

SERVICE_URL = "http://localhost:5000"
SERVICE_SCRIPT = "/root/.openclaw/.openclaw/workspace/crypto_data_service.py"

def is_service_running():
    """Check if service is already running"""
    try:
        resp = requests.get(f"{SERVICE_URL}/health", timeout=2)
        return resp.status_code == 200
    except:
        return False

def start_service():
    """Start the crypto data service"""
    print("Starting crypto data service...")
    proc = subprocess.Popen(
        [sys.executable, SERVICE_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Wait for service to be ready
    for _ in range(30):
        if is_service_running():
            print("Service started successfully")
            return proc
        time.sleep(0.5)
    raise Exception("Failed to start service")

def stop_service():
    """Stop the crypto data service gracefully"""
    print("Shutting down service...")
    try:
        requests.post(f"{SERVICE_URL}/api/shutdown", timeout=5)
    except:
        pass
    time.sleep(1)

def query_quotes(symbol, samples):
    """Query quotes at 1-minute intervals"""
    # Get the latest timestamp first
    resp = requests.get(f"{SERVICE_URL}/api/quotes?symbol={symbol}&start=2026-01-01%2000:00:00&minutes=1000000")
    resp.raise_for_status()
    data = resp.json()
    
    if not data.get('quotes'):
        print(f"No quotes found for {symbol}")
        return
    
    # Calculate start time (samples minutes ago from latest)
    quotes = data['quotes']
    latest = quotes[-1]
    latest_ts = latest['timestamp']
    start_ts = latest_ts - (samples * 60)
    
    for i in range(samples):
        target_ts = start_ts + (i * 60)
        
        # Find closest quote
        closest = min(quotes, key=lambda q: abs(q['timestamp'] - target_ts))
        
        print(f"{closest['datetime']} | {closest['symbol']} | O:{closest['open']:.2f} H:{closest['high']:.2f} L:{closest['low']:.2f} C:{closest['close']:.2f} V:{closest['volume']:.0f}")
        
        if i < samples - 1:
            time.sleep(60)  # Wait 1 minute between queries

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 query_quotes.py <symbol> <samples>")
        print("Example: python3 query_quotes.py BTC-USD 5")
        sys.exit(1)
    
    symbol = sys.argv[1]
    samples = int(sys.argv[2])
    
    service_started = False
    proc = None
    
    try:
        # Check if service is running, start if not
        if not is_service_running():
            proc = start_service()
            service_started = True
        
        # Query quotes
        query_quotes(symbol, samples)
        
    finally:
        # Shutdown if we started the service
        if service_started:
            stop_service()
            if proc:
                proc.terminate()
                proc.wait(timeout=5)

if __name__ == "__main__":
    main()