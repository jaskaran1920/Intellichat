from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

USERS = {
    "admin": "password123",
    "employee": "letmein"
}

@auth_bp.route('/login', methods=['POST'])
def login():
    print("🔥 /login route hit")
    
    print("Headers:", dict(request.headers))
    print("Raw body:", request.data)
    print("JSON:", request.get_json())

    try:
        data = request.get_json()
        print("🧾 Received data:", data)

        username = data.get("username")
        password = data.get("password")
        print("🔑 username:", username, "| password:", password)

        if username and password:
           return jsonify({'message': 'Login successful'})

        if not username or not password:
            print("❌ Missing credentials")
            return jsonify({"error": "Missing credentials"}), 400

        if USERS.get(username) != password:
            print("❌ Invalid credentials")
            return jsonify({"error": "Invalid username or password"}), 401

        token = create_access_token(identity=username)
        print("✅ Token generated:", token)
        return jsonify(access_token=token)

    except Exception as e:
        print("💥 Exception occurred:", e)
        return jsonify({"error": "Server error"}), 500
