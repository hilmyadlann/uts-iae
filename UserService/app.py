from flask import Flask, jsonify

app = Flask(__name__)

users = {
    1: {"id": 1, "name": "Adit", "email": "adit@mail.com"},
    2: {"id": 2, "name": "Aldo", "email": "aldo@mail.com"},
    3: {"id": 3, "name": "Hilmy", "email": "hilmy@mail.com"},
    4: {"id": 4, "name": "Pricilia", "email": "pricilia@mail.com"},
}
@app.route('/')
def home():
    return "Welcome to User Service!"

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(users.get(user_id, {"error": "User not found"}))

if __name__ == '__main__':
    app.run(port=5000)
