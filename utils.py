import logging

def save_to_csv(businesses, filename='businesses.csv'):
    if not businesses:
        logging.error("No businesses to save to CSV")
        return

    keys = ['name', 'phone', 'website', 'address', 'hours', 'email']
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(businesses)
    
    logging.info(f"Saved {len(businesses)} businesses to {filename}")

def configure_logging(log_text):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()

    class TextHandler(logging.Handler):
        def emit(self, record):
            msg = self.format(record)
            log_text.insert('end', f"{msg}\n")
            log_text.yview(tk.END)

    handler = TextHandler()
    logger.addHandler(handler)
