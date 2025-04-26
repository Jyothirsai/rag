import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings   
from langchain.schema import Document  # Import Document class
import tempfile
import os
import json
from langchain_ollama import OllamaLLM
import asyncio
import nest_asyncio
nest_asyncio.apply()

def initialize_llm():
    return OllamaLLM(model="llama3.1:8b")

def load_json_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name
    with open(temp_path, "r", encoding="utf-8") as file:
        content = json.load(file)  # Load JSON content
    return content

st.title("JSON File Summarizer and Q&A")
uploaded_file = st.file_uploader("Upload a JSON file", type="json")

if uploaded_file:
    try:
        st.info("Processing Uploaded JSON File...")
        data = load_json_file(uploaded_file)
        st.success("JSON file loaded successfully!")

        # Convert JSON data into a string for processing
        json_string = json.dumps(data, indent=2)
        st.write("JSON Data Preview:", json_string[:500])  # Show a preview of the JSON data

        # Convert the JSON string into a list of Document objects
        documents = [Document(page_content=json_string)]

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = Chroma.from_documents(documents, embeddings, persist_directory="chroma_db")
        retriever = vectordb.as_retriever(search_kwargs={"k": 3})
        chain = ConversationalRetrievalChain.from_llm(initialize_llm(), retriever=retriever, return_source_documents=True)
        
        st.subheader("Summarize the JSON Data")
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                summary_prompt = f"Summarize the following JSON data:\n\n{json_string[:1000]}"
                summary = chain({"question": summary_prompt, "chat_history": []})["answer"]
                st.success(summary)

        st.subheader("Ask a Question About the JSON Data")
        query = st.text_input("Ask a question:")
        if query:
            with st.spinner("Thinking..."):
                full_prompt = f"Here's the JSON data:\n\n{json_string}\n\nAnswer this question: {query}"
                response = chain({"question": full_prompt, "chat_history": []})["answer"]
                st.success(response)
    except Exception as e: 
        st.error(f"An error occurred: {e}")