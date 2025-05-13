import os
import stripe
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv

load_dotenv()

billing_bp = Blueprint("billing", __name__)

# Set your Stripe secret key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Dummy: simulate who paid (in-memory store for now)
premium_users = set()

@billing_bp.route("/create-checkout-session", methods=["POST"])
@jwt_required()
def create_checkout_session():
    current_user = get_jwt_identity()

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'AI Chatbot Premium Access',
                        },
                        'unit_amount': 500,  # $5.00
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:5000/payment-success?user=' + current_user,
            cancel_url='http://localhost:5000/payment-cancel',
        )

        return jsonify({"checkout_url": checkout_session.url})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@billing_bp.route("/payment-success")
def payment_success():
    user = request.args.get("user")
    if user:
        premium_users.add(user)
        return f"Payment successful! {user} is now a premium user. You may close this tab."
    return "Missing user"

@billing_bp.route("/premium-status", methods=["GET"])
@jwt_required()
def check_premium():
    user = get_jwt_identity()
    return jsonify({"premium": user in premium_users})
