from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Simulasi database sederhana
invoices = []

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    data['items'] = [
        {'no': 1, 'nama': data['item1'], 'jumlah': data['jumlah1'], 'harga': data['harga1'], 'diskon': data['diskon1']},
        {'no': 2, 'nama': data['item2'], 'jumlah': data['jumlah2'], 'harga': data['harga2'], 'diskon': data['diskon2']}
    ]
    invoices.append(data)
    return render_template('invoice.html', data=data, now=datetime.now())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
