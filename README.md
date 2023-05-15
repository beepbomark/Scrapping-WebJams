# Web Scraping Game Jams with Prize Money
Manually browsing and checking each GameJam listed on itch.io for prize money can be a time-consuming task. To make this process more efficient, this web scraping script is designed to automatically filter and list the GameJams with prize money, easing our lives and saving us time.
 
## Overview
The script fetches the GameJam list from itch.io and filters out jams with a description containing a dollar sign ($), indicating prize money. The result is a list of relevant GameJams, which can be exported to a CSV file for further analysis or reference.

## Dependencies
To run the script, you'll need the following Python libraries:

* **`requests`**: To make HTTP requests and fetch web pages.
* **`BeautifulSoup`**: To parse and work with HTML content.
* **`pandas`**: To manipulate data and create DataFrames.
* **`re`**: To perform regular expression operations.

## Usage
1. Clone or download the repository to your local machine.
2. Make sure you have Python and the required libraries installed.
3. Run the script using your Python interpreter:

## Output
The resulting DataFrame and CSV file will contain the following columns:
* **`Jam ID`**: The unique identifier of the GameJam.
* **`Jam Link`**: The URL to the GameJam page on itch.io.
* **`Jam Title`**: The title of the GameJam.
* **`Joined Count`**: The number of participants in the GameJam.
* **`Dollar Sentences`**: The sentences from the description containing a dollar sign ($), indicating prize money.

The script will fetch the list of GameJams from itch.io and filter out the ones with prize money in their description. It will print the result in the terminal and export the list to a CSV file named **`jam_data.csv`** in the same directory.
## Google Sheets Integration for Web Scraping
In our project, we have integrated Google Sheets as a database to store and manage the data scraped from various game jam websites. We use the Google Sheets API to automate the process of updating the sheet with the latest data each time our web scraping script is run.
The data scraped from the web is written into the Google Sheets document in a structured format, allowing for easy analysis and comparison of different game jams. This simplifies the process of monitoring and analyzing the data over time. 
The link to the Google Sheets is: https://docs.google.com/spreadsheets/d/1P-bMkUd19Xajdj2bZAMkWNvzHvz96xwYFRrbl0QghEE/edit#gid=0

## Code Explanation
The script follows these steps:
1. Define helper functions, such as `fetch_html` to fetch the content of a URL, and `find_dollar_sign` to check if a text contains a dollar sign.
2. Fetch the main GameJams listing page from itch.io using the `fetch_html` function.
3. Parse the fetched HTML content using BeautifulSoup to find and loop through all the individual GameJam cells.
4. For each GameJam, fetch the corresponding detail page to check its description.
5. Use the `find_dollar_sign` function and regular expressions to filter out GameJams with prize money mentioned in their description.
6. Collect the filtered GameJams' details, such as ID, link, title, joined count, and dollar sentences.
7. Create a DataFrame using pandas to store and display the collected data.
8. Optionally, export the DataFrame to a CSV file for further use.

Throughout the script, progress updates are printed in the terminal to keep track of the current GameJam being processed.
