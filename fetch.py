import requests
import logging

def get_html(url):
    try:
        logging.debug(f"Fetching URL: {url}")
        print(f"Fetching URL: {url}")  # Debug print
        response = requests.get(url)
        response.raise_for_status()
        print(f"Fetched URL successfully: {url}")  # Debug print
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        print(f"Error fetching {url}: {e}")  # Debug print
        raise
