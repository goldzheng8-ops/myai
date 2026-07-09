import requests

r = requests.get("https://news.ycombinator.com", timeout=10)
print(r.status_code)