"""
Chat with X-Co - Streamlit App

This Streamlit application enables users to chat with company Data.
Users can ask questions related to X-Co, and the application provides relevant answers 
by interacting with the GPT model and referencing the indexed X-Co documents.

Features:
- Real-time chat interface
- Typing simulation for a more interactive user experience
- Efficient document indexing for quick retrievals

Author: Al Jepps
Date: 12th Oct 2023
Version: 0.1
"""

# Standard Library Imports
import time

# External Imports
import openai
import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, SimpleDirectoryReader
from llama_index.llms import OpenAI

# Constants
PAGE_TITLE = "Chat with X-Co"
#OPENAI_API_KEY = st.secrets.OPENAI_API_KEY
INPUT_DIR="scraped/{some-dir}"
MODEL="gpt-3.5-turbo-16k-0613"
SYSTEM_PROMPT="""
"You are an assistant for the X-Co Website, and your job is to answer questions. 
Assume that all questions are related to X-Co. 
Keep your answers based on facts do not make things up - if you dont know say so."
"""

# Streamlit App Configuration
st.set_page_config(page_title=PAGE_TITLE, page_icon="🗿", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the X-CoGPT 🗿")

# Initialize the chat messages history     
if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about X-Co"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading Axiologik Docs. This may take 1-2 minutes.."):
        reader = SimpleDirectoryReader(input_dir=INPUT_DIR, recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model=MODEL, temperature=0.5, system_prompt=SYSTEM_PROMPT))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

# Initialize the chat engine
if "chat_engine" not in st.session_state.keys(): 
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True, streaming=True)

# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display the prior chat messages
for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate a new assistant's response if the last message wasn't from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    message_placeholder = st.empty()
    full_response = ""
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            total_response = ""

            response = st.session_state.chat_engine.stream_chat(prompt)
            for token in response.response_gen:
                full_response += token + ""
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history