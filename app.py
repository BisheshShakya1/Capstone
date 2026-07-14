from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import account
import CRUD
import alg

app = Flask(__name__)

# 1. Enable CORS (Crucial for local API development)
# This allows your frontend (e.g., localhost:3000) to talk to your backend (localhost:5000)
CORS(app) 

# --- Routes calling account.py ---
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    result = account.create_account(email, password)
    return jsonify(result), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    result = account.verify_login(email, password)
    # Added .get() and parentheses to prevent crashes if 'success' key is missing
    return jsonify(result), (200 if result.get('success') else 401)

# --- Routes calling CRUD.py ---
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = CRUD.create_record(data)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = CRUD.read_record(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# --- Routes calling alg.py ---
@app.route('/process', methods=['POST'])
def process_data():
    data = request.get_json()
    processed_result = alg.run_algorithm(data)
    return jsonify({"result": processed_result}), 200

if __name__ == '__main__':
    # 2. Create a public tunnel to your local Flask server (port 5000)
    public_url = ngrok.connect(5000)
    print(f"✅ Your local API is now publicly accessible at: {public_url}")
    print("⚠️  Note: Your API is only online while this script is running!")
    
    # 3. Run the Flask app locally
    app.run(debug=True, port=5000)
