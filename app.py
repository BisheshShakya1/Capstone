from flask import Flask, request, jsonify, session
from flask_cors import CORS
from pyngrok import ngrok
import account
import CRUD
import alg

app = Flask(__name__)
app.secret_key = "your_secret_key_here" # Required if using sessions
CORS(app)

# Helper function to get the current user's role (Adjust this to match your auth system!)
def get_current_user_role():
    # Example 1: If you store it in the Flask session after login
    # return session.get('account_type', 'user') 
    
    # Example 2: If the frontend sends it in the JSON payload (Less secure, but common for simple apps)
    data = request.get_json() or {}
    return data.get('account_type', 'user')


@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    account_type = get_current_user_role() # Get the role
    
    # Pass the account_type to the CRUD function
    result = CRUD.create_plant(data, account_type)
    
    if "error" in result:
        return jsonify(result), 403 # 403 Forbidden
    return jsonify(result), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    account_type = get_current_user_role()
    
    result = CRUD.update_plant(item_id, data, account_type)
    
    if "error" in result:
        return jsonify(result), 403
    return jsonify(result), 200


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    account_type = get_current_user_role()
    
    result = CRUD.delete_plant(item_id, account_type)
    
    if "error" in result:
        return jsonify(result), 403
    return jsonify(result), 200


# Read operations remain unchanged (no account_type needed)
@app.route('/items', methods=['GET'])
def get_all_items():
    items = CRUD.get_all_plants()
    return jsonify({"plants": items}), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = CRUD.get_plant_by_id(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    public_url = ngrok.connect(5000)
    print(f"✅ API is live at: {public_url}")
    app.run(debug=True, port=5000)
