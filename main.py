
from flask import Flask, jsonify
import requests

app = Flask(__name__)

FIXED_WEIGHT = 3.5  # وزن مدل به گرم
FIXED_COMMISSION = 7  # درصد اجرت ساخت
FALLBACK_PRICE_PER_GRAM = 7500000  # قیمت ثابت اگر API کار نکرد

def get_gold_price():
    try:
        res = requests.get("https://api.navasan.tech/v1/gold/price")
        data = res.json()
        price_per_gram = float(data['data']['price'])
        return price_per_gram
    except:
        return FALLBACK_PRICE_PER_GRAM

@app.route('/calculate-fixed', methods=['GET'])
def calculate_fixed():
    price_per_gram = get_gold_price()
    base_price = FIXED_WEIGHT * price_per_gram
    commission_price = (FIXED_COMMISSION / 100) * base_price
    total_price = base_price + commission_price

    return jsonify({
        'weight': FIXED_WEIGHT,
        'price_per_gram': price_per_gram,
        'commission_percent': FIXED_COMMISSION,
        'total_price': total_price
    })

@app.route('/')
def index():
    return "Gold Price Calculator is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
