#!/usr/bin/env python3
"""
Crypto Data Service
- Loads CSV data into SQLite
- Provides REST API for quote queries
- Periodically updates data from API
- Periodically saves to CSV
"""

import csv
import os
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import urllib.request
import json

app = Flask(__name__)

# Config
DB_PATH = "/root/.openclaw/.openclaw/workspace/crypto_data.db"
CSV_PATH = "/root/.openclaw/.openclaw/workspace/btc_usd_1m.csv"
API_URL = "https://min-api.cryptocompare.com/data/v2/histominute"
UPDATE_INTERVAL = 60  # 1 minute
CSV_SAVE_INTERVAL = 3600  # 1 hour

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Quotes table
    c.execute('''CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        datetime TEXT NOT NULL,
        open REAL NOT NULL,
        high REAL NOT NULL,
        low REAL NOT NULL,
        close REAL NOT NULL,
        volume REAL NOT NULL,
        UNIQUE(symbol, timestamp)
    )''')
    
    # Create index for fast queries
    c.execute('''CREATE INDEX IF NOT EXISTS idx_symbol_timestamp 
                 ON quotes(symbol, timestamp)''')
    
    conn.commit()
    conn.close()

def load_csv_to_db():
    """Load CSV data into SQLite"""
    if not os.path.exists(CSV_PATH):
        print(f"CSV not found: {CSV_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    count = 0
    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                c.execute('''INSERT OR IGNORE INTO quotes 
                    (symbol, timestamp, datetime, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    ('BTC-USD', int(row['timestamp']), row['datetime'],
                     float(row['open']), float(row['high']), float(row['low']),
                     float(row['close']), float(row['volume']))
                )
                count += 1
            except Exception as e:
                print(f"Error inserting row: {e}")
    
    conn.commit()
    conn.close()
    print(f"Loaded {count} rows from CSV")

def fetch_latest_from_api(symbol='BTC', limit=60):
    """Fetch latest data from CryptoCompare"""
    url = f"{API_URL}?fsym={symbol}&tsym=USD&limit={limit}"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            if data.get("Response") == "Success":
                return data["Data"]["Data"]
    except Exception as e:
        print(f"API fetch error: {e}")
    return []

def update_db_from_api():
    """Fetch latest data and add to database"""
    data = fetch_latest_from_api('BTC', 100)
    if not data:
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    count = 0
    for d in data:
        try:
            dt = datetime.utcfromtimestamp(d['time']).strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''INSERT OR IGNORE INTO quotes 
                (symbol, timestamp, datetime, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                ('BTC-USD', d['time'], dt, d['open'], d['high'], 
                 d['low'], d['close'], d.get('volumeto', 0))
            )
            count += 1
        except Exception as e:
            pass
    
    conn.commit()
    conn.close()
    if count > 0:
        print(f"Added {count} new quotes from API")

def save_db_to_csv():
    """Export database to CSV"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''SELECT symbol, timestamp, datetime, open, high, low, close, volume
                 FROM quotes ORDER BY timestamp''')
    
    with open(CSV_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'datetime', 'open', 'high', 'low', 'close', 'volume'])
        for row in c.fetchall():
            writer.writerow([row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
    
    conn.close()
    print(f"Saved database to {CSV_PATH}")

# Background update threads
def start_background_updates():
    # Periodic API updates
    def api_updater():
        while True:
            update_db_from_api()
            time.sleep(UPDATE_INTERVAL)
    
    # Periodic CSV saves
    def csv_saver():
        while True:
            save_db_to_csv()
            time.sleep(CSV_SAVE_INTERVAL)
    
    t1 = threading.Thread(target=api_updater, daemon=True)
    t2 = threading.Thread(target=csv_saver, daemon=True)
    t1.start()
    t2.start()

# REST API
@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    """Get quotes by symbol, start datetime, and minutes"""
    symbol = request.args.get('symbol', 'BTC-USD')
    start_dt = request.args.get('start')
    minutes = int(request.args.get('minutes', 60))
    
    if not start_dt:
        return jsonify({"error": "start parameter required (YYYY-MM-DD HH:MM:SS)"}), 400
    
    try:
        start_time = datetime.strptime(start_dt, '%Y-%m-%d %H:%M:%S')
        end_time = start_time + timedelta(minutes=minutes)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('''SELECT * FROM quotes 
                 WHERE symbol = ? AND timestamp >= ? AND timestamp < ?
                 ORDER BY timestamp''',
              (symbol, int(start_time.timestamp()), int(end_time.timestamp())))
    
    rows = c.fetchall()
    conn.close()
    
    quotes = [dict(row) for row in rows]
    # Remove internal id
    for q in quotes:
        q.pop('id', None)
    
    return jsonify({
        "symbol": symbol,
        "start": start_dt,
        "minutes": minutes,
        "count": len(quotes),
        "quotes": quotes
    })

@app.route('/api/symbols', methods=['GET'])
def get_symbols():
    """List available symbols"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT DISTINCT symbol FROM quotes ORDER BY symbol")
    symbols = [row[0] for row in c.fetchall()]
    conn.close()
    return jsonify({"symbols": symbols})

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM quotes")
    count = c.fetchone()[0]
    conn.close()
    return jsonify({"status": "ok", "quotes_count": count})

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """Graceful shutdown: save CSV and exit"""
    from flask import request
    print("Shutdown requested...")
    
    # Save to CSV
    save_db_to_csv()
    
    # Schedule server shutdown after response
    def shutdown_server():
        import os
        os._exit(0)
    
    # Use Flask's internal shutdown or exit
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()
    else:
        import threading
        threading.Timer(1, shutdown_server).start()
    
    # Return response before exiting
    return jsonify({"status": "shutting_down", "message": "CSV saved, service stopping"})

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Loading CSV data...")
    load_csv_to_db()
    print("Starting background updates...")
    start_background_updates()
    print("Starting Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)