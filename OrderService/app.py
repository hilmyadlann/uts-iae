from flask import Flask, jsonify, request, render_template_string
import requests
import json

app = Flask(__name__)

# Nama file untuk menyimpan data pesanan
ORDERS_FILE = "orders.json"

# Fungsi untuk memuat data pesanan dari file JSON
def load_orders():
    try:
        with open(ORDERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Jika file tidak ditemukan, kembalikan list kosong

# Fungsi untuk menyimpan data pesanan ke file JSON
def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=4)

# Memuat data pesanan saat aplikasi dimulai
orders = load_orders()

# Halaman utama dengan menu
@app.route('/')
def home():
    return render_template_string("""
        <h1>Order Service</h1>
        <p>Menu:</p>
        <ul>
            <li><a href="/view_all_orders">Lihat Semua Pesanan</a></li>
            <li><a href="/add_order_form">Tambah Pesanan</a></li>
        </ul>
    """)

# Route untuk melihat semua pesanan
@app.route('/view_all_orders')
def view_all_orders():
    return render_template_string("""
        <h1>Semua Pesanan</h1>
        <ul>
            {% for order in orders %}
                <li>
                    <strong>ID Pesanan:</strong> {{ order['order_id'] }} <br>
                    <strong>User:</strong> {{ order['user']['name'] }} <br>
                    <strong>Produk:</strong> {{ order['product']['name'] }} <br>
                    <strong>Harga Produk:</strong> Rp {{ order['product_price'] }} <br>
                    <strong>Status:</strong> {{ order['status'] }} <br><br>
                </li>
            {% else %}
                <p>No orders found.</p>
            {% endfor %}
        </ul>
        <a href="/">Kembali ke Menu</a>
    """, orders=orders)

# Route untuk menambah pesanan
@app.route('/add_order_form')
def add_order_form():
    return render_template_string("""
        <h1>Tambah Pesanan Baru</h1>
        <form action="/add_order" method="POST">
            <label for="user_id">ID Pengguna:</label><br>
            <input type="number" id="user_id" name="user_id"><br><br>
            <label for="product_id">ID Produk:</label><br>
            <input type="number" id="product_id" name="product_id"><br><br>
            <input type="submit" value="Tambah Pesanan">
        </form>
        <a href="/">Kembali ke Menu</a>
    """)

# Menambah pesanan
@app.route('/add_order', methods=['POST'])
def add_order():
    # Ambil data dari request
    data = request.form
    user_id = int(data.get('user_id'))
    product_id = int(data.get('product_id'))

    # Mengambil data user dari UserService
    user_resp = requests.get(f"http://localhost:5000/users/{user_id}")
    if user_resp.status_code != 200:
        return jsonify({"error": "User not found"}), 404

    # Mengambil data produk dari ProductService
    product_resp = requests.get(f"http://localhost:5001/products/{product_id}")
    if product_resp.status_code != 200:
        return jsonify({"error": "Product not found"}), 404

    # Buat data pesanan
    order = {
        "order_id": len(orders) + 1,
        "user": user_resp.json(),
        "product": product_resp.json(),
        "product_price": product_resp.json().get("price"),  # Menambahkan harga produk
        "status": "success"
    }

    orders.append(order)  # Simpan pesanan
    save_orders(orders)  # Simpan data pesanan ke file JSON
    return jsonify(order), 201

if __name__ == '__main__':
    app.run(port=5002)
