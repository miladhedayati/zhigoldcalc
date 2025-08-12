from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_gold_price():
    url = "https://www.estjt.ir/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    price_tag = soup.find('td', string='طلا ۱۸ عیار')
    if price_tag:
        price = price_tag.find_next('td').text.strip()
        price = int(price.replace(',', '').replace(' تومان', '').replace('٬', ''))
        return price
    else:
        return 7500000  # قیمت fallback اگر نتونست قیمت رو بگیره

@app.route('/calculate/<float:weight>/<float:commission_percent>', methods=['GET'])
def calculate(weight, commission_percent):
    price_per_gram = get_gold_price()
    base_price = weight * price_per_gram
    commission_price = (commission_percent / 100) * base_price
    total_price = base_price + commission_price

    return jsonify({
        'weight': weight,
        'price_per_gram': price_per_gram,
        'commission_percent': commission_percent,
        'total_price': int(total_price)
    })

@app.route('/')
def index():
    return "Gold Price Calculator is Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
