import pandas as pd
from market_simulator import generate_price_series
from alpha_signal import generate_momentum_signal
from quote_engine import generate_quotes
from execution_simulator import simulate_execution
from risk_manager import compute_risk_metrics
from analyzer import plot_performance

import os

# Create output folder if not exists
os.makedirs("output", exist_ok=True)

def main():
    print("✅ Step 1: Generating market data...")
    df = generate_price_series()
    df.to_csv("output/simulated_market.csv")

    print("✅ Step 2: Generating alpha signal...")
    df['signal'] = generate_momentum_signal(df['mid'], lookback=5)
    df.to_csv("output/market_with_signal.csv")

    print("✅ Step 3: Generating bid/ask quotes...")
    zero_inventory = pd.Series(0, index=df.index)
    quotes = generate_quotes(df['mid'], df['signal'], zero_inventory)
    df['quoted_bid'] = quotes['bid']
    df['quoted_ask'] = quotes['ask']
    df.to_csv("output/market_with_quotes.csv")

    print("✅ Step 4: Simulating trade executions...")
    df = simulate_execution(df, fill_probability=0.2)
    df.to_csv("output/executed_trades.csv")

    print("✅ Step 5: Computing risk metrics...")
    metrics = compute_risk_metrics(df)
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    print("✅ Step 6: Plotting performance...")
    plot_performance(df)
    print("✅ All done!")

# Only run the code under this block if the file is being run directly, not when it’s being imported as a module.
if __name__ == "__main__":
    main()
