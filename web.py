from flask import Flask, render_template_string, request
from datetime import datetime, timedelta
import joblib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24) 

lookup_table = joblib.load('product_lookup_table.joblib')

def get_remaining_days(product_name):
    return lookup_table.get(product_name, None)

def calculate_expiry_date_and_remaining_days(product_name, purchase_date_str):
    remaining_days = get_remaining_days(product_name)
    if remaining_days is None:
        return "Product not found", None

    try:
        purchase_date = datetime.strptime(purchase_date_str, '%d-%m-%Y')
    except ValueError:
        return "Invalid date format. Use DD-MM-YYYY", None

    expiry_date = purchase_date + timedelta(days=remaining_days)
    return expiry_date.strftime('%d-%m-%Y')

login_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Product Expiry Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 50%;
            margin: 100px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
        }
        .form-group input {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #007BFF;
            color: #fff;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Product Expiry Calculator</h2>
        <form method="post" action="{{ url_for('calculate') }}">
            <div class="form-group">
                <label for="product_name">Product Name:</label>
                <input type="text" id="product_name" name="product_name" required>
            </div>
            <div class="form-group">
                <label for="purchase_date">Purchase Date (DD-MM-YYYY):</label>
                <input type="text" id="purchase_date" name="purchase_date" required>
            </div>
            <button type="submit">Calculate Expiry Date</button>
        </form>
    </div>
</body>
</html>
"""

result_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Expiry Date Result</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 50%;
            margin: 100px auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Expiry Date Result</h2>
        <p>Product: {{ product_name }}</p>
        <p>Expiry Date: {{ expiry_date }}</p>
        <br>
        <a href="{{ url_for('login') }}">Back</a>
    </div>
</body>
</html>
"""

@app.route('/')
def login():
    return render_template_string(login_html)

@app.route('/calculate', methods=['POST'])
def calculate():
    product_name = request.form['product_name']
    purchase_date_str = request.form['purchase_date']
    expiry_date_str = calculate_expiry_date_and_remaining_days(product_name, purchase_date_str)
    return render_template_string(result_html, product_name=product_name, expiry_date=expiry_date_str)

if __name__ == '__main__':
    app.run(debug=True)
