import requests
from bs4 import BeautifulSoup

url="https://www.youtube.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
idx = 0
data = dict()
for link in soup.find_all('a',href=True):
    idx += 1
    if (f"{link.get('href')}") == '/None':
        continue
    if (f"{link.get('href')}") in data:
        # TODO:licznik wyswietlen
        #  licznik podstron
        #  licznik stron
        #  stworzenie pająka poprzez dodawanie w petli nowych url
        break
    data[(f"{link.get('href')}"
        f"{link.string}")] += idx

for line in data:
    print(line)
