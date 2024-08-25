import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import logging

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

    scraped_data = []
    for link in links[:10]:  # Limit to 10 links for demonstration
        full_link = link if link.startswith('http') else f"{url.rstrip('/')}/{link.lstrip('/')}"
        logging.debug(f"Processing link: {full_link}")
        try:
            link_response = requests.get(full_link, timeout=5)
            link_response.raise_for_status()
            soup = BeautifulSoup(link_response.text, 'html.parser')
            
            h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]
            h2_tags = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
            a_tags = [{'text': a.get_text(strip=True), 'href': a.get('href')} 
                      for a in soup.find_all('a') if a.get('href')]
            
            main_content = ' '.join([p.get_text(strip=True) for p in soup.find_all('p')])[:1000]
            
            scraped_data.append({
                'url': full_link,
                'h1_tags': h1_tags,
                'h2_tags': h2_tags,
                'a_tags': a_tags[:10],
                'main_content': main_content
            })
            logging.debug(f"Successfully scraped {full_link}")
        except requests.RequestException as e:
            logging.warning(f"Failed to scrape {full_link}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error when scraping {full_link}: {e}")
    
    logging.info(f"Scraped {len(scraped_data)} links")
    return scraped_data

# Function to generate questions using an LLM (example using OpenAI's GPT)
# Function to generate questions using Gemini
def generate_questions(content):
    # Replace with the actual way to initialize and authenticate with Gemini
    gemini_api_key = 'AIzaSyA9hLGJD5RjmB8OrAmwdL5zpSEzUiG3w1Y'  # Replace with your actual Gemini API key
    
    # Example API request to Gemini (this will vary depending on Gemini's API)
    response = requests.post(
        url="https://api.gemini.ai/v1/question-generation",
        headers={"Authorization": f"Bearer {gemini_api_key}"},
        json={
            "content": content,
            "max_questions": 10,
            "max_characters": 80
        }
    )

    if response.status_code == 200:
        questions = response.json().get('questions', [])
    else:
        print(f"Failed to generate questions: {response.status_code}, {response.text}")
        questions = []

    return questions


# Function to find relevant links (here simply selecting the first 5 links)
def find_relevant_links(links):
    return links[:5]

# Main function to process the website and generate the structured JSON
def process_website(base_url):
    sd = scrape_website(base_url)
    print(sd)
    data = []

    questions = generate_questions(sd)
    # relevant_links = find_relevant_links(sd)

    entry = {
        "url": "link",
        "questions": questions,
        # "relevant_links": [{"url": rl, "title": rl} for rl in relevant_links]
    }
    data.append(entry)

    print(entry)

    # for link in scraped_links:
    #     content = get_page_content(link)
    #     if not content:
    #         continue

    #     questions = generate_questions(content)
    #     relevant_links = find_relevant_links(scraped_links)

    #     entry = {
    #         "url": link,
    #         "questions": questions,
    #         "relevant_links": [{"url": rl, "title": rl} for rl in relevant_links]
    #     }
    #     data.append(entry)

    # Save the results in a structured JSON file
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=4)

# Run the process on a sample website
process_website('https://anciitk.in/')  # Replace with the actual URL
