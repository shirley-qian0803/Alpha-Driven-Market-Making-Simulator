import pandas as pd

def compute_risk_metrics(df: pd.DataFrame) -> dict:
    """
    Compute basic risk metrics for the trading strategy.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns 'pnl', 'inventory', and 'mid'.

    Returns
    -------
    dict
        Dictionary of risk metrics including:
        - total_pnl
        - max_drawdown
        - sharpe_ratio
        - average_inventory
        - max_inventory
    """
    pnl = df['pnl']
    returns = pnl.diff().fillna(0)

    total_pnl = pnl.iloc[-1]
    drawdown = pnl - pnl.cummax()
    max_drawdown = drawdown.min()

    if returns.std() > 0:
        sharpe_ratio = returns.mean() / returns.std() * (252 * 390) ** 0.5  # annualized
    else:
        sharpe_ratio = float('nan')

    average_inventory = df['inventory'].mean()
    max_inventory = df['inventory'].abs().max()

    return {
        'total_pnl': total_pnl,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'average_inventory': average_inventory,
        'max_inventory': max_inventory
    }

if __name__ == "__main__":
    df = pd.read_csv("output/executed_trades.csv", index_col="minute")
    metrics = compute_risk_metrics(df)
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")
