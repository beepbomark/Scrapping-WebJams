import re
import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        print("Error fetching URL:", e)

    return None

url = "https://itch.io/jam/boba-design-jam-2-prizes-"
url = "https://itch.io/jam/bullet-hell-jam-2023"
html_content = fetch_html(url)
if html_content:
    soup = BeautifulSoup(html_content, 'html.parser')
    description = soup.find('div', class_='jam_content')
    if description and re.search(r'\$', description.text):
        print("Found")
    else:
        print(description)
