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

live_rate = fetch_live_exchange_rate()

with st.form("capital_exchange_form"):
    aud_capital = st.number_input("Enter your total capital in AUD:", min_value=0.0, value=500.0, step=100.0)
    override_rate = st.checkbox("Override exchange rate manually?")
    if override_rate:
        manual_rate = st.number_input("Enter your custom AUD to USD exchange rate:", min_value=0.0, value=live_rate, step=0.01)
        aud_to_usd = manual_rate
    else:
        aud_to_usd = live_rate
    submitted = st.form_submit_button("Confirm Inputs & Start Analysis")

if submitted and aud_to_usd:
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

    # (Rest of app continues...)
