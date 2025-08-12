from flask import Flask, request, jsonify

app = Flask(__name__)

# قیمت ثابت هر گرم طلا (موقت - به تومان)
FIXED_PRICE_PER_GRAM = 1200000  

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    try:
        weight = float(data.get('weight', 0))
        commission_percent = float(data.get('commission_percent', 0))

        # محاسبه: وزن × قیمت هر گرم
        base_price = weight * FIXED_PRICE_PER_GRAM

        # محاسبه اجرت
        commission = (commission_percent / 100) * base_price

        total_price = base_price + commission

        return jsonify({
            'weight': weight,
            'price_per_gram': FIXED_PRICE_PER_GRAM,
            'commission_percent': commission_percent,
            'total_price': total_price
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def index():
    return "Gold Price Calculator is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
