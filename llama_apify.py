"""
Chat with X-Co - Streamlit App with direct Apify integration

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
import os
import subprocess
from types import SimpleNamespace

# External Imports
import openai
import streamlit as st
from llama_index.llms import OpenAI
from llama_index import download_loader, set_global_handler, load_index_from_storage, StorageContext


from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Set local variables using the environment variables
COMPANY = os.getenv('COMPANY')
GPT_NAME = os.getenv('GPT_NAME')
START_URL = os.getenv('START_URL')
MODEL = os.getenv('MODEL')


# Assert tests for the variables
# START_URL should be a valid URL
assert START_URL.startswith('http://') or START_URL.startswith('https://'), f"MY_VAR1 '{START_URL}' is not a valid URL"

# MODEL should be one of the pre-determined strings
ALLOWED_MODELS = ['gpt-3.5-turbo-16k-0613']
assert MODEL in ALLOWED_MODELS, f"MODEL {MODEL} is not an allowed string"

# COMPANY should be a string
assert isinstance(COMPANY, str), f"COMPANY '{COMPANY}' is not a valid string"

print("All tests passed!")


PAGE_TITLE = f"Chat with {GPT_NAME}"
SYSTEM_PROMPT=f"""
You are the digital assistant for {COMPANY}'s website. 
Your primary role is to provide information related to {COMPANY}. 
Ensure your responses are factual and based on the content available on the website. 
If you're unsure of an answer, please indicate that you don't have that information.
"""

LLM=OpenAI(model=MODEL, temperature=0.0, system_prompt=SYSTEM_PROMPT)

set_global_handler("simple")

# Streamlit App Configuration
st.set_page_config(page_title=PAGE_TITLE, page_icon="🗿", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title(f"Chat with the {GPT_NAME} 🗿")

# Initialize the chat messages history     
if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [
        {"role": "assistant", "content": f"Ask me a question about {COMPANY}"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading Docs..."):
        # to load index later, make sure you setup the storage context
        # this will loaded the persisted stores from persist_dir
        storage_context = StorageContext.from_defaults(
            persist_dir="./vector_index"
        )
        index = load_index_from_storage(storage_context)
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

            response = st.session_state.chat_engine.stream_chat(prompt)
            for token in response.response_gen:
                full_response += token + ""
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history