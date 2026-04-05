# frozen_string_literal: true

# Real‑time crypto quotes using CoinGecko public API.
# No API key needed – the basic endpoints are free.
#
# Usage: ruby crypto_quotes.rb
# Press Ctrl‑C to stop.

require "net/http"
require "uri"
require "json"

COINGECKO_API = "https://api.coingecko.com/api/v3"

# Map coin IDs to friendly labels
COINS = {
  "bitcoin"   => "BTC-USD",
  "ethereum"  => "ETH-USD",
  "solana"    => "SOL-USD"
}

def fetch_prices
  ids = COINS.keys.join(",")
  uri = URI("#{COINGECKO_API}/simple/price?ids=#{ids}&vs_currencies=usd")
  response = Net::HTTP.get(uri)
  data = JSON.parse(response)
  data.transform_keys! { |k| COINS[k] }
end

puts "Fetching real‑time prices from CoinGecko (Ctrl‑C to stop)..."
loop do
  begin
    prices = fetch_prices
    prices.each do |label, value|
      puts "#{label}: $#{value["usd"]}"
    end
  rescue => e
    puts "Error: #{e.message}"
  end
  sleep 2
end