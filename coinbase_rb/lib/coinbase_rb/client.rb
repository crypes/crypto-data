# frozen_string_literal: true

require "json"
require "faye/websocket"

module CoinbaseRb
  class Client
    BASE_URL = "wss://ws-feed.exchange.coinbase.com".freeze

    attr_reader :subscriptions, :ws

    def initialize
      @subscriptions = {}
      @callbacks = {
        message: [],
        ticker: [],
        trade: [],
        error: [],
        close: []
      }
      @connected = false
    end

    def connect
      @ws = Faye::WebSocket::Client.new(BASE_URL)

      @ws.on :open do
        @connected = true
      end

      @ws.on :message do |event|
        begin
          data = JSON.parse(event.data)
          handle_message(data)
        rescue => e
          emit(:error, e)
        end
      end

      @ws.on :close do
        @connected = false
        emit(:close)
      end

      @ws.on :error do |event|
        emit(:error, event.message)
      end

      # Wait for connection
      sleep 1

      self
    end

    def on_message(&block)
      @callbacks[:message] << block
    end

    def on_ticker(&block)
      @callbacks[:ticker] << block
    end

    def on_trade(&block)
      @callbacks[:trade] << block
    end

    def on_error(&block)
      @callbacks[:error] << block
    end

    def on_close(&block)
      @callbacks[:close] << block
    end

    def subscribe(product_ids:, channels:)
      msg = {
        type: "subscribe",
        product_ids: product_ids,
        channels: channels
      }
      @ws.send(msg.to_json)
      @subscriptions[channels] = product_ids
    end

    def subscribe_ticker(product_ids:)
      subscribe(product_ids: product_ids, channels: ["ticker"])
    end

    def subscribe_trades(product_ids:)
      subscribe(product_ids: product_ids, channels: ["matches"])
    end

    def subscribe_level2(product_ids:)
      subscribe(product_ids: product_ids, channels: ["level2"])
    end

    def unsubscribe(channels:)
      msg = {
        type: "unsubscribe",
        channels: channels
      }
      @ws.send(msg.to_json)
      @subscriptions.delete(channels)
    end

    def close
      @ws.close
      @connected = false
    end

    def connected?
      @connected
    end

    private

    def emit(event, *args)
      @callbacks[event]&.each { |cb| cb.call(*args) }
    end

    def handle_message(data)
      type = data["type"]

      case type
      when "ticker"
        emit(:ticker, data)
      when "match", "last_match"
        emit(:trade, data)
      when "subscriptions"
        # Confirmation of subscription
      when "error"
        emit(:error, data)
      end

      emit(:message, data)
    end
  end

  module Ticker
    class << self
      def price(data)
        data["price"].to_f
      end

      def product_id(data)
        data["product_id"]
      end

      def side(data)
        data["side"]
      end

      def open_24h(data)
        data["open_24h"].to_f
      end

      def volume_24h(data)
        data["volume_24h"].to_f
      end

      def low_24h(data)
        data["low_24h"].to_f
      end

      def high_24h(data)
        data["high_24h"].to_f
      end
    end
  end
end