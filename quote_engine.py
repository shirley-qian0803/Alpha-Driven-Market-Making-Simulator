import pandas as pd
import numpy as np
# A quote is the price at which a market participant is willing to buy (bid) or sell (ask) an asset.
def generate_quotes(mid_prices: pd.Series, signals: pd.Series, inventory: pd.Series, 
                    base_spread: float = 0.05, inventory_penalty: float = 0.01, signal_strength: float = 0.02) -> pd.DataFrame:
    """
    Generate dynamic bid and ask quotes based on mid price, alpha signal, and current inventory.

    Parameters
    ----------
    mid_prices : pd.Series
        Series of mid prices.
    signals : pd.Series
        Alpha signal values (e.g., momentum signal in range [-1, 1]).
    inventory : pd.Series
        Series representing the current inventory position at each timestep.
    base_spread : float
        The minimum fixed spread between bid and ask.
    inventory_penalty : float
        Sensitivity to inventory level (more inventory -> wider or skewed quotes).
    signal_strength : float
        How aggressively the signal biases the bid/ask quotes.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns 'bid' and 'ask' representing the quoted prices at each timestep.
    """
    # Inventory ↑ Want to sell more → lower quotes
    # bid ↓, ask ↓
    # Signal ↑  Expect price rise → raise quotes
    # bid ↑, ask ↑

    # Add risk-weighted inventory penalty (penalty = inventory × volatility).
    rolling_volatility = mid_prices.rolling(window=10).std().fillna(0)
    adj_vol = 1 + rolling_volatility

    bid = mid_prices - base_spread / 2 - inventory * inventory_penalty * adj_vol + signals * signal_strength
    ask = mid_prices + base_spread / 2 - inventory * inventory_penalty * adj_vol + signals * signal_strength

    # Set position limits to prevent overexposure.
    max_inventory = 10  # Example limit, can be adjusted based on strategy
    for t in range(len(inventory)):
        if inventory[t] >= max_inventory:
            # flatten quote: don't buy more
            bid[t] = np.nan
        elif inventory[t] <= -max_inventory:
            # flatten quote: don't sell more
            ask[t] = np.nan

    return pd.DataFrame({ 'bid': bid, 'ask': ask })

if __name__ == "__main__":
    df = pd.read_csv("output/market_with_signal.csv", index_col="minute")
    inventory = pd.Series(0, index=df.index)  # placeholder: assume 0 inventory
    quotes = generate_quotes(df['mid'], df['signal'], inventory)
    df['quoted_bid'] = quotes['bid']
    df['quoted_ask'] = quotes['ask']
    df.to_csv("market_with_quotes.csv")
    print("Quotes generated and saved.")
