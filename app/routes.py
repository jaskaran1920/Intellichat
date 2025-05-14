from flask import Blueprint, request, jsonify
from app.rag_pipeline import load_and_index_documents, ask_question

chat_bp = Blueprint('chat', __name__)

vectorstore = load_and_index_documents("data_docs/sample.pdf")

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        question = data.get("question", "")
        
        if not question:
            return jsonify({"error": "No question provided"}), 400

        print(f"❓ Question: {question}")
        answer = ask_question(vectorstore, question)
        print(f"✅ Answer: {answer}")
        
        return jsonify({"answer": answer})
    
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500
