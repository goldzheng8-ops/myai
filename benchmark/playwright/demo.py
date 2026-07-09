from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            proxy={
            "server": "socks5://127.0.0.1:1080",
        },
        )

        page = browser.new_page()

        page.goto(
            "https://news.ycombinator.com",
            wait_until="networkidle"
        )

        titles = page.locator(".titleline").all_text_contents()

        print("=" * 60)

        for i, title in enumerate(titles[:10], 1):
            print(f"{i}. {title}")

        browser.close()


if __name__ == "__main__":
    main()