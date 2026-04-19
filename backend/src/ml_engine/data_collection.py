
import sys
from pathlib import Path

# 1. Get the path to the current notebook directory (ml_engine)
# current_dir = Path.cwd()

# # 2. Navigate up three levels to reach the project root ('Ai-stock-analytics')
# # Current: ml_engine
# # Parent: src
# # Grandparent: backend
# # Great-Grandparent: Ai-stock-analytics (This is the required path)
# project_root = current_dir.parent.parent
# print(f"current_dir: {current_dir}")
# print(f"project_root: {project_root}")
# # 3. Add the project root to sys.path
# if str(project_root) not in sys.path:
#     sys.path.insert(0, str(project_root))

# print(f"Project root added to sys.path: {project_root}")
# print("\nNew sys.path:")
# for path in sys.path:
#     print(path)

import yfinance as yf
import requests

# ---- UNIVERSAL PATCH: Force yfinance to use custom headers ---- #

"""
Patches yfinance to use a custom requests.Session with specific headers.
This helps in avoiding request blocks by Yahoo Finance servers.
"""
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive'
})


def dataFrame(ticker,start, session=session):
    """
    Downloads historical stock/index data using yfinance with custom headers."""
    # Monkey patch yfinance globally
    yf.utils.requests = session

    print("Downloading data...")
    df = yf.download(ticker, start=start, interval="1d", progress=False)
    print(f"{ticker} Data downloaded successfully.")
    return df



if __name__ == "__main__":
    print("ML Engine main executed")