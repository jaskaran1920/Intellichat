# 🧠 AI Chatbot Project - Steps 1 to 5 Explained

This document provides a full explanation of what has been done so far in your project — including what was built, why each part exists, what files were created, and how each component is connected.

---

## ✅ Step 1: Project Setup & Environment

### 🔧 What Was Done:

* Created the folder structure using VS Code and Cursor.
* Initialized a Python virtual environment: `python3 -m venv venv`
* Installed core libraries using pip:

  ```bash
  pip install flask openai langchain faiss-cpu flask-jwt-extended stripe python-dotenv
  ```
* Created `requirements.txt` to track all dependencies.

### 📁 Why:

* Flask = lightweight backend web server
* LangChain = manages RAG (retrieval augmented generation)
* FAISS = for vector storage
* JWT = for authentication
* Stripe = for future payments
* dotenv = to load secrets like API keys

---

## ✅ Step 2: Flask App Structure

### 📁 Files Created:

* `app/main.py` → initializes Flask app and JWT
* `run.py` → entry point to start the server
* `.env` → stores secrets (like API keys)

### 🔧 What It Does:

* Loads environment variables securely
* Initializes the Flask app with JWT config
* Registers blueprints for `/chat` and `/login` routes
* Serves a default health check at `/`

### 🔗 Connections:

* `run.py` → imports and runs `app.main.app`
* `main.py` → imports routes and auth blueprints

---

## ✅ Step 3: RAG Pipeline with LangChain

### 📁 File Created:

* `app/rag_pipeline.py`

### 🔧 What It Does:

* Loads a PDF from `data_docs/sample.pdf`
* Splits it into chunks
* Converts those chunks into vector embeddings using `OpenAIEmbeddings`
* Stores them in `FAISS` for fast similarity search
* Uses `ChatOpenAI` to answer based on relevant chunks

### 🔗 Connections:

* Used in `/chat` route to answer user questions
* Called once and cached as `vectorstore` on app startup

---

## ✅ Step 4: `/chat` API Route

### 📁 File Created:

* `app/routes.py`

### 🔧 What It Does:

* Defines `/chat` POST endpoint
* Accepts JSON body with a `question`
* Passes question to RAG pipeline → returns answer

### 🔗 Connections:

* `chat_bp` blueprint registered in `main.py`
* `vectorstore` loaded at the top of the file

### 🛡️ Later updated with:

* `@jwt_required()` to secure the route

---

## ✅ Step 5: JWT Authentication

### 📁 File Created:

* `app/auth.py`

### 🔧 What It Does:

* Defines `/login` route
* Accepts a username/password (from hardcoded dict)
* If valid, returns a JWT token
* This token is required to access `/chat`

### 🔗 Connections:

* `auth_bp` blueprint registered in `main.py`
* Token verified using `@jwt_required()` in `routes.py`
* Identity fetched with `get_jwt_identity()`

---

## 🔗 Summary of File Roles and Connections

| File              | Purpose                                        | Connected To                           |
| ----------------- | ---------------------------------------------- | -------------------------------------- |
| `.env`            | Store API keys securely                        | Used in `main.py`, `rag_pipeline.py`   |
| `run.py`          | Starts the app                                 | Imports `main.py`                      |
| `main.py`         | Initializes Flask, JWT, registers routes       | Uses `routes.py`, `auth.py`            |
| `routes.py`       | Defines `/chat` endpoint                       | Uses `rag_pipeline.py`, JWT decorators |
| `auth.py`         | Defines `/login` route                         | Uses `flask-jwt-extended`              |
| `rag_pipeline.py` | Loads PDF, builds vector DB, answers questions | Used in `routes.py`                    |

---

## ✅ What’s Ready

* Smart GPT answers from your own documents ✅
* Secure login with JWT ✅
* Protected API for `/chat` ✅

Next step? Stripe payment integration 💳 (Step 6)

Let me know if you want this as a PDF or copied into your README!
