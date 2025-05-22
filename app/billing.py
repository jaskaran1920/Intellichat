import os
import stripe
from flask import Blueprint, request, jsonify, redirect
from dotenv import load_dotenv

load_dotenv()

billing_bp = Blueprint("billing", __name__)
print("📦 billing_bp loaded ✅")

# Set your Stripe secret key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# In-memory store to simulate premium users
premium_users = set()


@billing_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    current_user = request.args.get("user", "guest")  # hardcoded for now

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
            # ✅ Redirect to backend first, then redirect to Angular
            success_url='http://127.0.0.1:5000/payment-success?user=' + current_user,
            cancel_url='http://127.0.0.1:4200/chat?premium=cancel',
        )

        return jsonify({"checkout_url": checkout_session.url})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@billing_bp.route("/payment-success")
def payment_success():
    user = request.args.get("user", "guest")
    if user:
        premium_users.add(user)
        print(f"✅ {user} added to premium_users:", premium_users)
        # ✅ Redirect back to Angular with success flag
        return redirect(f"http://localhost:4200/chat?premium=success&user={user}")
    return "❌ Missing user"


@billing_bp.route("/premium-status", methods=["GET"])
def check_premium():
    user = request.args.get("user", "guest")
    return jsonify({"premium": user in premium_users})


@billing_bp.route("/test-payment", methods=["GET"])
def test_payment():
    return "Stripe route works!"
