from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.rag_pipeline import load_and_index_documents, ask_question

chat_bp = Blueprint('chat', __name__)

vectorstore = load_and_index_documents("data_docs/sample.pdf")

@chat_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    try:
        current_user = get_jwt_identity()
        print(f"User: {current_user}")

        data = request.get_json()
        question = data.get("question", "")
        
        if not question:
            return jsonify({"error": "No question provided"}), 400

        answer = ask_question(vectorstore, question)
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

