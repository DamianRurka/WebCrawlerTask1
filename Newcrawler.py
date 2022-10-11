import requests
from bs4 import BeautifulSoup



class WebCrawler:


    def __init__(self,URL):
        self.URL = URL
        self.IDX = 1
        self.link_views_dict = None
        self.views_pages_number = None
        self.url = None
        self.soup = None
        self.response = None
        self.pages_number = None
        self.link_title_dict = None
        self.id_link = None
        self.get_links()

    def get_links(self):
        self.url = self.URL
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.pages_number = -1
        self.link_title_dict = dict()
        self.link_views_dict = dict()
        self.id_link = dict()

        for link in self.soup.find_all('a', href=True):
            get_link = f"{link.get('href')}"
            get_title = f"{link.string}"
            self.views_pages_number = 0

            if get_link == '/None' or \
                    get_link == "/" or \
                    get_link == "/new" or \
                    get_link == "/t/terms" or \
                    get_link == "/t/privacy" or \
                    get_link == '/t/contact_us/':
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
                self.pages_number += 1  # TODO:liczba podstron na stronie
                self.link_views_dict = {get_link: 1}  # TODO: number of page views
                self.id_link = {self.IDX: get_link}
        new_url_for_spider = self.id_link.get(self.IDX)
        self.IDX += 1
        if new_url_for_spider != self.url:

            self.URL = new_url_for_spider

            self.get_links()


start = WebCrawler("https://www.youtube.com/")
start.get_links()

