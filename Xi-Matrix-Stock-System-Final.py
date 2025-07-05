import yfinance as yf
import numpy as np
import pandas as pd
import requests
import csv
from datetime import datetime
import plotly.graph_objs as go
import streamlit as st
import os  # For environment variables

st.title("MainaStock Smart - Stock Prediction & Investment System")

st.info("Please enter your capital and exchange rate above to start analysis.")

# Load API keys securely from environment variables (for future integrations)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

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

    # (The rest of your full app remains unchanged)
