"""
Web Scraping Tool

This script is designed to scrape content from given URLs and save the extracted content
into specified output directories. PDF content is extracted and saved as text.
The script also supports multiprocessing for efficient scraping.

Usage:
    $ python script_name.py [--test_run] [--output OUTPUT_DIR] [--spider SPIDER_DIR]
"""

import os
import json
import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
import random
import string
import logging
from urllib.parse import urlparse, unquote
import PyPDF2
from io import BytesIO
import argparse
import os
import shutil
import zipfile
from datetime import datetime

# Setting up command-line arguments
parser = argparse.ArgumentParser(description='Web scraping tool.')
parser.add_argument('--test_run', action='store_true', help='Set to test mode. Defaults to false.')
parser.add_argument('--output', type=str, default='output', help='Set the output directory.')
parser.add_argument('--spider', type=str, default='spider.json', help='Set the spider directory.')

args = parser.parse_args()

# Define the main scraped directory
SCRAPED_DIR = 'scraped'

# Handle test_run argument
if args.test_run:
    output_directory = os.path.join(SCRAPED_DIR, 'test')
    spider = 'test.json'
else:
    output_directory = os.path.join(SCRAPED_DIR, args.output)
    spider = args.spider

def extract_pdf_content(content):
    """
    Extracts text from a given PDF content.

    Args:
        content (bytes): PDF content.

    Returns:
        str: Extracted text from the PDF.
    """
    with BytesIO(content) as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(0,len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

logging.basicConfig(level=logging.INFO)

def random_filename():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(10))

def suggested_filename_from_response(response):
    """
    Extracts filename from the content-disposition response header.
    
    Args:
        response (requests.Response): HTTP response.

    Returns:
        str or None: Suggested filename or None if not found.
    """
    content_disposition = response.headers.get('content-disposition')
    if content_disposition:
        fname = re.findall("filename=(.+)", content_disposition)
        if len(fname) == 0:
            return None
        return fname[0]
    return None

def generate_filename_from_url(url):
    """Generates a filename based on the given URL."""
    parsed_url = urlparse(url)
    basename = os.path.basename(unquote(parsed_url.path))
    if not basename:
        basename = "page"
    random_string = random_filename()
    return f"{basename}_{random_string}"

def download_page(url):
    """Downloads the given URL and returns the content and response."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    try:
        with requests.Session() as session:
            response = session.get(url, headers=headers)
            response.raise_for_status()
            return response.content, response  # Return content and response
    except requests.RequestException as e:
        logging.error(f"Error downloading {url}: {e}")
        return None, None

def process_page(args):
    """Processes a given webpage, extracts its content and saves it."""
    entry, download_folder = args
    url = entry["url"]
    content, response = download_page(url)

    # Check if the content is None. If so, log an error and return.
    if content is None:
        logging.error(f"Failed to download content from {url}")
        return None

# Check content type
    if response and "application/pdf" in response.headers.get("Content-Type", ""):
        text = extract_pdf_content(content)
        file_extension = "txt"  # You can choose to save the extracted content as .txt
    else:
        # The existing logic for non-PDF content
        soup = BeautifulSoup(content, 'html.parser')
        
        for tag in soup.find_all(['header', 'footer', 'nav', 'script', 'style']):
            tag.decompose()

        text_parts = [tag.get_text(separator=' ').strip() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'li'])]
        text = ' '.join(text_parts)
        text = ' '.join(text.split())
        text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
        file_extension = "txt"
    
    # Generating the filename based on content type
    suggested_name = suggested_filename_from_response(response)
    if suggested_name:
        file_base_name = f"{suggested_name}_{random_filename()}"
    else:
        file_base_name = generate_filename_from_url(url)

    # Updated directory path to include the "scraped" main directory
    os.makedirs(output_directory, exist_ok=True)

    text_filename = os.path.join(output_directory, f"{file_base_name}.{file_extension}")
    with open(text_filename, 'w') as text_file:
        text_file.write(text)

    logging.info(f"Processed: {url}")
    entry["file_on_disk"] = text_filename
    return entry

if __name__ == "__main__":

        # Modified directory-checking logic
    if os.path.exists(output_directory):
        # Zip the directory
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        zip_filename = f'{output_directory}_{timestamp}'
        shutil.make_archive(zip_filename, 'zip', output_directory)
        
        # Empty the directory
        for filename in os.listdir(output_directory):
            file_path = os.path.join(output_directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    with open(spider, "r") as json_file:
        data = json.load(json_file)

    with Pool(4) as pool:
        args = [(entry, output_directory) for entry in data]
        updated_data = pool.map(process_page, args)

    print(json.dumps([item for item in updated_data if item], indent=4))