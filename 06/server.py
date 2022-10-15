from urllib.request import urlopen
import re
from bs4 import BeautifulSoup

URL = "https://ru.wikipedia.org/wiki/Python"
N = 1


def fetch_url(url):
    with urlopen(url) as resp:
        data = resp.read().decode("utf-8")
        soup = BeautifulSoup(data, "html.parser")
        print(soup.get_text(strip=False))
        # pattern = "<title.*?>.*?</title.*?>"
        # match_results = re.search(pattern, data, re.IGNORECASE)
        # title = match_results.group()
        # title = re.sub("<.*?>", "", title)
        # print(data)
    return data


fetch_url(URL)
