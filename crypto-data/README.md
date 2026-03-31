# Crypto Data

Historical and real-time cryptocurrency price data with REST API service.

## Overview

This repository contains:
- **BTC-USD historical data** (1-minute OHLCV) in `btc_usd_1m.csv`
- **Flask REST API service** for querying stored quotes
- **CLI tool** for querying quotes from command line

## Data Format

CSV columns:
- `timestamp` - Unix timestamp
- `datetime` - ISO datetime (UTC)
- `open`, `high`, `low`, `close` - OHLC prices (USD)
- `volume` - Trading volume

## Quick Start

### 1. Run the Service

```bash
python3 crypto_data_service.py
```

The service runs on `http://localhost:5000`

### 2. Query via REST API

```bash
# Get 10 minutes of BTC-USD quotes starting at given time
curl "http://localhost:5000/api/quotes?symbol=BTC-USD&start=2026-03-31%2002:00:00&minutes=10"

# List available symbols
curl "http://localhost:5000/api/symbols"

# Health check
curl "http://localhost:5000/health"
```

### 3. Query via CLI

```bash
# Query 5 samples (at 1-minute intervals)
python3 query_quotes.py BTC-USD 5
```

Output example:
```
2026-03-31 02:55:00 | BTC-USD | O:68123.45 H:68150.00 L:68100.00 C:68125.00 V:1450000
2026-03-31 02:56:00 | BTC-USD | O:68125.00 H:68160.00 L:68120.00 C:68145.00 V:1500000
...
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/quotes` | GET | Get quotes by symbol, start time, and minute count |
| `/api/symbols` | GET | List available crypto symbols |
| `/api/shutdown` | POST | Gracefully stop the service (saves CSV) |
| `/health` | GET | Health check |

### Quote Parameters

- `symbol` - Crypto symbol (e.g., `BTC-USD`)
- `start` - Start datetime (format: `YYYY-MM-DD HH:MM:SS`)
- `minutes` - Number of minutes to fetch

## Updating Data

The service automatically:
- Fetches new data from CryptoCompare API every 1 minute
- Saves the database to CSV every hour

### Manual Update

```bash
python3 update_dataset.py
```

## Service Management

### Start
```bash
python3 crypto_data_service.py &
```

### Stop
```bash
curl -X POST http://localhost:5000/api/shutdown
```

## Requirements

- Python 3.8+
- Flask
- SQLite (built-in)

Install dependencies:
```bash
pip install flask
```

## Data Source

Data is fetched from [CryptoCompare](https://www.cryptocompare.com/) API.

## License

MIT