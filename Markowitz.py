import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Prompt user for file path
file_path = input("Enter the path to your CSV or Excel file containing tickers: ")

# Read only the 'Stock' column from the file (supports CSV and Excel)
if file_path.endswith('.csv'):
    tickers_df = pd.read_csv(file_path, usecols=lambda c: c == 'Stock')
elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
    tickers_df = pd.read_excel(file_path, usecols=lambda c: c == 'Stock')
else:
    raise ValueError("Unsupported file type. Please provide a .csv or .xlsx/.xls file.")

tickers = tickers_df['Stock'].dropna().astype(str).tolist()

print(f"Tickers loaded: {tickers}")

data = yf.download(tickers, period="600d")
if data is None or "Close" not in data:
    raise ValueError("Failed to download data or 'Close' prices not found.")

portfolio = data["Close"].dropna()

# Calculate daily returns
portfolio_normalised = portfolio.pct_change().dropna()

# Equal weights for any number of tickers
weights = np.array([1.0 / len(tickers)] * len(tickers))

# Portfolio statistics
mean_returns = portfolio_normalised.mean()
cov_matrix = portfolio_normalised.cov() * 252
net_return = np.sum(mean_returns * weights) * 252
std_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix.values, weights)))
SR = net_return / std_risk

# Monte Carlo simulation
np.random.seed(199)
number_simulation = 100000
weight_saved = np.zeros((number_simulation, len(tickers)))
ret_arr = np.zeros(number_simulation)
vol_arr = np.zeros(number_simulation)
sharpe_arr = np.zeros(number_simulation)

for a in range(number_simulation):
    weight = np.random.rand(len(tickers))
    weight_rebalanced = weight / np.sum(weight)
    weight_saved[a, :] = weight_rebalanced
    ret_arr[a] = np.sum(mean_returns * weight_rebalanced) * 252
    vol_arr[a] = np.sqrt(np.dot(weight_rebalanced.T, np.dot(cov_matrix.values, weight_rebalanced)))
    sharpe_arr[a] = ret_arr[a] / vol_arr[a]

# Find optimal weights
max_sharpe_idx = sharpe_arr.argmax()
optimal_weights = weight_saved[max_sharpe_idx, :]

# Output the weights of each stock in the optimal portfolio
print("Optimal Portfolio Weights (Max Sharpe Ratio):")
for ticker, weight in zip(tickers, optimal_weights):
    print(f"{ticker}: {weight:.4f}")

# Output the return, risk, and Sharpe ratio of the final portfolio
final_return = ret_arr[max_sharpe_idx]
final_risk = vol_arr[max_sharpe_idx]
final_sharpe = sharpe_arr[max_sharpe_idx]
print(f"\nFinal Portfolio Return: {final_return:.4f}")
print(f"Final Portfolio Risk (Volatility): {final_risk:.4f}")
print(f"Final Portfolio Sharpe Ratio: {final_sharpe:.4f}")

# Create DataFrame for plotting
array = np.array([ret_arr, vol_arr, sharpe_arr]).T
column_values = ["Return", "Volatility", "Sharpe Ratio"]
df = pd.DataFrame(array, columns=column_values)

# Plot
df.plot.scatter(x="Volatility", y="Return", c="Sharpe Ratio", cmap="viridis", edgecolors="k", figsize=(10, 8), grid=True)
plt.show()

# Print optimal weights and Sharpe ratio
print("Optimal weights:", dict(zip(tickers, optimal_weights)))
print("Max Sharpe Ratio:", sharpe_arr[max_sharpe_idx])







#calculate the daily returns for each ticker






