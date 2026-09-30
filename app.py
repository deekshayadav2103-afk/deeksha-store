from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3, os

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE, 'templates'))
app.secret_key = 'deeksha_store_2026'
DB = os.path.join(BASE, 'shop.db')

def get_db():
    conn = sqlite3.connect(DB)
    return conn

# DB + More Products for Deeksha
conn = get_db()
conn.execute('''CREATE TABLE IF NOT EXISTS products
(id INTEGER PRIMARY KEY, name TEXT, price INTEGER, image TEXT, desc TEXT)''')
conn.execute("DELETE FROM products")
products = [
(1, "Bluetooth Headphone", 1499, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500", "Noise Cancellation, 40Hr Battery, for Deeksha"),
(2, "Smart Watch", 2499, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500", "Heart Rate, SpO2, Calls"),
(3, "Nike Shoes", 2999, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500", "Running Shoes, Comfortable"),
(4, "Mac Lipstick - Ruby Woo", 899, "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=500", "Favorite shade for Deeksha ❤️"),
(5, "Zara Dress - Red", 1999, "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500", "Party Wear Dress"),
(6, "iPhone 15", 70999, "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500", "128GB, Pink")
]
for p in products:
    conn.execute("INSERT INTO products VALUES (?,?,?,?,?)", p)
conn.commit()
conn.close()

@app.route('/')
def home():
    q = request.args.get('q','')
    conn = get_db()
    if q:
        prods = conn.execute("SELECT * FROM products WHERE name LIKE?", ('%'+q+'%',)).fetchall()
    else:
        prods = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    cart_count = len(session.get('cart', []))
    return render_template('index.html', products=prods, cart_count=cart_count)

@app.route('/product/<int:pid>')
def product(pid):
    conn = get_db()
    p = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    conn.close()
    return render_template('product.html', p=p, cart_count=len(session.get('cart', [])))

@app.route('/add_to_cart/<int:pid>')
def add_to_cart(pid):
    if 'cart' not in session: session['cart'] = []
    session['cart'].append(pid)
    session.modified = True
    return redirect('/cart')

@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    conn = get_db()
    items = []
    total = 0
    for pid in cart_ids:
        pr = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
        if pr:
            items.append(pr)
            total += pr[2]
    conn.close()
    return render_template('cart.html', items=items, total=total, cart_count=len(cart_ids))

@app.route('/remove/<int:pid>')
def remove(pid):
    if 'cart' in session and pid in session['cart']:
        session['cart'].remove(pid)
        session.modified = True
    return redirect('/cart')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Simple login for Deeksha
        session['user'] = request.form['username']
        return redirect('/')
    return render_template('login.html')

@app.route('/checkout')
def checkout():
    session['cart'] = []
    return "<h1 style='text-align:center; margin-top:100px; font-family:Arial'>🎉 Order Placed for Deeksha! ❤️<br><br><a href='/'>Back to Home</a></h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)