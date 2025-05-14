import os
import stripe
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv

load_dotenv()

billing_bp = Blueprint("billing", __name__)
print("📦 billing_bp loaded ✅")

# Set your Stripe secret key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Dummy: simulate who paid (in-memory store for now)
premium_users = set()


@billing_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    current_user = request.args.get("user", "guest")  # just use this line, no get_jwt_identity

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'AI Chatbot Premium Access',
                        },
                        'unit_amount': 500,
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
def check_premium():
    user = request.args.get("user", "guest")  # fallback
    return jsonify({"premium": user in premium_users})

@billing_bp.route("/test-payment", methods=["GET"])
def test_payment():
    return "Stripe route works!"
