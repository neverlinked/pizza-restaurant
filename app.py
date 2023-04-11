from flask import Flask, render_template, request, redirect, url_for
from collections import deque

app = Flask(__name__)

orders = deque()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/reception')
def reception():
    return render_template('reception.html', orders=orders)

@app.route('/webpage')
def webpage():
    return render_template('websitepage.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/send_order', methods=['POST'])
def send_order():
    table_number = request.form['table_number']
    item1 = int(request.form['item1'])
    item2 = int(request.form['item2'])
    item3 = int(request.form['item3'])
    item4 = int(request.form['item4'])
    item5 = int(request.form['item5'])
    item6 = int(request.form['item6'])
    total_price = item1 * 12.99 + item2 *  14.99 + item3 * 10.99 + item4 * 1.99 + item5 *  2.99 + item6 * 2.99
    
    order = {
        'table_number': table_number,
        'items': {
            'item1': item1,
            'item2': item2,
            'item3': item3,
            'item4': item4,
            'item5': item5,
            'item6': item6
        },
        'status': 'pending',
        'total_price': total_price
    }
    
    orders.append(order)
    return redirect(url_for('main'))

@app.route('/kitchen')
def kitchen():
    return render_template('kitchen.html', orders=orders)

@app.route('/update_status', methods=['POST'])
def update_status():
    order_index = int(request.form.get('order_index'))
    status = request.form.get('status')

    if 0 <= order_index < len(orders):
        orders[order_index]['status'] = status

    if request.referrer.endswith('/reception'):
        return redirect(url_for('reception'))
    else:
        return redirect(url_for('kitchen'))



@app.route('/remove_order', methods=['POST'])
def remove_order():
    order_index = int(request.form.get('order_index'))
    if 0 <= order_index < len(orders):
        orders.remove(orders[order_index])
    return redirect(url_for('kitchen'))

@app.route('/arduino_status')
def arduino_status():
    return render_template('arduino_status.html', current_status = current_status)

current_status = ['Pizza is not ready']
@app.route('/update_arduino', methods =['POST'])
def update_arduino():
    arduino_data = request.get_json()
    pizza_ready = arduino_data['Pizza']
    
    current_status[0] = pizza_ready
    return redirect(url_for('arduino_status'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)
