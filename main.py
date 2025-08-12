from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    weight = float(data.get('weight', 0))
    price_per_gram = float(data.get('price_per_gram', 0))
    total_price = weight * price_per_gram
    return jsonify({'total_price': total_price})

@app.route('/')
def index():
    return "Gold Price Calculator is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
