from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def fetch_news(limit=20):

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto("https://www.baidu.com")

        html = page.content()

        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    rows = soup.select(".athing")

    news = []

    for row in rows[:limit]:

        title = row.select_one(".titleline a").text

        link = row.select_one(".titleline a")["href"]

        news.append(
            {
                "title": title,
                "url": link
            }
        )

    return news