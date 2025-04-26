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
    return OllamaLLM(model="llama3.1:8b",system="You are a an assistant.Always respond in English.")    

def load_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path=temp_file.name
    loader = PyPDFLoader(temp_path)
    documents=loader.load()
    return documents

st.set_page_config(page_title="PDF Chatbot")
st.title("Samsung User manual Chatbot")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chain" not in st.session_state and uploaded_file:
    try:
        with st.spinner("Processing your PDF..."):
            docs=load_pdf(uploaded_file)
            embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectordb=Chroma.from_documents(docs,embeddings,persist_directory="chroma_db")
            retriver=vectordb.as_retriever(search_kwargs={"k": 3})
            st.session_state.chain=ConversationalRetrievalChain.from_llm(
                llm=initialize_llm(),
                retriever=retriver,
                return_source_documents=True
            )
            st.success("PDF loaded successfully!")
    except Exception as e:
        st.error(f"Error loading PDF: {e}")
if "chain" in st.session_state:
    user_input = st.chat_input("Ask a question about the PDF:")
    if user_input:
        st.session_state.chat_history.append(("user",user_input))
        with st.spinner("Generating response..."):
            result=st.session_state.chain.invoke({"question": user_input,"chat_history": st.session_state.chat_history})
            answer=result["answer"]
            st.session_state.chat_history.append(("ai",answer))

    for role,msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)
