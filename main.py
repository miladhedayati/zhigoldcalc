from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_gold_price():
    try:
        url = "https://egoldunion.ir/"  # سایت اتحادیه طلا
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # پیدا کردن قیمت طلای 18 عیار؛ این بخش ممکنه نیاز به آپدیت داشته باشه بر اساس ساختار سایت
        # نمونه: قیمت تو تگی با کلاس 'price' هست، یا id خاص
        price_tag = soup.find("td", text="طلا ۱۸ عیار")
        if price_tag:
            # قیمت در سلول کناری هست
            price_value = price_tag.find_next_sibling("td").text.strip()
            # حذف کاما و تبدیل به عدد
            price_num = float(price_value.replace(",", ""))
            return price_num

        return 1200000  # قیمت پیش فرض در صورت خطا

    except Exception as e:
        print(f"Error fetching gold price: {e}")
        return 1200000  # قیمت پیش فرض

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        weight = float(data.get('weight', 0))
        commission_percent = float(data.get('commission_percent', 0))

        price_per_gram = get_gold_price()

        base_price = weight * price_per_gram
        commission_price = (commission_percent / 100) * weight * price_per_gram

        total_price = base_price + commission_price

        return jsonify({
            'weight': weight,
            'price_per_gram': price_per_gram,
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
