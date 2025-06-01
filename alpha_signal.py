import pandas as pd
import numpy as np

def generate_momentum_signal(price_series: pd.Series, lookback: int = 5) -> pd.Series:
    """
    Generate a simple momentum signal based on price difference over a lookback window.

    Parameters
    ----------
    price_series : pd.Series
        Series of mid prices.
    lookback : int
        Number of time steps to look back for momentum calculation.

    Returns
    -------
    pd.Series
        Signal values between -1 and 1 representing directional momentum:
        - Positive values suggest upward momentum
        - Negative values suggest downward momentum
    """
    # Diff() computes the difference between the current price and the price lookback periods ago.
    # If lookback = 5, then: momentum[t] = price_series[t] - price_series[t - 5]
    momentum = price_series.diff(lookback)
    # Normalizes the momentum signal by volatility → higher signal if strong move & low volatility
    # This helps prevent false signals in high-volatility conditions. reduce the effect of noise
    normalized_signal = np.tanh(momentum / price_series.rolling(lookback).std()) # tanh keeps value between 1 and -1
    return normalized_signal.fillna(0)

if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("simulated_market.csv", index_col="minute")
    signal = generate_momentum_signal(df['mid'], lookback=5)
    df['signal'] = signal
    df.to_csv("market_with_signal.csv")
    print("Alpha signal added to market data.")
