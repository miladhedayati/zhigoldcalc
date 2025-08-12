
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

FIXED_WEIGHT = 3.5  # گرم
FIXED_COMMISSION = 7  # درصد اجرت ساخت
FALLBACK_PRICE_PER_GRAM = 7_500_000  # قیمت fallback به تومان

def get_gold_price():
    try:
        url = "https://eghtesadonline.com/fa/tags/1908"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # این قسمت باید دقیق‌تر روی سایتت چک بشه که قیمت کجا هست
        # فرض می‌گیریم قیمت تو یک تگ span با کلاس خاص هست
        price_span = soup.find('span', class_='value')  # مثال
        if price_span:
            price_text = price_span.text.strip()
            # فرض می‌گیریم قیمت به شکل "7,600,000" هست
            price_number = int(price_text.replace(',', '').replace('٬', ''))
            return price_number
        else:
            return FALLBACK_PRICE_PER_GRAM
    except Exception as e:
        print("Error fetching price:", e)
        return FALLBACK_PRICE_PER_GRAM

@app.route('/calculate-fixed', methods=['GET'])
def calculate_fixed():
    price_per_gram = get_gold_price()
    base_price = FIXED_WEIGHT * price_per_gram
    commission_price = (FIXED_COMMISSION / 100) * base_price
    total_price = base_price + commission_price

    return jsonify({
        'weight': FIXED_WEIGHT,
        'price_per_gram': int(price_per_gram),
        'commission_percent': FIXED_COMMISSION,
        'total_price': int(total_price)
    })

@app.route('/')
def index():
    return "Gold Price Calculator is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
