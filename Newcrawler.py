import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


def create_csv_headers():
    headers = ["link",
               "title",
               "number of internal links",
               "number of external links",
               "reference count"]
    with open("data.csv", "w") as file:
        create = csv.writer(file)
        create.writerow(headers)


class WebCrawler:

    def __init__(self, URL, count_of_results):
        self.links_internal_links_count_dict = dict()        # słownik link:liczba podstron
        self.link_title_dict = dict()                        # słownik link:tytuł
        self.id_link_dict = dict()                           # słownik numer strony : tytuł
        self.id_link_dict[1] = URL
        self.link_true_false_dict = dict()                   # słownik link: true/false
        self.link_true_false_dict[URL] = False
        self.internal_link_link_dict = dict()                # słownik : podstrona : link
        self.link_number_of_external_links_dict = dict()     # słownik link : liczba podstron
        self.clear_link_reference_count_dict = dict()        # słownik czysty link : liczba odnośników
        self.link_reference_count_dict = dict()              # słownik link : liczba odnośników
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
                self.link_reference_count_dict[get_link] += 1
                continue


            else:
                self.links_cleaner = get_link
                self.render_name_page()

                # Ustawienie dla kazdego otrzymanego linku , linku nadrzednego
                self.internal_link_link_dict[get_link] = self.search_link
                # dodanie do słownika linku i tytułu
                self.link_title_dict[get_link] = get_title

                self.link_reference_count_dict[get_link] = 1

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
            self.link_number_of_external_links_dict[search_link_for_add_number_external_links] += \
                self.index_of_internal_external_links

        # następny sprawdzany link +1
        self.searchIDX += 1

        # dodanie do słownika linku i liczby podstron odnalezionych na tej stronie
        self.links_internal_links_count_dict[self.search_link] = self.index_of_internal_external_links

        # następny sprawdzany link
        new_url_for_spider = self.id_link_dict.get(self.searchIDX)
        self.search_link = new_url_for_spider
        self.get_links()
        self.counter -= 1
        if self.counter > 0:
            self.get_links()
        else:
            pass
            # self.add_data_to_csv()



    def render_name_page(self):
        link = tuple(self.links_cleaner)
        index_of_dot = link.index(".")
        take_url = index_of_dot + 1
        no_dot = link[take_url:]

        if "." not in no_dot:
            self.links_cleaner = no_dot
            self.clear_link_reference_count_dict[self.links_cleaner] += 1

        if "." in no_dot:
            index_of_dot = no_dot.index('.')
            self.links_cleaner = no_dot[:index_of_dot]
            self.clear_link_reference_count_dict[self.links_cleaner] += 1

    # def add_data_to_csv(self):
    #
    #     for a, b  in self.link_title_dict:
    #         print("{}: {}".format(a, b))
    #         data = {
    #             'link': [a],
    #             'title': [b],
    #             'number of internal links': [self.c],
    #             'number of external links': [self.d],
    #             'reference count': [self.?????]
    #         }
    #         df = pd.DataFrame(data)
    #         df.to_csv('data.csv', mode='a', index=False, header=False)




start = WebCrawler("https://www.youtube.com/", 20)

#TODO:Przepraszam za niekompletną funkcję zliczania
# podstron i podstron podstron ale przez te nocne kodowanie przysypiam na fotelu ,
# za mało czasu miałem na napisanie tego "Simple web crawler" z podkreśleniem na Simple :)
# 4 dni walczyłem z szukaniem normal.mod na partycjach zeby zainstalować Ubuntu na tym dinozaurze (laptopie)
# Cud że wogóle pyCharm na tym odpalił więc utknięcie w pętli podczas testowania programu kończyło się :black screen,
# Coś w stylu : kiedy junior programuje ,google, stackoverflow, copy , paste , error : black screen , reset system ,
# polubiłem już te memy :)
# jeśli jakimś cudem dostanę się na ten staż to chyba tylko dlatego że ktoś doceni te moje wypociny i to że starałem
# się jak tylko umiałem , niestety za mało czasu miałem żeby doprowadzić ten kod do 100% sprawności
# Ps. Proszę o sprawdzenie commitów
# dziękuje za poświęcony czas !
