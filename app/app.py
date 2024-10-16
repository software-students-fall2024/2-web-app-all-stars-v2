from flask import Flask, render_template, request, redirect, url_for, jsonify
from bson.objectid import ObjectId
from bson.decimal128 import Decimal128
from connection import *
from store_data import get_store_data
from get_transactions import get_transactions
from add_transaction import add_transaction
from get_transaction_to_edit import get_transaction_to_edit
from edit_transaction import edit_transaction
from delete_transaction import delete_transaction
from get_transaction import get_transaction
import json

# Home Screen (Select location) 
# Store information Screen
# List of Transaction Screen (For selected location)    -read.html
# Add Transaction Screen (CREATE transaction)   -create.html
# Edit Transaction Screen (UPDATE transaction)  -edit.html
# Delete Transaction Screen (DELETE transaction)  - delete.html

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location/<store_location>')

def location(store_location):

    store_data = get_store_data(store_location)
    store_data['total_revenue'] = "{:,.2f}".format(store_data['total_revenue'])
    
    return render_template('location.html',store_location=store_location, **store_data)

@app.route('/transactions/<store_location>')
def transactions(store_location):
    transaction_data =  get_transactions(store_location)
    return render_template('read.html', store_location=store_location, transaction_data=transaction_data['transactions'])

@app.route('/add_transaction_page/<store_location>')
def add_transaction_page(store_location):
    return render_template('create.html', store_location=store_location)

@app.route('/submit/<store_location>', methods=['POST'])
def submit_form(store_location):
    form_data = {
        'item_name': request.form.get('item_name'),
        'quantity': int(request.form.get('quantity')),
        'price': float(Decimal128(request.form.get('price')).to_decimal()),
        'store_location': store_location,
        'gender': request.form.get('gender'),
        'age': int(request.form.get('age')),
        'email': request.form.get('email'),
        'coupon_used': request.form.get('coupon_used'),
        'purchase_method': request.form.get('purchase_method')
    }
    add_transaction(**form_data)
    transaction = get_transaction(form_data['email'])
    transaction['_id'] = str(transaction['_id'])
    transaction = dict(transaction)
    return render_template('create.html', store_location=store_location, added_transaction=transaction)

@app.route('/edit/<store_location>')
def edit_page(store_location):
    return render_template('edit.html', store_location=store_location)

@app.route('/get_to_edit')
def get_to_edit():
    email = request.args.get('customer_email')
    print(email)
    purchase_method = request.args.get('purchase_method')
    print(purchase_method)
    if get_transaction_to_edit(email) != "Transaction not found.":
        edit_transaction(email, purchase_method)
        ## Where will this go?
    return get_transaction_to_edit(email)

@app.route('/delete')
def delete_page():
    return render_template('delete.html')

@app.route('/delete_transaction', methods=['POST'])
def delete():
    email = request.form.get('customer_email')
    if email:
        try: 
            transaction = get_transaction(email)
            transaction['_id'] = str(transaction['_id'])
            transaction = dict(transaction)
            delete_transaction(email)
            return render_template('delete.html', transaction=transaction)
        except:
            return f"No transaction found for {email}.", 404
    return "Email is required.", 400

if __name__ == '__main__':
    app.run(debug=True)