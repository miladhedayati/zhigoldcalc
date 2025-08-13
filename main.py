import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# کلید رو از Environment Variable می‌گیریم
BRSAPI_KEY = os.getenv("BRSAPI_KEY")
BASE_URL = "https://brsapi.ir/api/v1"

def get_live_gold_price():
    """
    گرفتن قیمت لحظه‌ای طلا از BrsApi
    """
    if not BRSAPI_KEY:
        return {"error": "API key not set in environment variables."}

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Authorization": f"Bearer {BRSAPI_KEY}"
        }
        # مسیر دقیق باید با مستندات BrsApi هماهنگ بشه
        url = f"{BASE_URL}/gold"
        r = requests.get(url, headers=headers, timeout=8)
        r.raise_for_status()
        data = r.json()
        return data
    except Exception as e:
        return {"error": str(e)}

@app.route("/gold")
def gold_price():
    return jsonify(get_live_gold_price())

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
