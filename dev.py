import cloudscraper
import pandas as pd
import trafilatura
from bs4 import BeautifulSoup
from newspaper import Article


# 1. Read URLs from txt or csv
async def read_urls(filepath):
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
        urls = df.iloc[:, 0].dropna().tolist()
    elif filepath.endswith(".txt"):
        with open(filepath, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    else:
        raise ValueError("File must be .txt or .csv")
    return urls


# 2. Try Newspaper3k
async def extract_with_newspaper(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text.strip()


# 3. Try Trafilatura
async def extract_with_trafilatura(url):
    html = trafilatura.fetch_url(url)
    return trafilatura.extract(html) if html else None


# 4. Try BeautifulSoup with cloudscraper
async def extract_with_bs4(url):
    scraper = cloudscraper.create_scraper()
    res = scraper.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    article = soup.find("article") or soup.find("div", class_="article-body")
    if article:
        return " ".join(p.get_text(strip=True) for p in article.find_all("p")).strip()  # type: ignore
    return None


# 5. Main extraction logic with fallback
async def extract_article_text(url):
    for method in [extract_with_newspaper, extract_with_trafilatura, extract_with_bs4]:
        try:
            text = method(url)
            if text and len(text.split()) > 100:  # filter short junk
                return text
        except Exception:
            continue
    return None
