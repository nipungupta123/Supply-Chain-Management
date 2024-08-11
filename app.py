from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    """ Create a database connection """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='nipun123',
            database='inventory_system'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

def add_item(name, quantity, price):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO items (name, quantity, price)
        VALUES (%s, %s, %s)
    ''', (name, quantity, price))
    connection.commit()
    connection.close()

def update_item(item_id, name, quantity, price):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE items
        SET name = %s, quantity = %s, price = %s
        WHERE id = %s
    ''', (name, quantity, price, item_id))
    connection.commit()
    connection.close()

def delete_item(item_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
    connection.commit()
    connection.close()

def view_items():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    connection.close()
    return items

@app.route('/')
def index():
    items = view_items()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        add_item(name, int(quantity), float(price))
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        update_item(item_id, name, int(quantity), float(price))
        return redirect(url_for('index'))
    return render_template('update_item.html', item_id=item_id)

@app.route('/delete/<int:item_id>')
def delete(item_id):
    delete_item(item_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
