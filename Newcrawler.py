import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


def create_csv_headers():
    headers = ["link",
               "title",
               "number of internal links",
               "number of external links",
               "number of times url was referenced by other pages"]
    with open("data.csv", "w") as file:
        create = csv.writer(file)
        create.writerow(headers)


class WebCrawler:

    def __init__(self, URL):
        self.new_url_for_spider = None
        self.pages_idx = 0
        self.searchIDX = 0
        self.actually_url = None
        self.basic_url = None
        self.base_url = None
        self.external_numbers = 0
        self.number_of_external_links = 0
        self.URL = URL
        self.IDX = -1
        self.link_views_dict = dict()
        self.views_pages_number = None
        self.url = URL
        self.soup = None
        self.response = None
        self.internal_numbers = None
        self.link_title_dict = dict()
        self.id_link = dict()
        create_csv_headers()
        self.get_links()

    def get_links(self):
        self.pages_idx = -1
        self.url = self.URL
        self.base_url = self.url
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.internal_numbers = -1
        self.spider()

    def spider(self):
        for link in self.soup.find_all('a', href=True):
            get_link = f"{link.get('href')}"
            get_title = f"{link.string}"
            self.views_pages_number = 0

            if get_link[0:5] != "https":
                continue

            if get_link in self.link_title_dict:
                self.link_views_dict[get_link] = self.link_views_dict[get_link] + 1
                continue

            else:
                self.link_title_dict[get_link] = get_title
                self.link_views_dict[get_link] = 1
                self.id_link[self.IDX] = get_link
                self.pages_idx += 1
                self.IDX += 1

        self.add_data_to_csv()
        self.new_url()

    def new_url(self):
        self.searchIDX += 1
        self.new_url_for_spider = self.id_link.get(self.searchIDX)
        self.render_name_page()
        self.URL = self.new_url_for_spider
        self.get_links()

    def render_name_page(self):
        link = tuple(self.URL)
        actually_url = tuple(self.new_url_for_spider)
        index_of_dot_1 = link.index(".")
        index_of_dot_1_2 = actually_url.index(".")
        take_url = index_of_dot_1 + 1
        take_url_2 = index_of_dot_1_2 + 1
        no_dot = link[take_url:]
        no_dot_2 = actually_url[take_url_2:]

        if "." not in no_dot:
            self.basic_url = no_dot

        if "." not in no_dot_2:
            self.basic_url = no_dot_2

        if "." in no_dot:
            index_of_dot_2 = no_dot.index('.')
            self.basic_url = no_dot[:index_of_dot_2]
        if "." in no_dot_2:
            index_of_dot_2_2 = no_dot_2.index('.')
            self.actually_url = no_dot_2[:index_of_dot_2_2]

        self.number_internal_external_links()

    def number_internal_external_links(self):
        if self.new_url_for_spider != self.basic_url:
            self.number_of_external_links += 1

        if self.URL == self.base_url:
            self.internal_numbers += 1

        if self.URL != self.base_url:
            self.external_numbers += 1

    def add_data_to_csv(self):
        for k, v in self.link_title_dict.items():
            print("{}: {}".format(k, v))
            data = {
                'link': [k],
                'title': [v],
                'number of internal links': [self.pages_idx],
                'number of external links': [0],
                'number of times url was referenced by other pages': [0]
            }
            df = pd.DataFrame(data)
            df.to_csv('data.csv', mode='a', index=False, header=False)
            self.pages_idx = 0


start = WebCrawler("https://www.youtube.com/")

#TODO:Przepraszam za niekompletną funkcję zliczania
# podstron i podstron podstron ale przez te nocne kodowanie przysypiam na fotelu ,
# za mało czasu miałem na napisanie tego "Simple web crawler" z podkreśleniem na Simple :)
# 4 dni walczyłem z szukaniem normal.mod na partycjach zeby zainstalować Ubuntu na tym dinozaurze (laptopie)
# Cud że wogóle pyCharm na tym odpalił więc utknięcie w pętli podczas testowania programu kończyło się :black screen,
# Coś w stylu : kiedy junior programuje ,google, stackoverflow, copy , paste , error : black screen , reset system , polubiłem już te memy :)
# jeśli jakimś cudem dostanę się na ten staż to chyba tylko dlatego że ktoś doceni te moje wypociny i to że starałem
# się jak tylko umiałem , niestety za mało czasu miałem żeby doprowadzić ten kod do 100% sprawności
# dziękuje za poświęcony czas !