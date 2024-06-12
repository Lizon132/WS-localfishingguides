import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading
import logging
from scrape import scrape_main_page, scrape_profile_page
from utils import save_to_csv, configure_logging
from email_finder import find_email_google, find_email_whois
import re
import config  # Import the configuration file

def start_scraping(url, log_text, progress_var, api_key, cse_id):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    log_text.insert('end', f"Starting scrape for {url}\n")
    businesses = scrape_main_page(url, log_text)

    total_businesses = len(businesses)
    for idx, business in enumerate(businesses):
        profile_data = scrape_profile_page(business['profile_url'], log_text)
        business.update(profile_data)
        business.pop('profile_url')  # Remove profile_url from the final data

        # Find email using Google Custom Search if not found
        if not business.get('email'):
            email = find_email_google(business['name'], api_key, cse_id)
            business['email'] = email
        
        # If email is still not found, use WHOIS lookup
        if not business.get('email') and business.get('website'):
            domain = re.sub(r'^https?://', '', business['website']).split('/')[0]
            email = find_email_whois(domain)
            business['email'] = email

        # Update progress
        progress = (idx + 1) / total_businesses * 100
        progress_var.set(progress)

    save_to_csv(businesses)
    log_text.insert('end', "Scraping completed and data saved to CSV\n")

def start_scraping_thread(url, log_text, progress_var, api_key, cse_id):
    threading.Thread(target=start_scraping, args=(url, log_text, progress_var, api_key, cse_id)).start()

def create_gui():
    root = tk.Tk()
    root.title("Web Scraper")

    tk.Label(root, text="Enter URL:").grid(row=0, column=0, padx=10, pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=10, pady=10)

    log_text = scrolledtext.ScrolledText(root, width=80, height=20)
    log_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

    # Configure logging to write to the log_text widget
    configure_logging(log_text)

    def on_scrape():
        url = url_entry.get()
        log_text.delete(1.0, tk.END)
        progress_var.set(0)
        start_scraping_thread(url, log_text, progress_var, config.API_KEY, config.CSE_ID)

    scrape_button = tk.Button(root, text="Scrape", command=on_scrape)
    scrape_button.grid(row=0, column=2, padx=10, pady=10)

    root.mainloop()
