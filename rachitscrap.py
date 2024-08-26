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
    unique_links = set()
    count = 0
    relevant_links = []

    for link in links:
        # Construct full link if necessary
        full_link = link if link.startswith('http') else f"{url.rstrip('/')}/{link.lstrip('/')}"

        # Check if the link is unique and doesn't contain '#'
        if '#' not in full_link and full_link not in unique_links:
            unique_links.add(full_link)
            logging.debug(f"Processing link: {full_link}")

            try:
                link_response = requests.get(full_link, timeout=5)
                link_response.raise_for_status()  # Check for HTTP errors

                soup = BeautifulSoup(link_response.text, 'html.parser')

                title = soup.title.string.strip() if soup.title else "No Title Found"
                relevant_links.append({"link": full_link, "title": title})
                content = {"link": full_link}
                txt = ""

                # Iterate over all elements and add their text to the content list
                for element in soup.find_all(['h1', 'h2', 'p']):
                    txt += " " + element.get_text(strip=True)

                content["text"] = txt.strip() + '\n'  # Ensure each content ends with a newline
                main_content.append(content)
                
                count += 1
                if count == 5:  # Stop after processing exactly 5 unique links
                    break

            except requests.RequestException as e:
                logging.warning(f"Failed to scrape {full_link}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error when scraping {full_link}: {e}")

    return main_content, relevant_links

def parse_json_string(json_string):
    try:
        # Trim the string to get the JSON part between the first '[' and the last ']'
        start_index = json_string.find('[')
        end_index = json_string.rfind(']') + 1
        trimmed_json_string = json_string[start_index:end_index].strip()

        # Check if the trimmed string is empty
        if not trimmed_json_string:
            raise ValueError("No valid JSON data found in the string.")

        # Parse the JSON string
        parsed_json = json.loads(trimmed_json_string)
        return parsed_json
    
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None

def process_website(url):
    print("Scraping website...")
    scraped_data, relevent_links = scrape_website(url)

    print(scraped_data)
    print(relevent_links)

    with open('scraped_data.json', 'w') as f:
        json.dump(scraped_data, f, indent=4)

    genai.configure(api_key="AIzaSyA9hLGJD5RjmB8OrAmwdL5zpSEzUiG3w1Y")
    model = genai.GenerativeModel('gemini-1.5-flash')
    query_template = "from the following content generate 2 general questions, with length striclty less than 78 characters. (return a json array): "

    questions = []

    for(content) in scraped_data:
        
        query = query_template + content["text"]
        response = model.generate_content(query)
        q = parse_json_string(response.text)
        if q:
            questions = questions + q

    print(questions)

    outputdata = [
        {
            "url": url,
            "questions": questions,
            "relevant_links": relevent_links
        }
    ]

    with open('output.json', 'w') as f:
        json.dump(outputdata, f, indent=4)

if __name__ == "__main__":
    website_url = "https://overlayy.com/" 
    process_website(website_url)