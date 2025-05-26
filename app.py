
from flask import Flask, render_template, request, redirect, send_file
from datetime import datetime
import io

app = Flask(__name__)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    product = request.form["product"]
    price = request.form["price"]
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return f"Invoice untuk {name}, produk: {product}, harga: {price}, tanggal: {now}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
