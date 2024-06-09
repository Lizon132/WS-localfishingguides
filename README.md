# Web Scraper Application

This Python application is designed to scrape business directory data from a specified URL and save the extracted data to a CSV file. The application features a graphical user interface (GUI) built with Tkinter and uses the Google Custom Search API to find missing email addresses.

## Features

- Scrapes business data from multiple pages of a business directory.
- Extracts information such as business name, phone number, website, physical address, operating hours, and email address.
- Uses Google Custom Search API to find missing email addresses.
- Displays progress and logs in the GUI during the scraping process.
- Saves the scraped data to a CSV file.

## Requirements

- Python 3.x
- `beautifulsoup4`
- `requests`
- `google-api-python-client`
- `tkinter` (usually included with Python)

## Setup

### 1. Install Dependencies

Ensure you have all necessary dependencies installed. Run this command in your terminal:

```sh
pip install -r requirements.txt
