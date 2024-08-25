import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import logging
import google.generativeai as genai

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_website(url):
    logging.info(f"Scraping website: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch the main URL: {e}")
        return []

    main_soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in main_soup.find_all('a') if link.get('href')]
    
    logging.debug(f"Found {len(links)} links on the main page")

    main_content = []

    for link in links:  # Limit to 10 links for demonstration
        full_link = link if link.startswith('http') else f"{url.rstrip('/')}/{link.lstrip('/')}"
        logging.debug(f"Processing link: {full_link}")
        try:
            link_response = requests.get(full_link, timeout=5)
            link_response.raise_for_status()
            soup = BeautifulSoup(link_response.text, 'html.parser')
            
            content = {"link": full_link}
            txt = ""

            # Iterate over all elements and add their text to the content list
            for element in soup.find_all(['h1', 'h2', 'p']):
                txt = txt+ " " +element.get_text(strip=True)

            content["text"] = txt

            # Join all the text together into a single string
            main_content.append(content)
            
        except requests.RequestException as e:
            logging.warning(f"Failed to scrape {full_link}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error when scraping {full_link}: {e}")

    return main_content

def process_website(url):
    print("Scraping website...")
    scraped_data = scrape_website(url)

    # print(scraped_data)

    # genai.configure(api_key="AIzaSyA9hLGJD5RjmB8OrAmwdL5zpSEzUiG3w1Y")

    # model = genai.GenerativeModel('gemini-1.5-flash')

    # query_template = "generate 10 questions from the following content, with length striclty less than 78 words: "
    # query = query_template + scraped_data

    # response = model.generate_content(query)
    # print(response.text)
    with open('scraped_data.json', 'w') as f:
        json.dump(scraped_data, f, indent=4)

 
if __name__ == "__main__":
    website_url = "https://www.anciitk.in/" 
    process_website(website_url)