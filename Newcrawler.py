import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


def create_csv_headers():
    headers = ["link",
               "title",
               "internal_links",
               "external_links",
               "reference_count"]
    with open("data.csv", "w") as file:
        create = csv.writer(file)
        create.writerow(headers)


class WebCrawler:

    def __init__(self, URL, count_of_results):
        self.ALL_DATA_TO_CSV = {URL: {'title': "home page", 'internal_links': 0,
                                      'external_links': 0, 'reference_count': 0}}
        self.soup = None
        self.response = None
        self.link_title_dict = dict()  # słownik link:tytuł
        self.id_link_dict = dict()  # słownik numer strony : tytuł
        self.id_link_dict[1] = URL
        self.link_true_false_dict = dict()  # słownik link: true/false
        self.link_true_false_dict[URL] = False
        self.internal_link_link_dict = dict()  # słownik : podstrona : link
        self.index_of_internal_external_links = 0
        self.search_link = URL
        self.counter = count_of_results
        self.searchIDX = 0
        self.true_false = None
        self.index_of_all_get_links = 1
        self.links_cleaner = URL

        create_csv_headers()
        self.render_name_page()
        self.get_links()

    def get_links(self):
        self.index_of_internal_external_links = 0
        self.response = requests.get(self.search_link)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.spider()

    def spider(self):
        for link in self.soup.find_all('a', href=True):
            get_link = f"{link.get('href')}"
            get_title = f"{link.string}"

            if get_link[0:5] != "https":
                continue

            if get_link in self.link_title_dict:
                self.ALL_DATA_TO_CSV[get_link]['reference_count'] += 1
                continue

            else:
                self.link_true_false_dict[get_link] = True
                self.links_cleaner = get_link
                self.render_name_page()

                # Ustawienie dla kazdego otrzymanego linku , linku nadrzednego
                self.internal_link_link_dict[get_link] = self.search_link
                # dodanie do słownika linku i tytułu
                if get_link in self.ALL_DATA_TO_CSV:
                    self.ALL_DATA_TO_CSV[get_link]['title'] = get_title
                else:
                    self.ALL_DATA_TO_CSV[get_link] = {'title': get_title}

                self.link_title_dict[get_link] = get_title
                if get_link not in self.ALL_DATA_TO_CSV:
                    self.ALL_DATA_TO_CSV[get_link]['reference_count'] += 1
                else:
                    self.ALL_DATA_TO_CSV[get_link]['reference_count'] = 1

                # licznik wszystkich znalezionych linków
                self.index_of_all_get_links += 1

                # słownik : numer linku i link , dodanie do słownika
                self.id_link_dict[self.index_of_all_get_links] = get_link

                # licznik podstron
                self.index_of_internal_external_links += 1

        self.new_url()

    def new_url(self):

        self.true_false = self.link_true_false_dict.get(self.search_link)
        if self.true_false:
            # wczytanie nadrzędnego linku
            search_link_for_add_number_external_links = self.internal_link_link_dict.get(self.search_link)

            # dodanie liczy popodstron do linku aktualnie obsługiwanej podstrony
            if search_link_for_add_number_external_links not in self.ALL_DATA_TO_CSV:
                self.ALL_DATA_TO_CSV[search_link_for_add_number_external_links]['external_links'] += \
                    self.index_of_internal_external_links
            else:
                self.ALL_DATA_TO_CSV[search_link_for_add_number_external_links]['external_links'] = \
                    self.index_of_internal_external_links


        # następny sprawdzany link +1
        self.searchIDX += 1

        # dodanie do słownika linku i liczby podstron odnalezionych na tej stronie
        self.ALL_DATA_TO_CSV[self.search_link]['internal_links'] = self.index_of_internal_external_links

        # następny sprawdzany link
        new_url_for_spider = self.id_link_dict.get(self.searchIDX)
        self.search_link = new_url_for_spider
        self.get_links()
        self.counter -= 1
        if self.counter > 0:
            self.get_links()
        else:
            self.add_data_to_csv()

    def render_name_page(self):
        link = list(self.links_cleaner)
        from_end = link[::-1]
        dot_or_slash_index = from_end.index('.')
        take_url = dot_or_slash_index - 4
        no_dot = from_end[take_url:]
        from_end = no_dot[::-1]
        joined = ''.join(from_end)
        print(joined)
        if joined in self.link_title_dict:
            self.ALL_DATA_TO_CSV[joined]['reference_count'] += 1
        else:
            self.ALL_DATA_TO_CSV[joined] = {'reference_count': 1}

    def add_data_to_csv(self):

        for link, values in self.ALL_DATA_TO_CSV.items():
            data = {
                'link': [link],
                'title': [self.ALL_DATA_TO_CSV[link]['title']],
                'internal_links': [self.ALL_DATA_TO_CSV[link]['internal_links']],
                'external_links': [self.ALL_DATA_TO_CSV[link]['external_links']],
                'reference_count': [self.ALL_DATA_TO_CSV[link]['reference_count']]
            }
            df = pd.DataFrame(data)
            df.to_csv('data.csv', mode='a', index=False, header=False)


start = WebCrawler("https://www.youtube.com/", 5)
