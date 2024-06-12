import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

def get_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def scrape_main_page(url, log_text):
    businesses = []
    page = 1

    while True:
        page_url = f"{url}?page={page}"
        try:
            log_text.insert('end', f"Scraping main page: {page_url}\n")
            html_content = get_html(page_url)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            business_elements = soup.select('.grid_element')

            if not business_elements:
                break  # Exit the loop if no more business elements are found

            for element in business_elements:
                name_tag = element.select_one('a[title]')
                phone_tag = element.select_one('.member-search-phone')
                profile_url_tag = element.select_one('a.center-block[title]')
                
                if name_tag and profile_url_tag:
                    name = name_tag.get('title').strip()
                    phone = phone_tag.get_text(strip=True) if phone_tag else ''
                    profile_url = urljoin(url, profile_url_tag.get('href'))
                    
                    businesses.append({
                        'name': name,
                        'phone': phone,
                        'profile_url': profile_url
                    })

            log_text.insert('end', f"Found {len(business_elements)} businesses on page {page}\n")
            page += 1
        except Exception as e:
            logging.error(f"Error scraping main page: {e}")
            log_text.insert('end', f"Error scraping main page: {e}\n")
            break

    return businesses

def scrape_profile_page(profile_url, log_text):
    try:
        log_text.insert('end', f"Scraping profile page: {profile_url}\n")
        html_content = get_html(profile_url)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        website_tag = soup.select_one('.weblink')
        address_tag = soup.select_one('.bold:contains("Location") + div')
        hours_tag = soup.select_one('.bold:contains("Hours of Operation") + div')
        email_tag = soup.select_one('a[href^="mailto:"]')
        
        website = website_tag.get('href').strip() if website_tag else ''
        address = address_tag.get_text(strip=True) if address_tag else ''
        hours = hours_tag.get_text(strip=True) if hours_tag else ''
        email = email_tag.get('href').replace('mailto:', '').strip() if email_tag else ''
        
        log_text.insert('end', f"Scraped profile page: {profile_url}\n")
        return {
            'website': website,
            'address': address,
            'hours': hours,
            'email': email
        }
    except Exception as e:
        logging.error(f"Error scraping profile page {profile_url}: {e}")
        log_text.insert('end', f"Error scraping profile page {profile_url}: {e}\n")
        return {
            'website': '',
            'address': '',
            'hours': '',
            'email': ''
        }
