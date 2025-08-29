import requests
from bs4 import BeautifulSoup

URL = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
THRESHOLD = 50.0

def get_price():
    res = requests.get(URL)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")
    price = soup.find("p", class_="price_color").text.strip()
    return float(price.replace("£", ""))

p = get_price()
if p < THRESHOLD:
    print(f"Price dropped: {p}")
else:
    print(f"Current price: {p}")
