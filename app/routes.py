from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

# --------------------- Setup ---------------------
chat_bp = Blueprint('chat', __name__)
vectorstore = None  # ✅ Global vectorstore

UPLOAD_FOLDER = "data_docs"
ALLOWED_EXTENSIONS = {"csv"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --------------------- Chat Route ---------------------
@chat_bp.route('/chat', methods=['POST'])
def chat():
    global vectorstore  # Access global

    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        if vectorstore is None:
            return jsonify({"error": "No data loaded. Please upload a CSV first."}), 400

        print(f"❓ Question: {question}")
        from app.rag_pipeline import ask_question
        answer = ask_question(vectorstore, question)
        print(f"✅ Answer: {answer}")

        return jsonify({"answer": answer})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

# --------------------- Upload CSV Route ---------------------
@chat_bp.route('/upload-csv', methods=['POST'])
def upload_csv():
    global vectorstore  # Modify global

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        print("📁 Saving uploaded CSV to:", filepath)
        file.save(filepath)

        print("📦 Creating vectorstore from CSV...")
        from app.rag_pipeline import load_and_index_csv
        vectorstore = load_and_index_csv(filepath)

        print("✅ Vectorstore loaded:", vectorstore)

        return jsonify({'message': 'CSV uploaded and indexed successfully'})

    return jsonify({'error': 'Invalid file type'}), 400
