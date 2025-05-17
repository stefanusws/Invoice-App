
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pdfkit
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    invoices = db.relationship('Invoice', backref='customer', lazy=True)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form['name']
    phone = request.form['phone']
    customer = Customer(name=name, phone=phone)
    db.session.add(customer)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_invoice/<int:customer_id>', methods=['POST'])
def add_invoice(customer_id):
    description = request.form['description']
    amount = float(request.form['amount'])
    invoice = Invoice(customer_id=customer_id, description=description, amount=amount)
    db.session.add(invoice)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/invoice/<int:invoice_id>/print')
def print_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    customer = Customer.query.get(invoice.customer_id)
    rendered = render_template('invoice.html', invoice=invoice, customer=customer)
    pdf_path = f'invoice_{invoice.id}.pdf'
    pdfkit.from_string(rendered, pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
