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
        self.links_index_of_internal_links = dict()
        self.index_of_internal_external_links = 0
        self.search_link = URL
        self.links_to_csv = dict()
        self.new_url_for_spider = None
        self.searchIDX = 0
        self.actually_url = None
        self.basic_url = None
        self.base_url = None
        self.external_numbers = 0
        self.number_of_external_links = 0
        self.index_of_all_get_links = 1
        self.link_views_dict = dict()
        self.views_pages_number = None
        self.url = URL
        self.soup = None
        self.response = None
        self.internal_numbers = None
        self.link_title_dict = dict()
        self.id_link = dict()
        self.id_link[1] = URL
        create_csv_headers()
        self.get_links()

    def get_links(self):
        self.index_of_internal_external_links = 0
        self.url = self.search_link
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
            if self.searchIDX > 3:
                break

            if get_link[0:5] != "https":
                continue

            if get_link in self.link_title_dict:
                self.link_views_dict[get_link] = self.link_views_dict[get_link] + 1
                continue

            else:
                self.links_to_csv[get_link] = get_title
                self.link_title_dict[get_link] = get_title
                self.link_views_dict[get_link] = 1

                # licznik wszystkich znalezionych linków
                self.index_of_all_get_links += 1

                #słownik : numer linku i link
                self.id_link[self.index_of_all_get_links] = get_link

                #licznik podstron
                self.index_of_internal_external_links += 1



        self.new_url()

    def new_url(self):
        self.searchIDX += 1

        #dodanie do słownika linku i liczby podstron odnalezionych na tej stronie
        self.links_index_of_internal_links[self.search_link] = self.index_of_internal_external_links
        self.new_url_for_spider = self.id_link.get(self.searchIDX)
        self.render_name_page()
        self.search_link = self.new_url_for_spider
        self.get_links()

    def render_name_page(self):
        link = tuple(self.search_link)
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

        if self.search_link == self.base_url:
            self.internal_numbers += 1

        if self.search_link != self.base_url:
            self.external_numbers += 1

    def add_data_to_csv(self):

        for k, v in self.links_to_csv.items():
            print("{}: {}".format(k, v))
            data = {
                'link': [k],
                'title': [v],
                'number of internal links': [self.index_of_internal_external_links],
                'number of external links': [self.external_numbers],
                'number of times url was referenced by other pages': [self.number_of_external_links]
            }
            df = pd.DataFrame(data)
            df.to_csv('data.csv', mode='a', index=False, header=False)
            self.index_of_internal_external_links = 0
        self.links_to_csv = dict()


start = WebCrawler("https://www.youtube.com/")

#TODO:Przepraszam za niekompletną funkcję zliczania
# podstron i podstron podstron ale przez te nocne kodowanie przysypiam na fotelu ,
# za mało czasu miałem na napisanie tego "Simple web crawler" z podkreśleniem na Simple :)
# 4 dni walczyłem z szukaniem normal.mod na partycjach zeby zainstalować Ubuntu na tym dinozaurze (laptopie)
# Cud że wogóle pyCharm na tym odpalił więc utknięcie w pętli podczas testowania programu kończyło się :black screen,
# Coś w stylu : kiedy junior programuje ,google, stackoverflow, copy , paste , error : black screen , reset system , polubiłem już te memy :)
# jeśli jakimś cudem dostanę się na ten staż to chyba tylko dlatego że ktoś doceni te moje wypociny i to że starałem
# się jak tylko umiałem , niestety za mało czasu miałem żeby doprowadzić ten kod do 100% sprawności
# Ps. Proszę o sprawdzenie commitów
# dziękuje za poświęcony czas !
