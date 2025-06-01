import pandas as pd
import matplotlib.pyplot as plt

def plot_performance(df: pd.DataFrame, output_prefix="performance"):
    """
    Plot trading performance over time including PnL, inventory, and trade executions.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing 'pnl', 'inventory', 'mid', and 'execution' columns.
    output_prefix : str
        Prefix for the saved plot image files.
    """
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # Plot PnL
    axs[0].plot(df.index, df['pnl'], label="PnL", color="green")
    axs[0].set_ylabel("PnL ($)")
    axs[0].set_title("Cumulative PnL Over Time")
    axs[0].grid(True)

    # Plot inventory
    axs[1].plot(df.index, df['inventory'], label="Inventory", color="blue")
    axs[1].set_ylabel("Inventory")
    axs[1].set_title("Inventory Position Over Time")
    axs[1].grid(True)

    # Plot mid price and trades
    axs[2].plot(df.index, df['mid'], label="Mid Price", color="gray", alpha=0.5)
    buy_signals = df[df['execution'] == 'buy']
    sell_signals = df[df['execution'] == 'sell']
    axs[2].scatter(buy_signals.index, buy_signals['mid'], color='green', label='Buy', marker='^', alpha=0.8)
    axs[2].scatter(sell_signals.index, sell_signals['mid'], color='red', label='Sell', marker='v', alpha=0.8)
    axs[2].set_ylabel("Price")
    axs[2].set_title("Trade Executions Over Time")
    axs[2].legend()
    axs[2].grid(True)

    plt.xlabel("Time (Minute)")
    plt.tight_layout()
    plt.savefig(f"output/{output_prefix}_summary.png")
    plt.close()

if __name__ == "__main__":
    df = pd.read_csv("output/executed_trades.csv", index_col="minute")
    plot_performance(df)
    print("Performance plots saved.")
