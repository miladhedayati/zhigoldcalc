from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_gold_price_per_gram():
    # اینجا API واقعی قیمت طلا
    try:
        response = requests.get("https://api.tgju.org/v1/market/price/gold_geram18")
        data = response.json()
        return float(data['result']['gold_geram18']['p'])  # قیمت به تومان
    except:
        return None

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    weight = float(data.get('weight', 0))
    commission_percent = float(data.get('commission_percent', 0))

    price_per_gram = get_gold_price_per_gram()
    if not price_per_gram:
        return jsonify({'error': 'خطا در دریافت قیمت طلا'}), 500

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
