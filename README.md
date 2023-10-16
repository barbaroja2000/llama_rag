# Web Scraping Tool & Chat with X-Co - Streamlit App

This repository contains tools:

1. **Web Scraping Tool** `get_data.py` - A Python script designed to scrape content from given URLs. Use this for full customization of apify scraping output
2. **Chat with X-Co - Streamlit App** `llama.py` - An interactive chat application powered by the GPT model and Streamlit, uses with the Custom Tool
3. **Chat with X-Co - Streamlit App with direct Apify Intergration** `create_vector_store.py` && `llama_apify.py`

## 1. Web Scraping Tool

### Overview

This script extracts content from specified URLs, with special attention given to PDF content, which is extracted and saved as plain text. The tool supports multiprocessing, ensuring efficient scraping of multiple URLs concurrently.

### Features:

- Extract content from URLs and save it in specified directories.
- Extract content from PDFs and save it as plain text.
- Supports multiprocessing.
- Comprehensive logging.
- Automatically zips existing scraped data before a new run.

### Setup:

Application uses a spidered json array for content to scrape. Apify.com is one way of doing this and it provides a free plan to get started. Output expected from the scraper is as follows.

```json
 {
    "url": "{url}",
    "pageTitle": "{page-title}",
    "h1": "{h1}",
    "first_h2": "{h2}",
    "random_text_from_the_page": ""
  }
```

### Usage:

```bash
$ python script_name.py [--test_run] [--output OUTPUT_DIR] [--spider SPIDER_DIR]
```

# Chat with X-Co - Streamlit App

This Streamlit application provides an interactive chat experience for users to interact with X-Co company's data. Leveraging the GPT model, the application delivers accurate and relevant answers by referencing indexed X-Co documents.

### Features

- **Real-time Chat Interface**: Users can communicate in real time and receive instant responses.
- **Typing Simulation**: Enhances the chat interaction by simulating typing for a more realistic user experience.
- **Efficient Document Indexing**: Rapidly retrieves information from indexed X-Co documents.

## Setup and Usage

1. **Installation**:
   Ensure you have Streamlit and other dependencies installed. If not, install via pip:

   ```bash
   pip install -r requirements.txt
   ```

2. **Running the App**:
Navigate to the directory containing the app's script and run:

```bash
streamlit run llama.py
```

3. **Configuration**:

* OPENAI_API_KEY: Add to `.streamlit/secrets.toml` as OPENAI_API_KEY=""
* MODEL: Add to `.env` as MODEL="" 
* COMPANY: Add to `.env` as COMPANY="" 
* GPT_NAME: Add to `.env` as GPT_NAME="" 
* START_URL: Add to `.env` as START_URL="" 
* GPT_NAME: Add to `.env` as GPT_NAME="" 

See `.streamlit/secrets.default` & `.env.default`

# Chat with X-Co - Streamlit App with direct apify integration

This Streamlit application provides an interactive chat experience for users to interact with X-Co company's data. Leveraging the GPT model, the application delivers accurate and relevant answers by referencing indexed X-Co documents. 

### Features

- **Real-time Chat Interface**: Users can communicate in real time and receive instant responses.
- **Typing Simulation**: Enhances the chat interaction by simulating typing for a more realistic user experience.
- **Efficient Document Indexing**: Rapidly retrieves information from indexed X-Co documents.

## Setup and Usage

1. **Installation**:
   Ensure you have Streamlit and other dependencies installed. If not, install via pip:

   ```bash
   pip install -r requirements.txt
   ```

2. **Running the App**:

Two part process, first spider and persist to index via `create_vector_store.py`

```bash
python create_vector_store.py --company "X-Co" --gpt_name "GPT-4" --start_url "https://example.com" --model "gpt-3.5-turbo-16k-0613" --openai_api_key "YOUR_OPENAI_KEY" --apify_api_key "YOUR
```


Then:
Navigate to the directory containing the app's script and run:

```bash
streamlit run llama_apify.py
```

3. **Configuration**:

* Dynamically created via CLI arguments to `create_vector_store.py`