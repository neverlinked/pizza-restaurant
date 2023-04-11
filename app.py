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

@app.route('/send_order', methods=['POST'])
def send_order():
    table_number = request.form.get('table_number')
    item1 = request.form.get('item1')
    item2 = request.form.get('item2')
    item3 = request.form.get('item3')
    item4 = request.form.get('item4')
    item5 = request.form.get('item5')
    item6 = request.form.get('item6')

    order = {
        'table_number': table_number,
        'items': {
            'item1': int(item1) if item1 else 0,
            'item2': int(item2) if item2 else 0,
            'item3': int(item3) if item3 else 0,
            'item4': int(item4) if item4 else 0,
            'item5': int(item5) if item5 else 0,
            'item6': int(item6) if item6 else 0,
        },
        'status': 'In Preparation'
    }

    orders.append(order)
    return redirect(url_for('kitchen'))

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
    app.run(debug=True, port=5001)
