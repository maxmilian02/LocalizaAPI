from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    categories = list(data[next(iter(data))].keys())

    return render_template('index.html', categories=categories)

@app.route('/data')
def get_data():
    category = request.args.get('category', 'GRUPO B - COMPACTO COM AR')

    with open('data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    labels = []
    prices = []

    for timestamp, prices_dict in data.items():
        labels.append(timestamp)
        prices.append(float(prices_dict[category].replace(',', '.')))

    chart_data = {
        'category': category,
        'labels': labels,
        'prices': prices
    }

    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True)
