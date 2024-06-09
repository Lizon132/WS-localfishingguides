from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import time
from fetch import get_html
import tkinter as tk  # Import tkinter to use tk.END and log_text.yview

def scrape_main_page(url, log_text):
    try:
        logging.info(f"Scraping main page: {url}")
        html_content = get_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        state_sections = soup.select('.col-md-12 > .row')
        guide_links = []
        current_state = None

        for section in state_sections:
            state_header = section.select_one('h3')
            if state_header:
                current_state = state_header.get_text()
            guides = section.select('.waters-list > li > a')
            logging.info(f"Found {len(guides)} guides in {current_state}")
            for guide in guides:
                guide_url = urljoin(url, guide['href'])  # Convert to absolute URL
                guide_location = guide.get_text()
                guide_links.append({'state': current_state, 'url': guide_url, 'location': guide_location})
                log_text.insert(tk.END, f"Found guide page: {guide_url} in {current_state}\n")
                log_text.yview(tk.END)
        
        return guide_links
    except Exception as e:
        logging.error(f"Error scraping main page: {e}")
        raise

def scrape_guide_page(url, state, location, log_text):
    try:
        logging.info(f"Scraping guide page: {url}")
        log_text.insert(tk.END, f"Scraping URL: {url}\n")
        log_text.yview(tk.END)
        
        html_content = get_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Verify the table location
        table = soup.select_one('#table tbody')
        if not table:
            logging.error(f"Table not found on {url}")
            return []
        
        table_rows = table.select('tr')
        logging.info(f"Found {len(table_rows)} rows in the table on {url}")

        guides = []

        for row in table_rows:
            guide_link = row.select_one('h4 a')
            if guide_link:  # Skip rows without guide data
                try:
                    name = guide_link.get_text()
                    captain = row.select_one('td > p').get_text()
                    phone = row.select_one('a[href^="tel:"]').get_text() if row.select_one('a[href^="tel:"]') else ''
                    email = row.select_one('a[href^="mailto:"]').get_text() if row.select_one('a[href^="mailto:"]') else ''
                    website = row.select_one('a[target="_blank"][rel="nofollow"]').get('href') if row.select_one('a[target="_blank"][rel="nofollow"]') else ''
                    facebook = row.select('a[href*="facebook.com"]')[-1].get('href') if row.select('a[href*="facebook.com"]') else ''
                    profile_url = urljoin(url, row.select_one('.btn.btn-primary')['href']) if row.select_one('.btn.btn-primary') else ''
                    
                    # Debug prints
                    logging.info(f"Scraped data from {url}: Name: {name}, Captain: {captain}, Phone: {phone}, Email: {email}, Website: {website}, Facebook: {facebook}, Profile URL: {profile_url}")
                    
                    guides.append({
                        'state': state,
                        'location': location,
                        'name': name,
                        'captain': captain,
                        'phone': phone,
                        'email': email,
                        'website': website,
                        'facebook': facebook,
                        'profile_url': profile_url
                    })
                except Exception as e:
                    logging.error(f"Error scraping guide data from {url}: {e}")
        
        if not guides:
            logging.error(f"No guides found on {url}")
        return guides
    except Exception as e:
        logging.error(f"Error scraping guide page {url}: {e}")
        raise
