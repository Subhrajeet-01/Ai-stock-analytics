import pandas as pd
from backend.src.ml_engine.data_collection import dataFrame

def get_index_returns(ticker, start_date):
    """
    Downloads historical index data, calculates daily returns, and cleans the result.
    """
    print(f"Downloading {ticker} data from {start_date} to today...")

    try:
        Stock_Data = dataFrame(ticker, start_date)
        index_data = pd.DataFrame(Stock_Data)
        index_data = index_data.reset_index()  # Reset index to make 'Date' a column
        index_data.columns = index_data.columns.get_level_values(0)  # Flatten MultiIndex columns
        # index_data['Date'] = pd.to_datetime(index_data['Date'], format="%Y-%m-%d", errors='coerce')
        if index_data.empty:
            print(f"Error: No data found for ticker {ticker} in the specified range.")
            return None

        # Calculate the Daily Return Feature
        # Use Adj Close for accurate returns over time
        index_data['Index_Return'] = index_data['Close'].pct_change()
        # Keep only the date index and the return feature
        index_feature = index_data[['Date','Index_Return']].dropna()
        
        print(f"Successfully downloaded {index_feature.shape[0]} rows and calculated returns for {ticker}.")
        return index_feature

    except Exception as e:
        print(f"An error occurred during download: {e}")
        return None


# ----------------------------------- data preparation ----------------------------------- #
def data_preparation(Stock_Data):
  """
    Prepares the stock/index data by resetting index and flattening columns.
  """
  df = pd.DataFrame(Stock_Data)
  df = df.reset_index()  # Reset index to make 'Date' a column
  df.columns = df.columns.droplevel(1)
  df.columns = df.columns.get_level_values(0)  # Flatten MultiIndex columns if any
  print(df.columns)
  return df


def index_data(START_DATE, ticker):
    """
    Downloads and prepares index data for Nifty 50, S&P 500, and NASDAQ.
    Returns cleaned DataFrames for each index.
    """
    for i in ticker:
        if i == "^NSEI":
            Nifty_50 = dataFrame(i, START_DATE)
            Nifty_50 = data_preparation(Nifty_50)
            # Nifty_50.set_index('Date', inplace=True)
            Nifty_50.drop(Nifty_50.tail(1).index, inplace=True)        #Drop last row to Predict todays Market
        elif i == "^GSPC":
            SnP_500_df = get_index_returns(i, START_DATE)
            # SnP_500_df = data_preparation(SnP_500_df)
            # SnP_500_df.set_index('Date', inplace=True)
        else:
            NASDAQ_df = get_index_returns(i, START_DATE)
            # NASDAQ_df = data_preparation(NASDAQ_df)
            # NASDAQ_df.set_index('Date', inplace=True)

    return Nifty_50, SnP_500_df, NASDAQ_df
    

if __name__ == "__main__":
    START_DATE = "2025-07-01"
    ticker = ["^NSEI", "^GSPC", "^IXIC"]
    Nifty_50, SnP_500_df, NASDAQ_df = index_data(START_DATE, ticker)
    print("After data preparation:-------------------------------------------")
    print(Nifty_50.info())
    print(SnP_500_df.info())
    print(NASDAQ_df.info())