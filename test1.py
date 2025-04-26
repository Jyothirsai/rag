import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings   
from langchain.document_loaders import PyPDFLoader
import tempfile
import os
from langchain_ollama import OllamaLLM
import asyncio
import nest_asyncio
nest_asyncio.apply()

def initialize_llm():
    return OllamaLLM(model="llama3.1:8b")

def load_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path=temp_file.name
    loader = PyPDFLoader(temp_path)
    documents=loader.load()
    return documents


st.title("Samsung User manual Chatbot")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    try:
        st.info("Processinng Uploaded PDF...")
        docs=load_pdf(uploaded_file)
        st.success("PDF loaded successfully!")

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb=Chroma.from_documents(docs, embeddings, persist_directory="chroma_db")
        retriever=vectordb.as_retriever(search_kwargs={"k": 3})
        chain=ConversationalRetrievalChain.from_llm(initialize_llm(), retriever=retriever, return_source_documents=True)
        
        query=st.text_input("Ask a question about your PDF:")
        if query:
            st.spinner("tHINKING...")
            result=chain.invoke({"question": query,"chat_history": []})
            answer=result["answer"]
            st.write("Answer:",answer)
    except Exception as e: 
        st.error(f"An error occurred: {e}")