import pandas as pd
import numpy as np

# def simulate_execution(df: pd.DataFrame, fill_probability: float = 0.1) -> pd.DataFrame:
#     """
#     Simulate market order flow hitting the quoted bid/ask prices.

#     Parameters
#     ----------
#     df : pd.DataFrame
#         DataFrame containing columns 'mid', 'signal', 'quoted_bid', 'quoted_ask'.
#     fill_probability : float
#         Probability that an order hits either bid or ask at each time step.

#     Returns
#     -------
#     pd.DataFrame
#         Updated DataFrame with columns:
#         - 'inventory': net position over time
#         - 'cash': cash balance after trades
#         - 'pnl': mark-to-market profit and loss
#         - 'execution': trade direction ("buy", "sell", or None)
#     """
#     inventory = 0
#     cash = 0
#     inventory_history = []
#     cash_history = []
#     execution_log = []

#     for i, row in df.iterrows():
#         # Random chance of market order hitting
#         exec_type = None
#         if np.random.rand() < fill_probability:
#             if np.random.rand() < 0.5:
#                 # Buy order hits our ask → we sell
#                 inventory -= 1
#                 cash += row['quoted_ask']
#                 exec_type = "sell"
#             else:
#                 # Sell order hits our bid → we buy
#                 inventory += 1
#                 cash -= row['quoted_bid']
#                 exec_type = "buy"

#         inventory_history.append(inventory)
#         cash_history.append(cash)
#         execution_log.append(exec_type)

#     df['inventory'] = inventory_history
#     df['cash'] = cash_history
#     df['execution'] = execution_log
#     df['pnl'] = df['cash'] + df['inventory'] * df['mid']
#     return df

# if __name__ == "__main__":
#     df = pd.read_csv("output/market_with_quotes.csv", index_col="minute")
#     df = simulate_execution(df, fill_probability=0.2)
#     df.to_csv("executed_trades.csv")
#     print("Execution simulation completed and saved.")


# Still need more improvements as it's too basic rn.

# import numpy as np
# import pandas as pd

def simulate_execution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate market order flow with dynamic fill probabilities based on quote aggressiveness.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'mid', 'quoted_bid', 'quoted_ask'.

    Returns
    -------
    pd.DataFrame
        DataFrame with 'inventory', 'cash', 'execution', and 'pnl'.
    """
    inventory = 0
    cash = 0
    inventory_history = []
    cash_history = []
    execution_log = []

    # Hyperparameter to control sensitivity to distance (tune this)
    aggressiveness_scale = 20.0

    for i, row in df.iterrows():
        mid = row['mid']
        bid = row['quoted_bid']
        ask = row['quoted_ask']

        # Distance from mid
        dist_bid = mid - bid
        dist_ask = ask - mid

        # Fill probabilities: exponential decay based on distance
        prob_bid = np.exp(-aggressiveness_scale * dist_bid)
        prob_ask = np.exp(-aggressiveness_scale * dist_ask)

        exec_type = None
        rand = np.random.rand()
        if rand < prob_ask:
            # Buy order hits our ask → we sell
            inventory -= 1
            cash += ask
            exec_type = "sell"
        elif rand < prob_ask + prob_bid:
            # Sell order hits our bid → we buy
            inventory += 1
            cash -= bid
            exec_type = "buy"

        inventory_history.append(inventory)
        cash_history.append(cash)
        execution_log.append(exec_type)

    df['inventory'] = inventory_history
    df['cash'] = cash_history
    df['execution'] = execution_log
    df['pnl'] = df['cash'] + df['inventory'] * df['mid']
    return df

if __name__ == "__main__":
    df = pd.read_csv("output/market_with_quotes.csv", index_col="minute")
    df = simulate_execution(df)
    df.to_csv("executed_trades.csv")
    print("✅ Execution simulation completed and saved.")