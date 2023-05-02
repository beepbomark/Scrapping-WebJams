import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def fetch_jams(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)

    return None

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

            jam_page_content = fetch_jams(jam_link)

            if jam_page_content:
                jam_page_soup = BeautifulSoup(jam_page_content, 'html.parser')
                description = jam_page_soup.find('div', class_='jam_content')

                if description and re.search(r'\$', description.text):
                    joined_count_element = jam_cell.find('span', class_='joined_count')
                    if joined_count_element:
                        count_text = joined_count_element.text.strip('()').split()[0]
                        count_text_no_commas = count_text.replace(',', '')
                        jam_joined = int(count_text_no_commas)
                    else:
                        jam_joined = 0

                    jam_data.append([jam_id, jam_link, jam_title, jam_joined, description.text.strip()])

        df = pd.DataFrame(jam_data, columns=['Jam ID', 'Jam Link', 'Jam Title', 'Joined Count', 'Description'])
        
        # Uncomment the next line to export the DataFrame to a CSV file
        df.to_csv('jam_data.csv', index=False)

        print(df)
    else:
        print("No content found.")
