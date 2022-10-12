import requests
from bs4 import BeautifulSoup
import csv


class WebCrawler:

    def __init__(self, URL):
        self.actually_url = None
        self.basic_url = None
        self.base_url = None
        self.external_numbers = 0
        self.number_of_external_links = 0
        self.URL = URL
        self.IDX = 1
        self.link_views_dict = None
        self.views_pages_number = None
        self.url = URL
        self.soup = None
        self.response = None
        self.internal_numbers = None
        self.link_title_dict = None
        self.id_link = None
        self.get_links()

    def number_internal_external_links(self):
        if self.actually_url != self.basic_url:
            self.number_of_external_links += 1

        if self.URL == self.base_url:
            self.internal_numbers += 1

        if self.URL != self.base_url:
            self.external_numbers += 1

        self.add_data_to_csv()

    def add_data_to_csv(self):

        all_data_to_save = []
        with open('data.csv', 'w') as creating_new_csv_file:
            pass

    def crawl_next_page(self):
        new_url_for_spider = self.id_link.get(self.IDX)
        self.IDX += 1
        if new_url_for_spider != self.url:
            self.URL = new_url_for_spider

            self.get_links()

    def render_name_page(self):
        link = tuple(self.base_url)
        actually_url = tuple(self.URL)
        index_of_dot_1 = link.index(".")
        index_of_dot_1_2 = actually_url.index(".")
        take_url = index_of_dot_1 + 1
        take_url_2 = index_of_dot_1_2 + 1
        no_dot = link[take_url:]
        no_dot_2 = actually_url[take_url_2:]
        print(no_dot)
        print(no_dot_2)
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

    def get_links(self):
        self.url = self.URL
        self.base_url = self.url
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.internal_numbers = -1
        self.link_title_dict = dict()
        self.link_views_dict = dict()
        self.id_link = dict()
        self.spider()

    def spider(self):
        for link in self.soup.find_all('a', href=True):
            get_link = f"{link.get('href')}"
            get_title = f"{link.string}"
            self.views_pages_number = 0

            if get_link[0:5] != "https":
                continue
            if get_link in self.link_title_dict:
                self.views_pages_number = self.link_views_dict.get(get_link)
                new_views_pages_number = self.views_pages_number + 1
                self.link_views_dict = {get_link: new_views_pages_number}
                continue
            else:
                for k, v in self.link_title_dict.items():
                    print("{}: {}".format(k, v))

                self.link_title_dict = {get_link: get_title}
                self.render_name_page()

            self.link_views_dict = {get_link: 1}
            self.id_link = {self.IDX: get_link}
            self.crawl_next_page()


start = WebCrawler("https://www.youtube.com/")
start.get_links()
