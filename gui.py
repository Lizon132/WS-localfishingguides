import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import logging
import threading
from scrape import scrape_main_page, scrape_guide_page
import csv
import time
from utils import configure_logging

def select_output_file(output_file_var):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        output_file_var.set(file_path)

def start_scraping_thread(url_entry, output_file_var, log_text):
    main_url = url_entry.get()
    output_csv = output_file_var.get()
    
    if not main_url or not output_csv:
        messagebox.showwarning("Input Error", "Please provide both the main URL and the output CSV file path.")
        return
    
    log_text.delete(1.0, tk.END)
    thread = threading.Thread(target=scrape_fishing_guides, args=(main_url, output_csv, log_text))
    thread.start()

def scrape_fishing_guides(main_url, output_csv, log_text):
    try:
        logging.info(f"Starting to scrape fishing guides from: {main_url}")
        guide_links = scrape_main_page(main_url, log_text)
        
        with open(output_csv, mode='w', newline='', encoding='utf-8') as file:  # Specify UTF-8 encoding
            writer = csv.writer(file)
            writer.writerow(['State', 'Location', 'Guide Name', 'Captain', 'Phone', 'Email', 'Website', 'Facebook', 'Profile URL'])
            
            records_written = False
            for guide in guide_links:
                state = guide['state']
                guide_url = guide['url']
                location = guide['location']
                try:
                    guides = scrape_guide_page(guide_url, state, location, log_text)
                    if not guides:
                        logging.error(f"No guides found for {guide_url}")
                        continue
                    for guide in guides:
                        writer.writerow([
                            guide['state'],
                            guide['location'],
                            guide['name'],
                            guide['captain'],
                            guide['phone'],
                            guide['email'],
                            guide['website'],
                            guide['facebook'],
                            guide['profile_url']
                        ])
                        logging.info(f"Written guide to CSV: {guide}")
                        records_written = True
                    file.flush()  # Ensure each batch is written to the file
                    logging.info(f"Scraped data: {guides}")
                except ValueError as e:
                    logging.error(f"Error: {e}")
                    messagebox.showerror("Error", str(e))
                time.sleep(1)  # Pause between requests to avoid overwhelming the server
            if not records_written:
                raise ValueError("No records were written to the CSV file.")
        messagebox.showinfo("Success", f"Data has been successfully scraped and saved to {output_csv}")
    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_gui():
    root = tk.Tk()
    root.title("Fishing Guide Scraper")

    # Main URL input
    tk.Label(root, text="Main URL:").grid(row=0, column=0, padx=10, pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=10, pady=10)
    url_entry.insert(0, "https://localfishingguides.com/find-a-guide")  # Default URL

    # Output file selection
    tk.Label(root, text="Output CSV File:").grid(row=1, column=0, padx=10, pady=10)
    output_file_var = tk.StringVar()
    output_file_entry = tk.Entry(root, textvariable=output_file_var, width=50)
    output_file_entry.grid(row=1, column=1, padx=10, pady=10)
    output_file_button = tk.Button(root, text="Browse...", command=lambda: select_output_file(output_file_var))
    output_file_button.grid(row=1, column=2, padx=10, pady=10)

    # Log text box
    log_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
    log_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    # Configure logging to use the log text box
    configure_logging(log_text)

    # Start button
    start_button = tk.Button(root, text="Start Scraping", command=lambda: start_scraping_thread(url_entry, output_file_var, log_text))
    start_button.grid(row=3, column=0, columnspan=3, pady=20)

    # Start the GUI event loop
    root.mainloop()
