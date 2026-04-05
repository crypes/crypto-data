#!/usr/bin/env ruby
# frozen_string_literal: true

# Test full workflow with new demo credentials

$LOAD_PATH.unshift(File.expand_path("kalshi-api-rb/lib", __dir__))

require "kalshi_rb"

KEY_ID = "7099ccd8-c6cd-4286-affc-a6aa40b95190"
PRIVATE_KEY_PATH = "/root/.openclaw/.openclaw/secrets/kalshi_demo_new.pem"

key = File.read(PRIVATE_KEY_PATH)
client = KalshiRb::Client.new(key_id: KEY_ID, private_key: key, env: :demo)

puts "=== Step 1: Check balance ==="
balance = KalshiRb::Portfolio.balance(client)
puts balance.inspect
puts

puts "=== Step 2: List markets (open, limit 5) ==="
markets = KalshiRb::Markets.list(client, status: "open", limit: 5)
puts markets.inspect
puts

# Find a market with liquidity
ticker = nil
if markets["markets"]
  markets["markets"].each do |m|
    if m["yes_bid_dollars"].to_f > 0 || m["yes_ask_dollars"].to_f > 0
      ticker = m["ticker"]
      puts "Selected market: #{ticker}"
      puts m.inspect
      break
    end
  end
end

if !ticker
  puts "No market with liquidity found, using first market"
  ticker = markets["markets"]&.first&.dig("ticker")
end

puts
puts "=== Step 3: Get orderbook for #{ticker} ==="
orderbook = KalshiRb::Markets.get_orderbook(client, ticker)
puts orderbook.inspect
puts

# Parse orderbook - handle both old and new format
yes_bids = orderbook["buy_orders"] || orderbook.dig("orderbook_fp", "yes_dollars") || []
yes_asks = orderbook["sell_orders"] || orderbook.dig("orderbook_fp", "no_dollars") || []

puts "Yes bids: #{yes_bids.inspect}"
puts "Yes asks: #{yes_asks.inspect}"

# Get best prices
best_bid = yes_bids.is_a?(Array) && yes_bids.first.is_a?(Hash) ? yes_bids.first["price"] : (yes_bids.first&.first)
best_ask = yes_asks.is_a?(Array) && yes_asks.first.is_a?(Hash) ? yes_asks.first["price"] : (yes_asks.first&.first)

puts "Best bid: #{best_bid}, Best ask: #{best_ask}"
puts

# Step 4: Place a buy order if we have an ask
order_id = nil
if best_ask
  order_params = {
    ticker: ticker,
    side: "buy",
    type: "limit",
    price: best_ask.to_i,
    count: 1
  }
  puts "=== Step 4: Place buy order ==="
  puts "Params: #{order_params.inspect}"
  result = KalshiRb::Orders.place(client, order_params)
  puts result.inspect
  order_id = result["order_id"]
  puts "Order ID: #{order_id}"
  puts
end

# Step 5: Check order status
if order_id
  puts "=== Step 5: Get order status ==="
  status = KalshiRb::Orders.get(client, order_id)
  puts status.inspect
  puts
end

# Step 6: Check balance again
puts "=== Step 6: Check balance after order ==="
balance2 = KalshiRb::Portfolio.balance(client)
puts balance2.inspect
puts

# Step 7: Check positions
puts "=== Step 7: Check positions ==="
positions = KalshiRb::Portfolio.positions(client)
puts positions.inspect
puts

# Step 8: Cancel order if still open
if order_id
  puts "=== Step 8: Cancel order ==="
  cancel = KalshiRb::Orders.cancel(client, order_id)
  puts cancel.inspect
  puts
end

# Step 9: Final balance check
puts "=== Step 9: Final balance ==="
balance3 = KalshiRb::Portfolio.balance(client)
puts balance3.inspect
puts

puts "=== Workflow complete ==="