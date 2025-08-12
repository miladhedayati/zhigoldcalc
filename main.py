
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_gold_price():
    # اینجا باید API واقعی قیمت طلا رو قرار بدی
    # فعلاً تستی: هر گرم طلا = 1,200,000 تومان
    return 1200000

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    weight = float(data.get('weight', 0))  # وزن طلا
    commission_percent = float(data.get('commission_percent', 0))  # درصد اجرت

    price_per_gram = get_gold_price()

    base_price = weight * price_per_gram
    total_price = base_price + (commission_percent / 100) * base_price

    return jsonify({
        'weight': weight,
        'commission_percent': commission_percent,
        'price_per_gram': price_per_gram,
        'total_price': total_price
    })

@app.route('/')
def index():
    return "Gold Price Calculator is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
