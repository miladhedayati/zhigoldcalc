import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

BRSAPI_KEY = os.getenv("BRSAPI_KEY")  # کلید رو تو Render به عنوان متغیر محیطی بذار
BASE_URL = "https://brsapi.ir/api/v1"

def get_live_gold_price():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Authorization": f"Bearer {BRSAPI_KEY}"
        }
        # این آدرس نمونه است، طبق مستندات BrsApi مسیر دقیق رو جایگزین کن
        url = f"{BASE_URL}/gold"
        r = requests.get(url, headers=headers, timeout=8)
        r.raise_for_status()
        data = r.json()
        return data  # داده خام رو برمی‌گردونیم
    except Exception as e:
        return {"error": str(e)}

@app.route("/gold")
def gold_price():
    price_data = get_live_gold_price()
    return jsonify(price_data)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
