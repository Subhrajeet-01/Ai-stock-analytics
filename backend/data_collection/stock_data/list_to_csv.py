import csv
import os
from io import StringIO  # Used to capture CSV output in memory

def list_of_lists_to_csv(data_rows, directory="historical_data", filename="historical_data.csv"):
    """
    Converts a list of lists (where each inner list is a data row) into 
    a CSV formatted string. This assumes the data within each row is 
    already ordered correctly in the sequence:
    [Date, Open, High, Low, Close, Adj. Close, Volume]
    """

    filepath = os.path.join(directory, filename)

    # Ensure the directory exists.
    try:
        os.makedirs(directory, exist_ok=True) 
    except Exception as e:
        print(f"Warning: Could not create directory '{directory}'. Proceeding to try writing to file path: {filepath}. Error: {e}")
    

    # Define the required column headers
    headers = ["Date", "Open", "High", "Low", "Close", "Adj. Close", "Volume"]

    # Use StringIO to simulate a file for the csv writer
    try:
        # Open the file for writing (newline='' to prevent extra blank lines on Windows)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write the header row
            writer.writerow(headers)
            
            # Write the data rows
            for row in data_rows:
                # Ensure correct slicing
                writer.writerow(headers, row)
        
        print(f"Successfully saved {len(data_rows)} rows to CSV file: {filepath}")
    except Exception as e:
        print(f"Error writing CSV file to {filepath}: {e}")
