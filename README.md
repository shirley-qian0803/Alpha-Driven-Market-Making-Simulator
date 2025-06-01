# Alpha-Driven-Market-Making-Simulator

## 🧠 Project Overview

This project simulates a **quant trader’s decision-making system** that combines **alpha signals** with **market making execution logic**. It models how a trader continuously quotes bid and ask prices, manages inventory risk, and adapts to market conditions to optimize PnL.

The simulator integrates both **quant research** (alpha generation) and **quant trading** (execution, risk control), reflecting how modern electronic traders operate in real financial markets.


## 🎯 Objectives

- Build an **alpha-driven strategy** that dynamically adjusts quotes based on market signals.
- Simulate realistic **order flow, execution, and inventory management**.
- Evaluate strategy performance using key **risk and return metrics**.
- Lay the groundwork for advanced features such as **volatility awareness, stop-loss logic, and machine learning-driven pricing**.



## 🧱 Core Components

### 1. Market Data Engine
Generates or loads price data (e.g. via random walk, historical prices, or order book simulation).

### 2. Alpha Signal Engine
Implements predictive signals to forecast short-term asset returns. Examples include:
- Momentum indicators
- Mean-reversion triggers
- Technical signals (RSI, MACD)
- Statistical or ML models

### 3. Quote Generator
Dynamically generates bid/ask quotes based on:
- Mid price
- Base spread
- Inventory level
- Alpha signal strength

### 4. Execution Simulator
Simulates how market orders hit the trader’s quotes:
- Matches buy/sell orders probabilistically
- Updates inventory and cash
- Models slippage or latency

### 5. Risk & Inventory Manager
Tracks:
- Inventory position
- Cash balance
- Realized + mark-to-market PnL
- Position limits and risk constraints

### 6. Performance Analyzer
Calculates and visualizes:
- PnL over time
- Sharpe ratio
- Max drawdown
- Spread captured
- Signal correlation vs return



## 📊 Key Metrics

| Metric | Description |
|--------|-------------|
| **Total PnL** | Overall strategy profitability |
| **Sharpe Ratio** | Risk-adjusted return |
| **Max Drawdown** | Largest drop in equity |
| **Spread Captured** | Average profit per trade |
| **Inventory Exposure** | Net position drift |
| **Hit Rate** | Proportion of profitable trades |



## 🚀 Advanced Features (To Be Implemented)

| Feature | Description |
|---------|-------------|
| 📈 **Volatility Regimes** | Adjust quote width during high/low volatility periods |
| 🧮 **Signal Confidence** | Scale quote bias based on predictive power |
| 💼 **Multi-Asset Netting** | Manage risk across correlated instruments |
| ⚖️ **Position Sizing** | Dynamically scale order size based on signal strength |
| ⏳ **Latency Simulation** | Introduce delays and model stale quotes |
| 🎯 **Stop-Loss Logic** | Automatically exit when loss thresholds are hit |
| 🤖 **Reinforcement Learning** | Train agent to quote optimally via trial and error |



## 🔧 Technology Stack

- **Python 3.8+**
- `numpy`, `pandas` for data simulation and tracking
- `matplotlib`, `plotly` or `seaborn` for visualization
- Optional: `scikit-learn`, `gym`, `statsmodels` for modeling/ML



## 🗂️ Project Structure (Planned)

```
market_making_simulator/
│
├── market_simulator.py          # Price generator (random walk or real data)
├── alpha_signal.py              # Alpha signal generation
├── quote_engine.py              # Bid/ask logic
├── execution_simulator.py       # Order matching & fill logic
├── risk_manager.py              # Inventory, cash, PnL
├── analyzer.py                  # Metric calculation & plots
├── config.py                    # Parameters & constants
├── main.py                      # Main simulation loop
└── README.md                    # Project documentation (this file)
```
