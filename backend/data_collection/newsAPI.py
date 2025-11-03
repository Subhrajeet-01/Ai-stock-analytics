import requests
from bs4 import BeautifulSoup
from typing import List
from backend.src.basemodel import NewsArticleModel
from urllib.parse import urljoin

def fetch_nifty50_news() -> List[NewsArticleModel]:
    url = "https://www.moneycontrol.com/news/tags/nifty-50.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print("request error:", e)
        return []

    print("status_code:", response.status_code, "url:", response.url)
    if not response.ok:
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    print("page text snippet:", soup)

    
    

if __name__ == "__main__":
    arts = fetch_nifty50_news()
    print(arts)