from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open(r'C:\Users\abcma\OneDrive\Documentos\python\localiza\LocalizaAPI\data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    categories = list(data[next(iter(data))].keys())

    return render_template('index.html', categories=categories)

@app.route('/data')
def get_data():
    category = request.args.get('category', 'GRUPO B - COMPACTO COM AR')

    with open(r'C:\Users\abcma\OneDrive\Documentos\python\localiza\LocalizaAPI\data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    labels = []
    prices = []

    for timestamp, prices_dict in data.items():
        labels.append(timestamp)
        price = float(prices_dict[category].replace(',', '.'))
        prices.append(price)

    minPrice = min(prices)
    maxPrice = max(prices)

    chart_data = {
        'category': category,
        'labels': labels,
        'prices': prices,
        'minPrice': minPrice,  # Inclua o valor mínimo no dicionário
        'maxPrice': maxPrice   # Inclua o valor máximo no dicionário
    }

    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(host='192.168.15.91', port=5000, debug=True)
