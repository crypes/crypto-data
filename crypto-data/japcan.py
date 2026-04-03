#!/usr/bin/env python3
"""
Japcan clustering experiment.
Generate 5-minute sliding window vectors from BTC-USD 1m data,
perform HDBSCAN clustering, and save results with price stats.
"""

import numpy as np
import pandas as pd
import hdbscan
import os

# Configuration
CSV_PATH = '/root/.openclaw/.openclaw/workspace/btc_usd_1m.csv'
WINDOW_SIZE = 5  # minutes
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'japcan.csv')

# Load data
print(f"Loading data from {CSV_PATH}")
df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.lower()
print(f"Loaded {len(df)} rows")

# Ensure needed columns exist
required = {'timestamp', 'open', 'high', 'low', 'close'}
if not required.issubset(df.columns):
    raise ValueError(f"Missing columns: {required - set(df.columns)}")

# Sort by timestamp to be safe
df = df.sort_values('timestamp').reset_index(drop=True)

# Number of complete windows
n_windows = len(df) - WINDOW_SIZE + 1
print(f"Creating {n_windows} windows of size {WINDOW_SIZE}")

# Prepare containers
vectors = []  # for clustering
records = []  # for output CSV

for i in range(n_windows):
    window = df.iloc[i:i + WINDOW_SIZE]
    
    # First timestamp and open price
    first_ts = int(window['timestamp'].iloc[0])
    first_open = window['open'].iloc[0]
    
    # Log of first open
    log_open0 = np.log(first_open)
    
    # Build 15-dim vector: log(H), log(L), log(C) for each of 5 minutes, minus log(first_open)
    vec = []
    for _, row in window.iterrows():
        vec.append(np.log(row['high']) - log_open0)   # log(H) - log(O0)
        vec.append(np.log(row['low']) - log_open0)    # log(L) - log(O0)
        vec.append(np.log(row['close']) - log_open0)  # log(C) - log(O0)
    
    vectors.append(vec)
    
    # Compute stats for output
    high_max = window['high'].max()
    low_min = window['low'].min()
    close_last = window['close'].iloc[-1]  # last close in window
    
    high_pct = (high_max / first_open) * 100.0
    low_pct = (low_min / first_open) * 100.0
    close_pct = (close_last / first_open) * 100.0
    
    records.append({
        'timestamp': first_ts,
        'open': first_open,
        'high': high_max,
        'high_pct': high_pct,
        'low': low_min,
        'low_pct': low_pct,
        'close': close_last,
        'close_pct': close_pct
    })

# Convert to numpy array for clustering
vectors_arr = np.array(vectors)
print(f"Feature matrix shape: {vectors_arr.shape}")

# Run HDBSCAN clustering
print("Running HDBSCAN clustering...")
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=8,
    min_samples=4,
    cluster_selection_method='leaf',
    metric='euclidean'
)
cluster_labels = clusterer.fit_predict(vectors_arr)

# Add cluster labels to records
for rec, label in zip(records, cluster_labels):
    rec['cluster_id'] = label

# Create output DataFrame
output_df = pd.DataFrame(records)

# Reorder columns for clarity
output_df = output_df[['cluster_id', 'timestamp', 'open', 'high', 'high_pct', 'low', 'low_pct', 'close', 'close_pct']]

# Save to CSV
output_df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved results to {OUTPUT_CSV}")

# Summary stats
n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
print(f"Clusters found (excluding noise): {n_clusters}")
print(f"Noise points: {np.sum(cluster_labels == -1)}")