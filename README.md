# MainaStock Smart 📈

An intelligent, customizable stock prediction and investment system built with Streamlit.

---

## 🚀 Features
- Auto-ranks US stocks & ETFs based on:
  - Fourier-transformed cycles
  - Momentum
  - Sharpe Ratio
- Predicts potential high-performing assets.
- Investment allocation suggestions (USD & AUD).
- Live AUD/USD exchange rate fetching.
- Interactive, hoverable charts (Plotly).
- Weekly top stock picks + investment strategy advisor.
- Ready for SMS alerts & automation (Twilio-ready).

---

## 📋 Requirements
Dependencies are listed in `requirements.txt`.  
Install via:
```bash
pip install -r requirements.txt
```

---

## ✅ Running the App Locally
```bash
streamlit run app.py
```

---

## 🏗️ Deploying on Render
**Start Command (Render Settings):**
```bash
streamlit run app.py --server.port $PORT --server.enableCORS false
```

---

## 📡 Optional (SMS Alerts)
Supports Twilio for SMS alerts (manual integration required).  
Simply add your Twilio credentials to the app when ready.

---

## 📄 License
MIT License (Customize as needed)

---
