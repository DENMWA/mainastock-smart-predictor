import yfinance as yf
import numpy as np
import pandas as pd
import requests
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st

st.title("MainaStock Smart - Stock Prediction & Investment System")

# Function to fetch live AUD to USD exchange rate
def fetch_live_exchange_rate():
    try:
        response = requests.get("https://api.exchangerate.host/latest?base=AUD&symbols=USD")
        data = response.json()
        rate = data['rates']['USD']
        st.success(f"Live AUD to USD exchange rate fetched: {rate}")
        return rate
    except Exception as e:
        st.error("Failed to fetch live exchange rate. Please enter manually.")
        return None

# Step 1: Input Parameters
aud_capital = st.number_input("Enter your total capital in AUD:", min_value=0.0, value=500.0, step=100.0)
use_live_rate = st.radio("Fetch live AUD to USD exchange rate?", ('Yes', 'No'))

if use_live_rate == 'Yes':
    aud_to_usd = fetch_live_exchange_rate()
else:
    aud_to_usd = st.number_input("Enter the AUD to USD exchange rate:", min_value=0.0, value=0.65, step=0.01)

if aud_to_usd:
    usd_capital = aud_capital * aud_to_usd

    # Log currency conversion
    log_entry = {
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'AUD_Capital': aud_capital,
        'Exchange_Rate': aud_to_usd,
        'USD_Capital': usd_capital
    }
    log_file = 'currency_log.csv'
    with open(log_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=log_entry.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(log_entry)

    # Step 2: Define Your Stocks and ETFs
    assets = {
        'SPY': 'S&P 500 ETF',
        'QQQ': 'Nasdaq-100 ETF',
        'VTI': 'Total US Market ETF',
        'VIG': 'Dividend Growth ETF',
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corp.',
        'NVDA': 'Nvidia Corp.',
        'TSLA': 'Tesla Inc.',
        'AMZN': 'Amazon.com Inc.',
        'META': 'Meta Platforms Inc.'
    }

    # Step 3: Fetch Historical Data
    stock_data = {}
    for ticker in assets:
        stock_data[ticker] = yf.Ticker(ticker).history(period="5y")

    # Step 4: Define Predictive Layers
    def fourier_score(prices):
        fft_vals = np.fft.fft(prices.dropna())
        dominant_freq = np.abs(fft_vals[1:5]).sum()
        return dominant_freq

    def momentum(prices, window=5):
        returns = np.log(prices / prices.shift(1))
        momentum_val = returns.rolling(window).mean().iloc[-1]
        return momentum_val

    def sharpe_ratio(returns):
        mean_return = returns.mean()
        volatility = returns.std()
        return mean_return / volatility if volatility != 0 else 0

    # Step 5: Compute MainaStock Smart Scores
    scores = {}
    for ticker, df in stock_data.items():
        close_prices = df['Close']
        returns = np.log(close_prices / close_prices.shift(1)).dropna()

        lambda1, lambda6 = 1.0, 2.0
        fourier = fourier_score(close_prices)
        mom = momentum(close_prices)
        sharpe = sharpe_ratio(returns)

        xi_score = (lambda1 * fourier + lambda6 * mom) * np.exp(0.1 * sharpe)
        scores[ticker] = xi_score

    # Step 6: Rank Assets and Allocate Capital
    ranked_assets = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    total_score = sum(score for _, score in ranked_assets)

    allocations = [(ticker, score / total_score) for ticker, score in ranked_assets]
    investments = [(ticker, allocation * usd_capital) for ticker, allocation in allocations]

    # Step 7: Output Results
    st.subheader("Investment Plan (USD)")
    st.write(pd.DataFrame(investments, columns=['Ticker', 'Investment (USD)']))

    st.subheader("Investment Plan (AUD Equivalent)")
    st.write(pd.DataFrame(
        [(ticker, amount / aud_to_usd) for ticker, amount in investments],
        columns=['Ticker', 'Investment (AUD)']
    ))

    st.subheader("Ranked Assets")
    st.write(pd.DataFrame(ranked_assets, columns=['Ticker', 'Score']))

    # Step 8: Visualize Top Stocks' Performance
    st.subheader("Top 3 Ranked Stocks - Historical Closing Prices & Cumulative Returns")
    top_assets = [ticker for ticker, _ in ranked_assets[:3]]
    plt.figure(figsize=(12, 8))
    for ticker in top_assets:
        prices = stock_data[ticker]['Close']
        returns = prices.pct_change().fillna(0).cumsum() * 100
        plt.plot(stock_data[ticker].index, prices, label=f"{ticker} ({assets[ticker]}) - Price")
        plt.plot(stock_data[ticker].index, returns, linestyle='--', label=f"{ticker} ({assets[ticker]}) - Cumulative Return (%)")
    plt.title("Top 3 Ranked Stocks - Historical Closing Prices & Cumulative Returns")
    plt.xlabel("Date")
    plt.ylabel("Price (USD) & Return (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
