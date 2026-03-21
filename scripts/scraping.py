import requests
from bs4 import BeautifulSoup

url = "https://www.pentest-standard.org/index.php/Pre-engagement"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

text = soup.get_text()

with open("pre_engagement.txt", "w") as f:
    f.write(text)