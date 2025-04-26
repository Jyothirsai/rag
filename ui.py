import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings   
from langchain.schema import Document  # Import Document class
import tempfile
import os
from langchain_ollama import OllamaLLM
import asyncio
import nest_asyncio
nest_asyncio.apply()

def initialize_llm():
    return OllamaLLM(model="llama3.1:8b")

def load_text_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name
    with open(temp_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content

st.title("Code Generation for business use cases")
uploaded_file = st.file_uploader("Upload a Text file", type="txt")

if uploaded_file:
    try:
        st.info("Processing Uploaded Text File...")
        docs = load_text_file(uploaded_file)
        st.success("Text file loaded successfully!")

        # Convert the string into a list of Document objects
        documents = [Document(page_content=docs)]  # Wrap the string in a Document object

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = Chroma.from_documents(documents, embeddings, persist_directory="chroma_db")
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        chain = ConversationalRetrievalChain.from_llm(initialize_llm(), retriever=retriever, return_source_documents=True)
        
        query = st.text_input("Give a use case regarding businness:")
        if query:
            with st.spinner("Thinking..."):
                result = chain({"question": query, "chat_history": []})
                answer = result["answer"]
                st.write("Answer:", answer)
            


    except Exception as e: 
        st.error(f"An error occurred: {e}")