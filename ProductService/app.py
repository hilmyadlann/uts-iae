from flask import Flask, jsonify

app = Flask(__name__)

# Data produk contoh
products = {
    10: {"id": 10, "name": "Laptop", "price": 7000000},
    20: {"id": 20, "name": "Printer", "price": 1500000},
    30: {"id": 30, "name": "Smartphone", "price": 5000000},
    40: {"id": 40, "name": "Headphones", "price": 800000}
}

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(port=5001)
