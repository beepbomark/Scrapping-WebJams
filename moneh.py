import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_jams(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)

    return None

def find_dollar_sign(text):
    return "$" in text

if __name__ == '__main__':
    url = "https://itch.io/jams"
    html_content = fetch_jams(url)
    
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        jam_cells = soup.find_all('div', class_='jam_cell')

        jam_data = []

        for jam_cell in jam_cells:
            jam_id = jam_cell.get('data-jam_id')
            jam_link_element = jam_cell.find('a')
            jam_link = 'https://itch.io' + jam_link_element.get('href')
            jam_title = jam_link_element.text.strip()
            
            joined_count_element = jam_cell.find('span', class_='joined_count')
            if joined_count_element:
                count_text = joined_count_element.text.strip('()').split()[0]
                count_text_no_commas = count_text.replace(',', '')
                jam_joined = int(count_text_no_commas)
            else:
                jam_joined = 0

            # Fetch the jam page content
            jam_page_content = fetch_jams(jam_link)
            dollar_sentences = []

            if jam_page_content:
                jam_page_soup = BeautifulSoup(jam_page_content, 'html.parser')
                paragraphs = jam_page_soup.find_all('p')

                for paragraph in paragraphs:
                    if find_dollar_sign(paragraph.text):
                        dollar_sentences.append(paragraph.text.strip())

            if dollar_sentences:  # Only add jam data if dollar_sentences is not empty
                jam_data.append({
                    'Jam ID': jam_id,
                    'Jam Link': jam_link,
                    'Jam Title': jam_title,
                    'Joined Count': jam_joined,
                    'Dollar Sentences': ' | '.join(dollar_sentences)
                })

        df = pd.DataFrame(jam_data)
        df.to_csv('jam_data_with_dollar_signs.csv', index=False)

        print(df)
    else:
        print("No content found.")
