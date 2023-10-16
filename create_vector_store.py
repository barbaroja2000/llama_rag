"""
Chat with X-Co - Streamlit App with direct Apify integration

This Streamlit application allows users to chat interactively with company data sourced from X-Co's website. By leveraging the capabilities of the GPT model, it provides answers to user queries by referencing indexed documents from the X-Co website.

Functionalities:
- Accepts configuration parameters like the company name, model type, start URL, and relevant API keys through command-line arguments.
- Validates the provided configuration parameters.
- Fetches and indexes content from the X-Co website using the Apify integration.
- Stores the OpenAI API key securely in `.streamlit/secrets.toml`.
- Stores other configuration parameters in the `.env` file for subsequent use.
- Interacts with the GPT model using the provided API key for real-time query processing.

Features:
- Real-time chat interface
- Typing simulation for a more immersive user experience
- Efficient document indexing for quick retrievals
- Secure handling and storage of API keys and other configuration parameters

Author: Al Jepps
Date: 12th Oct 2023
Version: 0.2
"""

# Standard Library Imports
import os
import argparse

from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI
from llama_index import download_loader
from llama_index.readers.schema.base import Document


# MODEL should be one of the pre-determined strings
ALLOWED_MODELS = ['gpt-3.5-turbo-16k-0613']

# Parse command line arguments
parser = argparse.ArgumentParser(description='Arguments for the script')
parser.add_argument('--company', type=str, required=True, help='Company name')
parser.add_argument('--gpt_name', type=str, required=True, help='GPT model name')
parser.add_argument('--start_url', type=str, required=True, help='Start URL')
parser.add_argument('--model', type=str, required=True, choices=ALLOWED_MODELS, help='Model string')
parser.add_argument('--openai_api_key', type=str, required=True, help='OpenAI API key')
parser.add_argument('--apify_api_key', type=str, required=True, help='Apify API key')
args = parser.parse_args()

COMPANY = args.company
GPT_NAME = args.gpt_name
START_URL = args.start_url
MODEL = args.model
APIFY_API_KEY = args.apify_api_key
OPENAI_API_KEY = args.openai_api_key

os.environ["OPENAI_API_KEY"] = args.openai_api_key

# Assert tests for the variables
# START_URL should be a valid URL
assert START_URL.startswith('http://') or START_URL.startswith('https://'), f"MY_VAR1 '{START_URL}' is not a valid URL"
assert MODEL in ALLOWED_MODELS, f"MODEL {MODEL} is not an allowed string"

# COMPANY should be a string
assert isinstance(COMPANY, str), f"COMPANY '{COMPANY}' is not a valid string"

# APIFY_API_KEY should be a string
assert isinstance(APIFY_API_KEY, str), f"APIFY_API_KEY '{APIFY_API_KEY}' is not a valid string"

# OPENAI_API_KEY should be a string
assert isinstance(OPENAI_API_KEY, str), f"APIFY_API_KEY '{OPENAI_API_KEY}' is not a valid string"


print("All tests passed!")

SYSTEM_PROMPT=f"""
You are the digital assistant for {COMPANY}'s website. 
Your primary role is to provide information related to {COMPANY}. 
Ensure your responses are factual and based on the content available on the website. 
If you're unsure of an answer, please indicate that you don't have that information.
"""

LLM=OpenAI(model=MODEL, temperature=0.0, system_prompt=SYSTEM_PROMPT)

# Converts a single record from the Actor's resulting dataset to the LlamaIndex format
def tranform_dataset_item(item):
    return Document(
        text=item.get("text"),
        extra_info={
            "url": item.get("url"),
        },
    )

ApifyActor = download_loader("ApifyActor")

reader = ApifyActor(APIFY_API_KEY)
documents = reader.load_data(
    actor_id="apify/website-content-crawler",
    run_input={"startUrls": [{"url":START_URL }]},
    dataset_mapping_function=tranform_dataset_item,
)

service_context = ServiceContext.from_defaults(llm=LLM)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
# save index
index.storage_context.persist(persist_dir="./vector_index")

# Save to .env
with open(".env", "w") as env_file:
    env_file.write(f"COMPANY={COMPANY}\n")
    env_file.write(f"GPT_NAME={GPT_NAME}\n")
    env_file.write(f"START_URL={START_URL}\n")
    env_file.write(f"MODEL={MODEL}\n")

# Save to .streamlit/secrets.toml 
with open(".streamlit/secrets.toml", "w") as secrets_file:
    secrets_file.write(f"OPENAI_API_KEY = \"{OPENAI_API_KEY}\"\n")


print("Complete!")