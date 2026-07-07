from flask import Flask, request, jsonify
import account
import CRUD
import alg

app = Flask(__name__)

# --- Routes calling account.py ---
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Calls the function inside account.py
    result = account.create_account(email, password)
    return jsonify(result), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Calls the function inside account.py
    result = account.verify_login(email, password)
    return jsonify(result), 200 if result['success'] else 401


# --- Routes calling CRUD.py ---
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    
    # Calls the function inside CRUD.py
    new_item = CRUD.create_record(data)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    # Calls the function inside CRUD.py
    item = CRUD.read_record(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404


# --- Routes calling alg.py ---
@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()
    
    # Calls the function inside alg.py
    processed_result = alg.run_algorithm(data)
    return jsonify({"result": processed_result}), 200


if __name__ == '__main__':
    app.run(debug=True)
