# Import necessary libraries
import requests                                                                 # Import the `requests` library to make HTTP requests to web pages.
from bs4 import BeautifulSoup                                                   # Import `BeautifulSoup` from the `bs4` library to parse HTML content.
import pandas as pd                                                             # Import the `pandas` library and use the alias `pd` to work with data in a DataFrame format.
import re                                                                       # Import the `re` library to work with regular expressions.
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

def write_to_sheet(df):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    # Load the credentials from the GOOGLE_CREDS environment variable
    creds_json = json.loads(os.getenv('GOOGLE_CREDS'))
    
    client = gspread.service_account_from_dict(creds_json, scope)
    
    # Find a workbook by name and open the first sheet
    sheet = client.open("Game Jam Web Scrapping").sheet1

    # Clear existing content
    sheet.clear()
    
    # Convert all int64 values to native Python int
    for col in df.columns:
        if df[col].dtype == 'int64':
            df[col] = df[col].astype(int)

    # Write DataFrame to Google Sheet
    for i in range(len(df)):
        row = df.iloc[i].tolist()
        index = i+1
        sheet.insert_row(row, index)

# Define a helper function to check if a dollar sign is present in the given text
def find_dollar_sign(text):
    return "$" in text                                                          # Check if the dollar sign is in the given text and return the result as a boolean.

# Define a helper function to fetch the HTML content of a given URL
def fetch_html(url):
    # Attempt to fetch the content of the given URL.
    try:
        response = requests.get(url)
        # If successful, return the text content of the response
        if response.status_code == 200:
            return response.text
    except requests.exceptions.RequestException as e:
        # If there's an error, print it and return `None`
        print("Error fetching URL:", e)
    return None

# Start the main script
if __name__ == '__main__':
    url = "https://itch.io/jams"                                                # Define the URL of the GameJams listing page.
    html_content = fetch_html(url)                                              # Fetch the content of the listing page.

    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')                       # Parse the fetched HTML content using BeautifulSoup.
        jam_cells = soup.find_all('div', class_="jam_cell")                     # Find all GameJam cells in the parsed HTML.

        jam_data = []                                                           # Create an empty list to store GameJam data.
        index = 1                                                               # To keep track of the current GameJam number.

        for jam_cell in jam_cells:
            # Print the current progress to the terminal.
            print("{}/{}".format(index, len(jam_cells)), end="\r")              

            # Get the GameJam ID, link, and title from the current GameJam cell.
            jam_id = jam_cell.get('data-jam_id')                                
            jam_link_element = jam_cell.find('a')                               
            jam_link = 'https://itch.io' + jam_link_element.get('href')         
            jam_content = fetch_html(jam_link)                                  
            jam_title = jam_link_element.text.strip()                      
            """
            # Check if the GameJam has ended; if so, skip it.
            if 'This jam is now over. It ran from ' in jam_content:
                print('{} ended'.format(jam_title))                             
                index += 1
                continue
            """
            # Fetch and parse the content of the GameJam detail page.
            if jam_content:
                soup1 = BeautifulSoup(jam_content, 'html.parser')
                description = soup1.find('div', class_='jam_content')

                # Check if the description contains a dollar sign; if so, process it.
                if description and re.search(r'\$', description.text):
                    #print(jam_title)
                    joined_count_element = jam_cell.find('span', class_='joined_count')

                    # Get the number of participants and clean it up.
                    if joined_count_element:
                        count_text = joined_count_element.text.strip('()').split()[0]
                        count_text_no_commas = count_text.replace(',', '')
                        jam_joined = int(count_text_no_commas)
                    else:
                        jam_joined = 0

                    # Find all sentences containing a dollar sign.
                    dollar_sentences = []
                    texts = description.find_all(string=True)
                    for text in texts:
                        if find_dollar_sign(text):
                            sentence = re.sub(r'\s+(?<! )', '', text.text)
                            dollar_sentences.append(sentence.strip())

                    # Only add jam data if dollar_sentences is not empty
                    if dollar_sentences:  
                        jam_data.append({
                            'Jam ID': jam_id,
                            'Jam Link': jam_link,
                            'Jam Title': jam_title,
                            'Joined Count': jam_joined,
                            'Dollar Sentences': ' | '.join(dollar_sentences)
                        })
                    else:
                        print(jam_link)
                # If the description is None, print an error message.
                elif (description is None):
                    print("Error reading description: {}".format(jam_link))
            # Increment the index for the next GameJam.
            index += 1
        # Create a DataFrame from the collected GameJam data.
        df = pd.DataFrame(jam_data, columns=['Jam ID', 'Jam Link', 'Jam Title', 'Joined Count', 'Dollar Sentences'])

        # Uncomment the next line to export the DataFrame to a CSV file
        df.to_csv('jam_data.csv', index=False)
        
        # Write the DataFrame to Google Sheet
        write_to_sheet(df)

        #print(df)
    else:
        print("No content found.")
