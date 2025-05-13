from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

@app.route('/')
def home():
    return "Chatbot backend is running!"

# Import blueprints AFTER app is defined
from app.auth import auth_bp
print("📦 auth_bp loaded")

app.register_blueprint(auth_bp)
print("✅ auth_bp registered")

# You can add other blueprints here if needed
