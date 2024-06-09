# Fishing Guide Scraper

Fishing Guide Scraper is a Python application designed to scrape fishing guide information from the website [localfishingguides.com](https://localfishingguides.com). The application uses BeautifulSoup for web scraping and Tkinter for a graphical user interface (GUI).

## Features

- Scrapes fishing guide information from multiple states.
- Collects guide details such as name, captain, phone number, email, website, Facebook URL, and profile URL.
- Saves the scraped data into a CSV file.
- Provides a GUI for easy interaction and monitoring of the scraping process.
- Logs scraping progress and errors in real-time within the application.

## Requirements

- Python 3.6+
- Requests
- BeautifulSoup4
- Tkinter

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/fishing-guide-scraper.git
    cd fishing-guide-scraper
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application:**

    ```sh
    python main.py
    ```

2. **Using the GUI:**

    - Enter the main URL to scrape (default is set to `https://localfishingguides.com/find-a-guide`).
    - Select the output CSV file location where the scraped data will be saved.
    - Click the "Start Scraping" button to begin the scraping process.
    - Monitor the scraping progress and logs in the provided text box within the application.

## File Structure

```plaintext
FishingGuideScraper/
│
├── fetch.py          # Handles fetching HTML content from URLs
├── scrape.py         # Contains functions to scrape the main page and guide pages
├── utils.py          # Utility functions for logging and error handling
├── gui.py            # Manages the GUI components and user interactions
├── main.py           # Entry point for the application
├── .gitignore        # Git ignore file to exclude certain files from the repository
└── README.md         # This README file
