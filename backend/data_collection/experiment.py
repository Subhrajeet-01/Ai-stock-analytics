import requests
from bs4 import BeautifulSoup
import re
import sys
import csv
from io import StringIO # Used to capture CSV output in memory
import os # Import os for file path and directory operations


def extract_td_contents(url):
    """
    Fetches a webpage, parses its HTML, and returns a list of text contents 
    from all <td> tags nested within <tr> tags that have the class 'yf-1jecxey'.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        list: A flat list containing the stripped text content (strings) of 
              all extracted data points, sequenced in scrape order (7 items per row).
    """
    print(f"Attempting to fetch data from: {url}")
    
    # --- ENHANCED HEADERS FOR BETTER BOT DETECTION AVOIDANCE ---
    # We include several headers to mimic a modern, English-language Chrome browser.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9', # Crucial: tells the server we prefer US English
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
    }
    
    try:
        # Fetch the HTML content
        response = requests.get(url, headers=headers, timeout=20)
        
        # Check for status codes carefully
        if response.status_code != 200:
             # Log the actual non-200 status code received
            print(f"Fetch failed! Received status code: {response.status_code}")
            response.raise_for_status() # This will raise the HTTPError for 4xx/5xx codes
        
        print("Successfully fetched the page content (Status 200).")
    except requests.exceptions.RequestException as e:
        # Catch and report any request-related error (404, 403, Timeout, etc.)
        print(f"Error fetching the URL: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    row_contents = []  # To hold the final extracted data points
    extracted_contents = []

    # Find all <tr> elements that have the specific class 'yf-1jecxey'
    target_rows = soup.find_all('tr', class_='yf-1jecxey')

    # Iterate through each row and extract its <td> children
    for row in target_rows:
        # Find all <td> children within this row
        td_elements = row.find_all('td')
        
        # Extract and store the text content of each <td> child
        # This will append all 7 data points sequentially to the flat list
        for td in td_elements:
            # Use .text.strip() to get clean text without extra whitespace
            row_contents.append(td.text.strip())
        if len(row_contents) == 7:
            extracted_contents.append(row_contents)
        row_contents = []  # Reset for the next row
    return extracted_contents

def list_of_lists_to_csv(data_rows, directory="historical_data", filename="historical_data.csv"):
    """
    Converts a list of lists (where each inner list is a data row) into 
    a CSV formatted string. This assumes the data within each row is 
    already ordered correctly in the sequence:
    [Date, Open, High, Low, Close, Adj. Close, Volume]
    """

    filepath = os.path.join(directory, filename)

    # Note: os.makedirs is used here assuming a standard Python environment 
    # where file system access is permitted.
    try:
        os.makedirs(directory, exist_ok=True) 
    except Exception as e:
        print(f"Warning: Could not create directory '{directory}'. Proceeding to try writing to file path: {filepath}. Error: {e}")
    

    # Define the required column headers
    headers = ["Date", "Open", "High", "Low", "Close", "Adj. Close", "Volume"]
    
    # Use StringIO to simulate a file for the csv writer
    try:
        # Open the file for writing (newline='' is important for CSV files in Python)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write the header row
            writer.writerow(headers)
            
            # Write the data rows
            for row in data_rows:
                writer.writerow(row)
        
        print(f"Successfully saved {len(data_rows)} rows to CSV file: {filepath}")
    except Exception as e:
        print(f"Error writing CSV file to {filepath}: {e}")
        # If saving fails (common in sandboxed environments), print the content as a fallback
        print("\n--- Fallback: CSV Content that would have been saved ---")
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(data_rows)
        print(output.getvalue())
        print("---------------------------------------------------------")


if __name__ == "__main__":
    # The target URL provided by the user
    target_url = "https://finance.yahoo.com/quote/RELIANCE.NS/history/?period1=1611446400&period2=1761296771"
    
    # Get all the extracted content
    extracted_data = extract_td_contents(target_url)

    # Convert the list of lists into CSV format
    csv_output = list_of_lists_to_csv(extracted_data, directory="historical_data", filename="reliance_historical_data.csv")

    print(csv_output)