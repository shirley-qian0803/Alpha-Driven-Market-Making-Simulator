import numpy as np
import pandas as pd

def generate_price_series(n_minutes=390, initial_price=100.0, daily_vol=0.2, base_spread=0.05):
    """
    You get a sequence of simulated prices where:
	•	The returns follow a normal distribution
	•	The prices follow a log-normal distribution
    r_t = ln(P_t/P_{t-1})

    Parameters
    ----------
    n_minutes : int
        Number of minutes per day (default is 390 for a full trading day).
    initial_price : int 
        Initial price of the asset.
    daily_vol : float 
        The standard deviation of the returns. Annualized daily volatility
    base_spread : float 
        Fixed bid-ask spread to apply around the mid price.

    Returns
    -------
    dataframe
        DataFrame with 'mid', 'bid', and 'ask' prices indexed by time.
    """
    minute_vol = daily_vol / (390 ** 0.5)
    returns = np.random.normal(loc=0, scale=minute_vol, size=n_minutes)
    prices = initial_price * np.exp(np.cumsum(returns))
    bid_prices = prices - base_spread / 2
    ask_prices = prices + base_spread / 2
    df = pd.DataFrame({
        'mid': prices,
        'bid': bid_prices,
        'ask': ask_prices
    })
    df.index.name = 'minute'
    return df

if __name__ == "__main__":
    df = generate_price_series()
    df.to_csv("simulated_market.csv")
    print("Generated simulated market data for one trading day.")