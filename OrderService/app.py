from flask import Flask, jsonify, request, render_template_string
import requests
import json
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Nama file untuk menyimpan data pesanan
ORDERS_FILE = "orders.json"

# Fungsi untuk memuat data pesanan dari file JSON
def load_orders():
    try:
        with open(ORDERS_FILE, 'r') as f:
            data = f.read()
            if not data.strip():
                return []  # Jika file kosong, kembalikan list kosong
            return json.loads(data)  # Jika ada data, proses dan kembalikan sebagai list
    except FileNotFoundError:
        return []  # Jika file tidak ditemukan, kembalikan list kosong
    except json.JSONDecodeError:
        return []  # Jika format JSON rusak, kembalikan list kosong

# Fungsi untuk menyimpan data pesanan ke file JSON
def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=4)

# Memuat data pesanan saat aplikasi dimulai
orders = load_orders()

# Konfigurasi Swagger UI
SWAGGER_URL = '/docs'  # URL untuk mengakses Swagger UI
API_URL = '/openapi.json'  # URL untuk mendapatkan file OpenAPI JSON

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Order Service"
    }
)

# Menambahkan blueprint Swagger UI ke aplikasi Flask
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Halaman utama dengan menu
@app.route('/')
def home():
    return render_template_string("""
        <h1>Order Service</h1>
        <p>Menu:</p>
        <ul>
            <li><a href="/view_all_orders">Lihat Semua Pesanan</a></li>
            <li><a href="/add_order_form">Tambah Pesanan</a></li>
            <li><a href="/docs">Swagger UI</a></li>
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
                    <strong>Jumlah:</strong> {{ order['quantity'] }} <br>
                    <strong>Total Harga:</strong> Rp {{ order['total_price'] }} <br>
                    <strong>Status:</strong> {{ order['status'] }} <br>
                    <strong>Suspicious:</strong> {{ order['suspicious'] }} <br>
                    <strong>Refund Status:</strong> {{ order['refund_status'] }} <br><br>
                </li>
            {% else %}
                <p>No orders found.</p>
            {% endfor %}
        </ul>
        <a href="/">Kembali ke Menu</a>
    """, orders=orders)

# Route untuk form menambah pesanan
@app.route('/add_order_form')
def add_order_form():
    return render_template_string("""
        <h1>Tambah Pesanan Baru</h1>
        <form action="/orders" method="POST">  
            <label for="user_id">ID Pengguna:</label><br>
            <input type="number" id="user_id" name="user_id"><br><br>
            <label for="product_id">ID Produk:</label><br>
            <input type="number" id="product_id" name="product_id"><br><br>
            <label for="quantity">Jumlah Produk:</label><br>
            <input type="number" id="quantity" name="quantity"><br><br>
            <input type="submit" value="Tambah Pesanan">
        </form>
        <a href="/">Kembali ke Menu</a>
    """)

# Menambah pesanan (Mendukung baik form-data atau JSON)
@app.route('/orders', methods=['POST'])
def add_order():
    try:
        # Cek format data yang dikirim
        if request.is_json:  # Jika data dikirim dalam format JSON
            data = request.get_json()
        else:  # Jika data dikirim dalam format form-data
            data = request.form

        # Ambil data dari request
        user_id = int(data.get('user_id'))
        product_id = int(data.get('product_id'))
        quantity = int(data.get('quantity'))

        # Periksa apakah data yang diperlukan ada
        if not user_id or not product_id or not quantity:
            return jsonify({"error": "Missing required fields"}), 400

        # Mengambil data user dari UserService
        user_resp = requests.get(f"http://localhost:5000/users/{user_id}")
        if user_resp.status_code != 200:
            return jsonify({"error": "User not found"}), 404

        # Mengambil data produk dari ProductService
        product_resp = requests.get(f"http://localhost:5001/products/{product_id}")
        if product_resp.status_code != 200:
            return jsonify({"error": "Product not found"}), 404

        # Menghitung total harga
        product_price = product_resp.json().get("price")
        total_price = product_price * quantity

        # Menandai apakah pesanan mencurigakan (quantity > 10)
        suspicious = True if quantity > 10 else False
        
        # Jika pesanan mencurigakan, ubah status menjadi "Failed" dan refund "Refund"
        status = "Failed" if suspicious else "Success"
        refund_status = "Refund" if suspicious else "No Refund"

        # Buat data pesanan
        order = {
            "order_id": len(orders) + 1,
            "user": user_resp.json(),
            "product": product_resp.json(),
            "product_price": product_price,
            "quantity": quantity,
            "total_price": total_price,
            "status": status,
            "suspicious": suspicious,
            "refund_status": refund_status
        }

        orders.append(order)  # Simpan pesanan
        save_orders(orders)  # Simpan data pesanan ke file JSON
        return jsonify(order), 201

    except Exception as e:
        print(f"Error occurred: {e}")  # Menambahkan log untuk menangkap error
        return jsonify({"error": "Internal Server Error"}), 500


# Endpoint untuk OpenAPI JSON
@app.route('/openapi.json')
def openapi_json():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Order Service API",
            "version": "1.0.0",
            "description": "API untuk mengelola pesanan"
        },
        "paths": {
            "/orders": {
                "post": {
                    "summary": "Menambah pesanan",
                    "operationId": "addOrder",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "user_id": {"type": "integer"},
                                        "product_id": {"type": "integer"},
                                        "quantity": {"type": "integer"}
                                    },
                                    "required": ["user_id", "product_id", "quantity"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Pesanan berhasil ditambahkan",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Order"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Order": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "integer"},
                        "user": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                                "email": {"type": "string"}
                            }
                        },
                        "product": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "name": {"type": "string"},
                                "price": {"type": "integer"}
                            }
                        },
                        "quantity": {"type": "integer"},
                        "total_price": {"type": "integer"},
                        "status": {"type": "string"},
                        "suspicious": {"type": "boolean"},
                        "refund_status": {"type": "string"}
                    }
                }
            }
        }
    })


if __name__ == '__main__':
    app.run(port=5002)
