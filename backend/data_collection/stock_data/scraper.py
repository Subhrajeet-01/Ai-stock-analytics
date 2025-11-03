import requests
from bs4 import BeautifulSoup
import csv
import os 
from .list_to_csv import list_of_lists_to_csv

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
    
    # Enhanced headers for better bot detection avoidance.
    # Accept-Language is used to specify English preference.
    # Accept-Encoding is included to handle compressed responses.
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
        
        if response.status_code != 200:
            print(f"Fetch failed! Received status code: {response.status_code}")
            response.raise_for_status() # This will raise the HTTPError for 4xx/5xx codes
        
        print("Successfully fetched the page content (Status 200).")
    except requests.exceptions.RequestException as e:
        # Catch and report any request-related error (404, 403, Timeout, etc.)
        print(f"Error fetching the URL: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    row_contents = []  
    extracted_contents = [] 

    # Find all <tr> elements that have the specific class 'yf-1jecxey'
    target_rows = soup.find_all('tr', class_='yf-1jecxey')

    for row in target_rows:
        # Find all <td> children within this row
        td_elements = row.find_all('td')
        
        # This will append all 7 data points sequentially to the list
        for td in td_elements:
            # Use .text.strip() to get clean text without extra whitespace
            row_contents.append(td.text.strip())
        if len(row_contents) == 7:
            extracted_contents.append(row_contents)

        row_contents = []  # Reset for the next row
    return extracted_contents


if __name__ == "__main__":

    company_symbols = ["RELIANCE.NS", "HDFCBANK.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS"]  
    for company_symbol in company_symbols:
        # The target URL provided by the user
        target_url = f"https://finance.yahoo.com/quote/{company_symbol}/history/?period1=1611446400&period2=1761296771"

        # Get all the extracted content
        extracted_data = extract_td_contents(target_url)

        # Convert the list of lists into CSV format
        csv_output = list_of_lists_to_csv(extracted_data, directory="historical_data", filename=f"{company_symbol}_historical_data.csv")

    print(csv_output)