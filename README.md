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

Now you have an automated solution to find GameJams with prize money on itch.io, making it easier to decide which ones to participate in. Happy gaming!
