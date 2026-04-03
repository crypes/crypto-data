#!/usr/bin/env python3
"""
HDBSCAN clustering on BTC-USD 1m price sequences.
"""
import pandas as pd
import numpy as np
import hdbscan

# Configurable window size (minutes)
window_minutes = 10

# Load data
csv_path = '/root/.openclaw/.openclaw/workspace/btc_usd_1m.csv'
df = pd.read_csv(csv_path)

# Print columns for debugging
print("Columns:", df.columns.tolist())

# Ensure 'Open' column exists
if 'open' not in df.columns.str.lower():
    raise ValueError("No 'Open' column found!")

# Normalize column names to lowercase for easier access
df.columns = df.columns.str.lower()

# Use 'timestamp' column; ensure it's present
if 'timestamp' not in df.columns:
    raise ValueError("No 'timestamp' column found!")

print(f"Loaded {len(df)} rows")
print(f"Window minutes: {window_minutes}")

# Build rolling sequences
sequences = []
start_timestamps = []
start_prices = []
final_log_values = []

n_windows = len(df) - window_minutes + 1
for i in range(n_windows):
    window = df.iloc[i:i + window_minutes]
    start_timestamp = int(window['timestamp'].iloc[0])
    start_price = window['open'].iloc[0]
    
    # Log returns relative to start price
    seq = np.log(window['open'].values) - np.log(start_price)
    
    sequences.append(seq)
    start_timestamps.append(start_timestamp)
    start_prices.append(start_price)
    final_log_values.append(seq[-1])

# Convert to 2D numpy array
sequences_array = np.array(sequences)
print(f"Sequences array shape: {sequences_array.shape}")

# Cluster with HDBSCAN
clusterer = hdbscan.HDBSCAN(min_cluster_size=10, min_samples=5)
labels = clusterer.fit_predict(sequences_array)

# Build result DataFrame
result_df = pd.DataFrame({
    'cluster': labels,
    'start_timestamp': start_timestamps,
    'start_price': start_prices,
    'final_log_value': final_log_values
})

# Save to CSV
output_path = '/root/.openclaw/.openclaw/workspace/btc_usd_1m_hdbscan_price_sequence_clusters.csv'
result_df.to_csv(output_path, index=False)
print(f"Saved to {output_path}")

# Print some stats
print(f"Number of clusters (excluding noise): len(set(labels)) - (1 if -1 in labels else 0)")
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print(f"Clusters: {n_clusters}, Noise points: {np.sum(labels == -1)}")