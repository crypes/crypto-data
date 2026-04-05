# frozen_string_literal: true

# BTC-USD Volatility & Price Prediction Neural Network
# Uses Ruby with Torch
#
# Input: 60 minutes of OHLCV data
# Output: volatility (std dev of returns) and price at t+15

require "torch"
require "csv"

DATA_PATH = "/root/.openclaw/.openclaw/workspace/btc_usd_1m.csv"
LOOKBACK = 60      # 60 minutes of history
FORWARD = 15       # Predict 15 minutes ahead

# Load and preprocess data
def load_data(path)
  data = []
  CSV.foreach(path, headers: true) do |row|
    data << {
      open: row["open"].to_f,
      high: row["high"].to_f,
      low: row["low"].to_f,
      close: row["close"].to_f,
      volume: row["volume"].to_f
    }
  end
  data
end

# Normalize data using min-max scaling
def normalize(data)
  closes = data.map { |d| d[:close] }
  min_val = closes.min
  max_val = closes.max
  range = max_val - min_val
  
  data.map do |d|
    {
      open: range.zero? ? 0 : (d[:open] - min_val) / range,
      high: range.zero? ? 0 : (d[:high] - min_val) / range,
      low: range.zero? ? 0 : (d[:low] - min_val) / range,
      close: range.zero? ? 0 : (d[:close] - min_val) / range,
      volume: d[:volume] # volume not normalized for now
    }
  end
end

# Create features: 60-minute lookback window
def create_features(data, lookback, forward)
  x = [] # input features
  y_vol = [] # volatility target
  y_price = [] # price target
  
  (lookback...data.length - forward).each do |i|
    window = data[i - lookback...i]
    
    # Features: open, high, low, close, volume for each minute
    features = window.flat_map { |d| [d[:open], d[:high], d[:low], d[:close], d[:volume]] }
    
    # Target: volatility (std dev of returns) and forward price
    forward_prices = data[i...i + forward].map { |d| d[:close] }
    returns = forward_prices.each_cons(2).map { |a, b| (b - a) / a }
    volatility = returns.sum.zero? ? 0.0 : Math.sqrt(returns.map { |r| r**2 }.sum / returns.size)
    forward_price = forward_prices.last
    
    x << features
    y_vol << volatility
    y_price << forward_price
  end
  
  [x, y_vol, y_price]
end

# Simple Neural Network model
class PredictionModel < Torch::NN::Module
  def initialize(input_size)
    super()
    @fc1 = Torch::NN::Linear.new(input_size, 128)
    @fc2 = Torch::NN::Linear.new(128, 64)
    @fc3 = Torch::NN::Linear.new(64, 32)
    @fc4_vol = Torch::NN::Linear.new(32, 1)   # volatility head
    @fc4_price = Torch::NN::Linear.new(32, 1) # price head
    @relu = Torch::NN::ReLU.new
    @dropout = Torch::NN::Dropout.new(0.2)
  end

  def forward(x)
    x = @relu.(@fc1.(x))
    x = @dropout.(@relu.(@fc2.(x)))
    x = @relu.(@fc3.(x))
    volatility = @fc4_vol.(x)
    price = @fc4_price.(x)
    [volatility, price]
  end
end

# Main training loop
puts "Loading data..."
data = load_data(DATA_PATH)
puts "Loaded #{data.length} data points"

puts "Normalizing..."
normalized = normalize(data)

puts "Creating features (lookback: #{LOOKBACK}, forward: #{FORWARD})..."
x, y_vol, y_price = create_features(normalized, LOOKBACK, FORWARD)
puts "Training samples: #{x.length}"

# Convert to tensors
x_tensor = Torch.tensor(x, dtype: :float)
y_vol_tensor = Torch.tensor(y_vol, dtype: :float).reshape([-1, 1])
y_price_tensor = Torch.tensor(y_price, dtype: :float).reshape([-1, 1])

# Train/val split (80/20)
split = (x.length * 0.8).to_i
x_train, x_val = x_tensor[0...split], x_tensor[split..-1]
y_vol_train, y_vol_val = y_vol_tensor[0...split], y_vol_tensor[split..-1]
y_price_train, y_price_val = y_price_tensor[0...split], y_price_tensor[split..-1]

puts "Training set: #{x_train.shape[0]}, Validation: #{x_val.shape[0]}"

# Model
model = PredictionModel.new(LOOKBACK * 5)
optimizer = Torch::ADAM.new(model.parameters, lr: 0.001)
mse = Torch::NN::MSELoss.new

# Training
epochs = 50
batch_size = 32

puts "Starting training..."
epochs.times do |epoch|
  model.train
  
  # Mini-batch training
  total_loss = 0.0
  num_batches = 0
  
  x_train.each_slice(batch_size).each do |batch|
    optimizer.zero_grad
    
    vol_pred, price_pred = model.forward(batch)
    
    loss_vol = mse.call(vol_pred, y_vol_train[0...vol_pred.shape[0]])
    loss_price = mse.call(price_pred, y_price_train[0...price_pred.shape[0]])
    loss = loss_vol + loss_price
    
    loss.backward
    optimizer.step
    
    total_loss += loss.item
    num_batches += 1
  end
  
  # Validation
  model.eval
  val_loss_vol = 0.0
  val_loss_price = 0.0
  Torch.no_grad do
    vol_pred, price_pred = model.forward(x_val)
    val_loss_vol = mse.call(vol_pred, y_vol_val).item
    val_loss_price = mse.call(price_pred, y_price_val).item
  end
  
  if (epoch + 1) % 10 == 0
    puts format("Epoch %d/%d - Train Loss: %.4f, Val Vol: %.4f, Val Price: %.4f", 
                epoch + 1, epochs, total_loss / num_batches, val_loss_vol, val_loss_price)
  end
end

puts "Training complete!"

# Save model
Torch.save(model.state_dict, "/root/.openclaw/.openclaw/workspace/btc_model.pt")
puts "Model saved to btc_model.pt"