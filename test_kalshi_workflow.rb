#!/usr/bin/env ruby
# frozen_string_literal: true

# Add the wrapper lib to load path
$LOAD_PATH.unshift(File.expand_path("kalshi-api-rb/lib", __dir__))

require "kalshi_rb"

# Configuration
KEY_ID = "e780f1c0-4fd7-489f-b547-0499a0572ee8"
PRIVATE_KEY_PATH = "/root/.openclaw/.openclaw/secrets/kalshi_demo.pem"

# Initialize client for demo environment
key = File.read(PRIVATE_KEY_PATH)
client = KalshiRb::Client.new(key_id: KEY_ID, private_key: key, env: :demo)

puts "=== Step 1: List markets (open, limit 5) ==="
markets_result = KalshiRb::Markets.list(client, status: "open", limit: 5)
puts markets_result.inspect
puts

# Extract first market ticker
if markets_result["markets"] && !markets_result["markets"].empty?
  first_market = markets_result["markets"].first
  ticker = first_market["ticker"]
  puts "First market ticker: #{ticker}"
  puts "Market details: #{first_market.inspect}"
  puts
else
  puts "No markets found."
  exit 1
end

puts "=== Step 2: Get orderbook for #{ticker} ==="
orderbook = KalshiRb::Markets.get_orderbook(client, ticker)
puts "Orderbook: #{orderbook.inspect}"
puts

# Extract best bid and ask
best_bid = orderbook["buy_orders"]&.first
best_ask = orderbook["sell_orders"]&.first
bid_price = best_bid ? best_bid["price"] : nil
ask_price = best_ask ? best_ask["price"] : nil
puts "Best bid: #{bid_price}, Best ask: #{ask_price}"
puts

# Step 3: Place a buy order at best ask (or mid price) if possible
if ask_price
  # Place a limit buy order at ask price (or slightly lower)
  order_params = {
    ticker: ticker,
    side: "buy",
    type: "limit",
    price: ask_price,
    count: 1
  }
  puts "=== Step 3: Place buy order ==="
  puts "Order params: #{order_params.inspect}"
  order_result = KalshiRb::Orders.place(client, order_params)
  puts "Order result: #{order_result.inspect}"
  order_id = order_result["order_id"]
  puts "Placed order ID: #{order_id}"
  puts
else
  puts "No ask price available, skipping order placement."
  order_id = nil
end

# Step 4: Check order status
if order_id
  puts "=== Step 4: Get order status ==="
  order_status = KalshiRb::Orders.get(client, order_id)
  puts "Order status: #{order_status.inspect}"
  puts
end

# Step 5: Check balance
puts "=== Step 5: Check balance ==="
balance_result = KalshiRb::Portfolio.balance(client)
puts "Balance: #{balance_result.inspect}"
puts

# Step 6: Check positions
puts "=== Step 6: Check positions ==="
positions_result = KalshiRb::Portfolio.positions(client)
puts "Positions: #{positions_result.inspect}"
puts

# Step 7: Cancel order if still open
if order_id
  puts "=== Step 7: Cancel order ==="
  cancel_result = KalshiRb::Orders.cancel(client, order_id)
  puts "Cancel result: #{cancel_result.inspect}"
  puts
end

# Step 8: Check balance again after cancel
puts "=== Step 8: Check balance after cancel ==="
balance_result2 = KalshiRb::Portfolio.balance(client)
puts "Balance: #{balance_result2.inspect}"
puts

puts "=== Workflow complete ==="