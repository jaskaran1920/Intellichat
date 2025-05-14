import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

import os
'''Load PDFs
Split content into chunks
Convert chunks to embeddings
Store in FAISS
Ask questions using RetrievalQA'''

def load_and_index_documents(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split docs into smaller pieces
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    # Create embeddings
    print("API Key:", os.getenv("OPENAI_API_KEY"))

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore

'''This function:

Loads your PDF
Splits it into ~500-token chunks
Embeds those chunks
Stores them in a local FAISS index

'''

def ask_question(vectorstore, query: str):
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY")),
        retriever=vectorstore.as_retriever()
    )
    return qa_chain.run(query)
''' This function:

Takes your question
Retrieves relevant chunks from FAISS
Asks ChatGPT using that info
'''
if __name__ == "__main__":
    vs = load_and_index_documents("data_docs/sample.pdf")
    answer = ask_question(vs, "What is this document about?")
    print("Answer:", answer)
