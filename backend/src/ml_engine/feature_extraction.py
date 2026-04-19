import pandas as pd 
import numpy as np

#---------------------------------------Feature Engineering---------------------------------------#
def feature_engineering(df):
  """
    Generates additional features for the stock data.
  """
  df["diff_open_close"] = df["Open"] - df["Close"]
  df["diff_high_low"] = df["High"] - df["Low"]
  df["day_of_week"] = df["Date"].dt.dayofweek
  df["VMA_5"] = df["Volume"].rolling(window=5).mean()
  df["VMA_10"] = df["Volume"].rolling(window=10).mean()
  df["VMA_20"] = df["Volume"].rolling(window=20).mean()
  df["RSI_14"] = 100 - (100 / (1 + (df["Close"].diff().apply(lambda x: x if x > 0 else 0).rolling(window=14).mean() / df["Close"].diff().apply(lambda x: -x if x < 0 else 0).rolling(window=14).mean())))
  df["rolling_mean_3"] = df["Close"].rolling(window=3).mean()
  df["rolling_std_3"] = df["Close"].rolling(window=3).std()
  df["rolling_mean_7"] = df["Close"].rolling(window=7).mean()
  df["rolling_std_7"] = df["Close"].rolling(window=7).std()
  df["rolling_mean_21"] = df["Close"].rolling(window=21).mean()
  df["rolling_std_21"] = df["Close"].rolling(window=21).std()
  df["target"] = df["Close"].shift(-1)  # Next day's closing price as target
  df['Daily_Return'] = df['Close'].pct_change()
  df['Target_Return'] = df['Daily_Return'].shift(-1)
  df = df.dropna()  # Drop rows with NaN values resulting from rolling calculations
  return df


def final_df(Nifty_50, SnP_500_df, NASDAQ_df):
    """
    Combines Nifty 50 data with S&P 500 and NASDAQ returns.
    """
    df = feature_engineering(Nifty_50)

    # before joining, set index to Date for all dataframes------------------------

    # df.columns = Nifty_50.columns.get_level_values(0)
    # SnP_500_df.columns = SnP_500_df.columns.get_level_values(0)
    # NASDAQ_df.columns = NASDAQ_df.columns.get_level_values(0)

    # print(df.columns)
    # print(SnP_500_df.columns)
    # print(NASDAQ_df.columns)

    # df.columns.name = None
    # SnP_500_df.columns.name = None
    # NASDAQ_df.columns.name = None


    df.set_index('Date', inplace=True)
    SnP_500_df.set_index('Date', inplace=True)
    NASDAQ_df.set_index('Date', inplace=True)
    # df["SnP"] = SnP_500_df["Index_Return"]
    # df["NASDAQ"] = NASDAQ_df["Index_Return"]
    # print("after setting index:-------------------------------------------")

    # print(df.columns)
    # print(SnP_500_df.columns)
    # print(NASDAQ_df.columns)

    # SnP_500_df = SnP_500_df.rename(columns={"Index_Return": "SnP"})
    # NASDAQ_df = NASDAQ_df.rename(columns={"Index_Return": "NASDAQ"})

    # df = df.join(SnP_500_df, how="left").join(NASDAQ_df, how="left")

    df["SnP"] = SnP_500_df["Index_Return"]
    df["NASDAQ"] = NASDAQ_df["Index_Return"]
    df = df.dropna()  # Drop rows with NaN values after joining

    return df

