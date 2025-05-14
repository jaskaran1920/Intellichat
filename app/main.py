from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

from app.routes import chat_bp
app.register_blueprint(chat_bp)
print("✅ chat_bp registered")

# ✅ Ensure this is BELOW app creation
from app.billing import billing_bp
app.register_blueprint(billing_bp)
print("✅ billing_bp registered")

@app.route('/')
def home():
    return "✅ Chatbot backend is running!"
