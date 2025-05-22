import os #Loads the os module.
from dotenv import load_dotenv #Loads the environment variables from the .env file.
import openai #Loads the OpenAI API key from the .env file.

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") # this os.getenv is a function from python os module is used to get the OpenAI API key from the .env file.
from langchain_community.document_loaders import PyPDFLoader #Loads the PyPDFLoader from the langchain_community library.
from langchain.text_splitter import RecursiveCharacterTextSplitter #Loads the RecursiveCharacterTextSplitter from the langchain library.
from langchain.chains import RetrievalQA #Loads the RetrievalQA chain from the langchain library.
from langchain_community.vectorstores import FAISS #Loads the FAISS vector store from the langchain_community library.
from langchain_openai import OpenAIEmbeddings, ChatOpenAI #Loads the OpenAIEmbeddings and ChatOpenAI from the langchain_openai library.

import os
'''Load PDFs
Split content into chunks
Convert chunks to embeddings
Store in FAISS
Ask questions using RetrievalQA'''

def load_and_index_documents(pdf_path: str):
    loader = PyPDFLoader(pdf_path)  # Load the PDF file
    documents = loader.load()


    # Split docs into smaller pieces
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50) # recursi

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
from langchain_community.document_loaders.csv_loader import CSVLoader

def load_and_index_csv(csv_path: str):
    loader = CSVLoader(file_path=csv_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore




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
