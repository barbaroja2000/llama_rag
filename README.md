# Web Scraping Tool & Chat with X-Co - Streamlit App

This repository contains two primary tools:

1. **Web Scraping Tool** - A Python script designed to scrape content from given URLs.
2. **Chat with X-Co - Streamlit App** - An interactive chat application powered by the GPT model and Streamlit.

## 1. Web Scraping Tool

### Overview

This script extracts content from specified URLs, with special attention given to PDF content, which is extracted and saved as plain text. The tool supports multiprocessing, ensuring efficient scraping of multiple URLs concurrently.

### Features:

- Extract content from URLs and save it in specified directories.
- Extract content from PDFs and save it as plain text.
- Supports multiprocessing.
- Comprehensive logging.
- Automatically zips existing scraped data before a new run.

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

* OPENAI_API_KEY: Add to ``.streamlit/secrets.toml` as OPENAI_API_KEY=""
* MODEL: Specifies which GPT model version to use. Default is gpt-3.5-turbo-16k-0613.
* SYSTEM_PROMPT: Guides the GPT model on the context and scope of expected responses.
