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

def compute_momentum_signal(price: pd.Series, lookback: int = 5) -> pd.Series:
    """
    Generate a simple momentum signal based on price difference over a lookback window.
    Use Exponential Moving Average (EMA) to smooth noisy momentum signals.

    An Exponential Moving Average is a weighted average where more recent values have more influence than older ones.
    This makes it more responsive to changes compared to a simple moving average (SMA), which weights all past values equally.
    The formula for EMA is:
    EMA = (price - EMA(previous day)) * alpha + EMA(previous day)
    where alpha = 2 / (N + 1) and N is the lookback period.

    Parameters:
    ----------
    price: pd.Series
        Price series
    lookback: int
        Lookback window for momentum calculation

    Returns:
    ----------
    pd.Series
        Momentum signal
    """
    raw_momentum = price.diff(lookback)
    smoothed_momentum = raw_momentum.ewm(span=10, adjust=False).mean()
    return np.tanh(smoothed_momentum / price.rolling(lookback).std()).fillna(0)

def compute_ma_crossover_signal(price: pd.Series, short: int = 5, long: int = 20) -> pd.Series:
    """
    Generate a moving average crossover signal.
    A moving average crossover occurs when a short-term moving average crosses above or below a long-term moving average.

    Parameters:
    ----------
    price: pd.Series
        Price series
    short: int
        Short-term window for moving average
    long: int
        Long-term window for moving average

    Returns:
    ----------
    pd.Series
        Crossover signal where:
        - Positive values indicate a bullish crossover (short MA crosses above long MA)
        - Negative values indicate a bearish crossover (short MA crosses below long MA)
    """
    short_ma = price.rolling(window=short).mean()
    long_ma = price.rolling(window=long).mean()
    crossover = short_ma - long_ma
    return np.tanh(crossover / price.rolling(long).std()).fillna(0)

def compute_rsi_signal(price: pd.Series, period: int = 14) -> pd.Series:
    """
    Compute the Relative Strength Index (RSI) signal.
    The RSI is a momentum oscillator that measures the speed and change of price movements.
    It ranges from 0 to 100 and is typically used to identify overbought or oversold conditions.
    A common threshold is 70 for overbought and 30 for oversold conditions.
    This function normalizes the RSI to a range of -1 to 1 for easier interpretation in trading signals.
    Parameters:
    ----------
    price: pd.Series
        Price series
    period: int
        Period for RSI calculation

    Returns:
    ----------
    pd.Series
        RSI series
    """
    delta = price.diff()
    gain = delta.clip(lower=0) # Keeps only positive price changes. Negative changes are set to 0.
    loss = -delta.clip(upper=0) # Keeps only negative price changes. Positive changes are set to 0.
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / (avg_loss + 1e-9) # Add 1e-9 to avoid divide-by-zero.
    rsi = 100 - (100 / (1 + rs))
    # But if you’re going to apply np.tanh() after, 
    # you actually want smaller input magnitudes to avoid over-flattening the signal.
    # However, the signal can't be too week. Between 2 and -2 is a good range.
    return np.tanh((rsi - 50) / 10).fillna(0)

def compute_volatility_breakout_signal(price: pd.Series, window: int = 20) -> pd.Series:
    rolling_high = price.rolling(window).max()
    rolling_low = price.rolling(window).min()
    signal = (price > rolling_high).astype(int) - (price < rolling_low).astype(int)
    return signal.fillna(0)

def generate_combined_signal(price: pd.Series) -> pd.Series:
    momentum = compute_momentum_signal(price)
    crossover = compute_ma_crossover_signal(price)
    rsi = compute_rsi_signal(price)
    breakout = compute_volatility_breakout_signal(price)

    combined = (
        0.4 * momentum +
        0.3 * crossover +
        0.2 * rsi +
        0.1 * breakout
    )
    return np.tanh(combined).fillna(0)

if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("simulated_market.csv", index_col="minute")
    signal = generate_combined_signal(df['mid'], lookback=5)
    df['signal'] = signal
    df.to_csv("output/market_with_signal.csv")
    print("Alpha signal added to market data.")
