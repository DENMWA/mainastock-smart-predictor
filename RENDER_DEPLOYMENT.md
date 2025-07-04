# Render Deployment Instructions for MainaStock Smart

## ✅ Prerequisites:
- GitHub repository containing:
  - app.py (your Streamlit app script)
  - requirements.txt
  - README.md (optional)
  - .gitignore (optional)

## ✅ Deployment Steps:
1. Log into your Render account: https://render.com/
2. Click **'New +' → 'Web Service'**.
3. Connect your GitHub repository.
4. In the **Environment** section, select **Python 3.x**.
5. Set the **Build Command** to:
```
pip install -r requirements.txt
```
6. Set the **Start Command** to:
```
streamlit run app.py --server.port $PORT --server.enableCORS false
```
7. Select a Free or Paid Render Plan as per your preference.
8. Click **'Create Web Service'** and wait for deployment.

## ✅ Notes:
- Your app will be publicly accessible at the provided Render URL.
- Ensure the main script is named **app.py** (or update the start command accordingly).
